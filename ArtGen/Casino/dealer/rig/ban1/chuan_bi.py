# Chuẩn bị mảnh để rig Lão Mực trong AtomSpine (GD_Claude/31 mốc D2). Đọc L1_goc_rig.png (1024 x 1536, nền xanh lơ, không viền)
# và các mảnh đã cắt ở manh/ (cat_manh.py), ghi ra ../atom/images/:
#   than.png      thân + đầu + chỏm + chân + giày (bỏ tay dưới vai, bàn tay, cổ găng, lưỡi trai; chỗ lưỡi trai che đầu tô đen lại)
#   luoi_trai.png lưỡi trai (xanh + đai kem + nút vàng), bay được khi sốc
#   tay_trai.png / tay_phai.png  dải tay (bên trái / phải người xem) từ khớp vai tới mép cổ găng, gồm nịt tay áo
#   mat_XX.png, mieng_XX.png (co theo tỉ lệ đầu), tay_XX.png (co theo cỡ găng ảnh gốc)
# và ../atom/geo.json: chỗ đặt (left, top trên khung 1024 x 1536), cỡ, các mốc khớp đo trên ảnh.
import json, os, sys
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

# mốc khớp (px ảnh L1, đọc trên soi/luoi_L1.png)
J = {
    "vai_trai": (448, 588), "co_tay_trai": (236, 858),
    "vai_phai": (578, 588), "co_tay_phai": (792, 858),
    "dau": (520, 545), "tam_dau": (520, 395), "co": (512, 560), "nguc": (512, 760), "hong": (512, 1000),
    "dui_trai": (400, 1030), "goi_trai": (398, 1170), "co_chan_trai": (402, 1320), "ban_chan_trai": (345, 1405),
    "dui_phai": (622, 1030), "goi_phai": (624, 1170), "co_chan_phai": (620, 1320), "ban_chan_phai": (678, 1405),
    "mat": (522, 378), "mieng": (522, 468),
    "luoi_trai": (545, 225), "chom1": (430, 215), "chom2": (470, 120), "chom3": (520, 85),
}


def load_rgba():
    a = np.asarray(Image.open(os.path.join(HERE, "L1_goc_rig.png")).convert("RGB")).astype(float)
    d = np.sqrt(((a - CYAN) ** 2).sum(2))
    al = np.clip((d - 70) / 40, 0, 1)
    rgb = a.copy()
    spill = (rgb[..., 2] > np.maximum(rgb[..., 0], rgb[..., 1]) + 30) & (al < 1)
    rgb[spill, 2] = np.maximum(rgb[spill, 0], rgb[spill, 1])
    return rgb, al


def side_of(px, py, a, b):
    """>0 nếu điểm nằm bên trái đường a->b (toạ độ ảnh, y xuống)."""
    return (b[0] - a[0]) * (py - a[1]) - (b[1] - a[1]) * (px - a[0])


def largest(al, thr=0.02):
    """Giữ khối liền lớn nhất (mẩu rời lơ lửng, vụn bỏ đi)."""
    m = (al > thr).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n <= 2:
        return al
    big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    return al * (lab == big)


def save(name, rgb, al, pad=6):
    ys, xs = np.where(al > 0.03)
    y0, y1 = max(0, ys.min() - pad), min(H, ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(W, xs.max() + pad + 1)
    out = np.dstack([rgb[y0:y1, x0:x1], al[y0:y1, x0:x1] * 255]).clip(0, 255).astype(np.uint8)
    Image.fromarray(out).save(os.path.join(IMG, name + ".png"))
    return {"left": int(x0), "top": int(y0), "w": int(x1 - x0), "h": int(y1 - y0)}


def main():
    rgb, al = load_rgba()
    yy, xx = np.mgrid[0:H, 0:W]
    lum = rgb.mean(2)
    sat = rgb.max(2) - rgb.min(2)
    solid = al > 0.5
    vis = al > 0.02
    geo = {"canvas": [W, H], "origin": list(ORIGIN), "J": J, "parts": {}}

    # --- bàn tay + cổ găng (kem) và mọi thứ ngoài thân ở hai bên dưới cổ găng: bỏ khỏi thân
    cream = (lum > 170) & (sat < 90)
    hands = vis & (yy > 845) & (yy < 1100) & ((xx < 300) | (xx > 724))
    # --- tay: phía ngoài đường cắt vai, trên mép cổ găng
    cutL = ((470, 572), (398, 660))
    cutR = ((556, 572), (628, 660))
    armL = vis & ~hands & (yy < 862) & (yy > 560) & (xx < 470) & (side_of(xx, yy, cutL[0], cutL[1]) > 0)
    armR = vis & ~hands & (yy < 862) & (yy > 560) & (xx > 556) & (side_of(xx, yy, cutR[0], cutR[1]) < 0)
    # bỏ phần cổ găng kem dính trên mép, và phần nơ đỏ (nơ ở y 530–620, nịt tay áo đỏ ở y 640–700)
    red = (rgb[..., 0] > 150) & (rgb[..., 0] > rgb[..., 1] + 50)
    for m in (armL, armR):
        m &= ~(cream & (yy > 840))
        m &= ~(red & (yy < 625))
    # phần tay đã tách hẳn khỏi thân (dưới y 650) thì bỏ khỏi thân; khớp vai giữ ở thân (đen chồng đen không lộ)
    armL_sep = armL & (yy > 650)
    armR_sep = armR & (yy > 650)

    # --- lưỡi trai: xanh lá, đai kem, nút vàng ở trên đầu
    green = (rgb[..., 1] > rgb[..., 0] + 25) & (rgb[..., 1] > rgb[..., 2] - 30) & (lum > 60)
    gold = (rgb[..., 0] > 180) & (rgb[..., 1] > 120) & (rgb[..., 2] < 110)
    visor = solid & (yy < 320) & (green | cream | gold)
    visor = cv2.morphologyEx(visor.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    visor = cv2.morphologyEx(visor, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(visor, 8)
    visor = np.isin(lab, [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 800])
    visor_soft = cv2.dilate(visor.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    visor_ring = cv2.dilate(visor.astype(np.uint8), np.ones((15, 15), np.uint8)) > 0

    # --- thân: còn lại; chỗ lưỡi trai che đầu / chỏm thì tô đen lấy vân đầu
    body_al = al.copy()
    body_al[hands | armL_sep | armR_sep] = 0
    body_rgb = rgb.copy()
    dark = solid & (lum < 90) & ~visor_soft
    head_zone = dark & (yy < 560)
    hull = cv2.convexHull(np.column_stack(np.where(head_zone))[:, ::-1].astype(np.int32))
    hull_mask = np.zeros((H, W), np.uint8)
    cv2.fillConvexPoly(hull_mask, hull, 1)
    # chỉ lấp phần lưỡi trai nằm trong khối đầu (nửa trái, nơi đai che đầu và gốc chỏm); vành lưỡi trai thò ra ngoài để trống
    fill = visor_ring & (hull_mask > 0) & (xx < 700) & ~((lum < 60) & ~visor_soft)
    src_y = np.clip(yy + 170, 0, H - 1)
    body_rgb[fill] = rgb[src_y[fill], xx[fill]]
    body_al[fill] = 1.0
    body_al[visor_soft & ~fill] = 0
    # vành quanh chỗ lưỡi trai cũ: điểm không đen (pha xanh lơ / xanh lá) bỏ đi
    body_al[visor_ring & ~fill & (lum > 85)] = 0
    # điểm pha xanh lơ còn sót ở mép (thân không có màu nào lục và lam cùng cao hơn đỏ nhiều)
    teal = (body_rgb[..., 1] - body_rgb[..., 0] > 50) & (body_rgb[..., 2] - body_rgb[..., 0] > 40)
    body_al[teal] = 0
    # sợi mảnh còn sót (viền mờ của tay, bàn tay): mở 5x5 rồi dựng lại vùng
    bm = (body_al > 0.02).astype(np.uint8)
    core = cv2.morphologyEx(bm, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    keep = cv2.dilate(core, np.ones((5, 5), np.uint8)) & bm
    body_al = largest(body_al * keep)
    # vụn nịt tay áo / viền vàng ở hai đầu vai (khớp vai giữ ở thân): bỏ điểm đỏ, vàng ở vùng vai
    shoulder = (yy > 600) & (yy < 720) & ((xx < 420) | (xx > 604))
    body_al[shoulder & (red | gold)] = 0
    geo["parts"]["than"] = save("than", body_rgb, body_al)
    geo["parts"]["luoi_trai"] = save("luoi_trai", rgb, al * visor_soft)
    geo["parts"]["tay_trai"] = save("tay_trai", rgb, largest(al * armL, 0.3))
    geo["parts"]["tay_phai"] = save("tay_phai", rgb, largest(al * armR, 0.3))

    # --- mắt, miệng: co theo đầu (bề ngang mắt ~ 0,62 đầu, miệng ~ 0,58 đầu); đầu rộng ~ 350 px
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
            im.save(os.path.join(IMG, f"{kind}_{i:02d}.png"))
            geo["parts"][f"{kind}_{i:02d}"] = {"w": im.width, "h": im.height}

    # --- bàn tay: co cho cổ găng bằng cổ găng ảnh gốc (~92 px); đo gốc cổ tay (cụm đen) và hướng tay
    h01 = Image.open(os.path.join(HERE, "manh", "tay_01.png")).height
    s_hand = 235.0 / h01
    geo["scale_hand"] = s_hand
    for i in range(1, 11):
        im = Image.open(os.path.join(HERE, "manh", f"tay_{i:02d}.png")).convert("RGBA")
        a = np.asarray(im).astype(float)
        aa = a[..., 3] > 128
        blk = (aa & (a[..., :3].mean(2) < 110)).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(blk, 8)
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        ys, xs = np.where(lab == big)
        sy, sx = ys.mean(), xs.mean()
        cy, cx = np.where(aa)
        cyy, cxx = cy.mean(), cx.mean()
        # bề rộng cụm đen vuông góc hướng tay ~ bề rộng cổ tay; cổ găng rộng hơn ~1,6 lần
        d = np.array([cxx - sx, cyy - sy])
        d /= np.linalg.norm(d) + 1e-9
        s = s_hand
        im2 = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
        im2.save(os.path.join(IMG, f"tay_{i:02d}.png"))
        # gốc = mép ngoài cụm đen (đầu cổ tay), tính theo ảnh đã co; hướng = gốc -> tâm
        along = (xs - sx) * d[0] + (ys - sy) * d[1]
        root = np.array([sx, sy]) + d * along.min()
        geo["parts"][f"tay_{i:02d}"] = {"w": im2.width, "h": im2.height, "goc": [float(root[0] * s), float(root[1] * s)],
                                        "huong": [float(d[0]), float(d[1])], "s": s}
    with open(os.path.join(ATOM, "geo.json"), "w", encoding="utf-8") as f:
        json.dump(geo, f, ensure_ascii=False, indent=1)
    print("đã ghi", len(geo["parts"]), "mảnh vào", IMG)
    for k in ("than", "luoi_trai", "tay_trai", "tay_phai"):
        print(k, geo["parts"][k])
    print("tỉ lệ mắt %.2f, miệng %.2f" % (s_eye, s_mouth))
    print("bàn tay:", [round(geo["parts"][f"tay_{i:02d}"]["s"], 2) for i in range(1, 11)])


if __name__ == "__main__":
    main()
