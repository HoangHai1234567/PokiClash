# Chuẩn bị mảnh để rig máy quả "Háu Ăn" trong AtomSpine. Đọc năm tờ gen không viền, nền hồng (cùng thư mục):
#   L1_goc.png   bản chuẩn cả con (chỉ để đo và so)          L2_than.png  thân trống (không mắt, mày, miệng, cần, lò xo, chân)
#   L3_chi.png   sao + lò xo, dải mày, cần + núm, hai chân    L4_mat.png   8 cặp mắt (2 cột x 4 hàng)
#   L5_mieng.png 6 miệng (3 cột x 2 hàng)
# Ghi ../atom/images/*.png và ../atom/geo.json (chỗ đặt trên khung 1024 x 1536, mốc khớp), soi/ghep_thu.png (ghép lại cạnh L1).
#   than        thân (một lưới)                 den_a_d/_h, den_b_d/_h  bóng đèn sáng (hai nhóm xen kẽ; _d trên vòm, _h ở cản dưới)
#   mat_01..08  trung tính, nhìn xuống, lồi, nhắm chặt, cười nhắm, chớp, buồn, mắt sao (co về cỡ mắt của L1)
#   mieng_01..06 cười, nghiến, rớt hàm, chữ o, mếu, cười to
#   may_t, may_p hai nửa dải mày                 can  cần + núm            lo_xo, sao  ăng ten
#   chan_t, chan_p ống chân DỰNG LẠI bằng mã (dải thẳng, hai đầu tròn, vân lấy từ ống chân gen)   giay_t, giay_p  cổ giày + giày
# Chạy: py -3 -I chuan_bi.py
import json, os, sys
import numpy as np
import cv2
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ATOM = os.path.abspath(os.path.join(HERE, "..", "atom"))
IMG = os.path.join(ATOM, "images")
SOI = os.path.join(HERE, "soi")
os.makedirs(IMG, exist_ok=True)
os.makedirs(SOI, exist_ok=True)
W, H = 1024, 1536
ORIGIN = (498, 1446)            # mặt đất giữa hai chân (đế giày y 1446; tâm ô cuộn x 500)
REEL = {"cols": [(275, 418), (433, 571), (588, 726)], "top": 605, "bot": 935}   # lòng ba cuộn (px L1 / L2)
BULBS = [(242, 400), (303, 311), (407, 262), (510, 250), (612, 262), (717, 311), (770, 400), (226, 1030), (770, 1030)]
LEG_X = {"t": 329, "p": 636}    # trục ống chân
LEG_W = 66                      # bề rộng ống chân
SOCKET_Y, ANKLE_Y = 1085, 1300  # gốc ống (trong thân) và cổ chân (trong cổ giày)


def bleed(rgb, solid, iters=10):
    """Loang màu vùng đặc ra ngoài (mép không còn ánh hồng của nền)."""
    rgb = rgb.copy()
    m = solid.astype(np.float32)
    for _ in range(iters):
        k = np.ones((3, 3), np.float32)
        num = cv2.filter2D(rgb * m[..., None], -1, k)
        den = cv2.filter2D(m, -1, k)
        new = (den > 0) & (m == 0)
        rgb[new] = num[new] / den[new][:, None]
        m[new] = 1
    return rgb


def fill_holes(mask):
    m = mask.astype(np.uint8)
    pad = cv2.copyMakeBorder(m, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    cv2.floodFill(pad, None, (0, 0), 2)
    return pad[1:-1, 1:-1] != 2


def key(name, holes=True):
    """Nền hồng -> alpha mềm; màu mép lấy từ phần đặc bên trong; lỗ kín bên trong coi là đặc (holes=False: giữ lỗ, vd. lòng lò xo)."""
    a = np.asarray(Image.open(os.path.join(HERE, name)).convert("RGB")).astype(np.float32)
    bg = np.median(a[:24, :24].reshape(-1, 3), axis=0)
    d = np.sqrt(((a - bg) ** 2).sum(2))
    al = np.clip((d - 70) / 50, 0, 1)
    if holes:
        hole = fill_holes(al > 0.5)
        al = np.where(hole & (al < 1), np.maximum(al, cv2.erode(hole.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(np.float32)), al)
    solid = cv2.erode((al > 0.97).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    rgb = bleed(a, solid)
    return rgb, al


def comps(al, dil=1, minarea=300):
    m = (al > 0.5).astype(np.uint8)
    if dil > 1:
        m = cv2.dilate(m, np.ones((dil, dil), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    return [(lab == i, st[i]) for i in range(1, n) if st[i, 4] >= minarea]


PARTS = {}


def save(name, rgb, al, left=None, top=None, pad=4):
    """Cắt sát, lưu RGBA; ghi chỗ đặt (left, top) trên khung 1024 x 1536 nếu có."""
    ys, xs = np.where(al > 0.03)
    y0, y1 = max(0, ys.min() - pad), min(al.shape[0], ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(al.shape[1], xs.max() + pad + 1)
    out = np.dstack([rgb[y0:y1, x0:x1], al[y0:y1, x0:x1] * 255]).clip(0, 255).astype(np.uint8)
    Image.fromarray(out).save(os.path.join(IMG, name + ".png"))
    PARTS[name] = {"left": int(x0 if left is None else left + x0), "top": int(y0 if top is None else top + y0), "w": int(x1 - x0), "h": int(y1 - y0)}
    return out


def resize(rgb, al, k):
    h, w = al.shape
    nw, nh = max(1, round(w * k)), max(1, round(h * k))
    pre = np.dstack([rgb * al[..., None], al]).astype(np.float32)
    r = cv2.resize(pre, (nw, nh), interpolation=cv2.INTER_AREA if k < 1 else cv2.INTER_CUBIC)
    a = np.clip(r[..., 3], 0, 1)
    c = np.where(a[..., None] > 1e-3, r[..., :3] / np.maximum(a[..., None], 1e-3), 0)
    return bleed(c.astype(np.float32), a > 0.9, 4), a


def main():
    geo = {"canvas": [W, H], "origin": list(ORIGIN), "reel": REEL, "leg_x": LEG_X, "socket_y": SOCKET_Y, "ankle_y": ANKLE_Y, "leg_w": LEG_W}
    l1, a1 = key("L1_goc.png")
    # ---------- thân + đèn ----------
    rgb, al = key("L2_than.png")
    save("than", rgb, al)
    yy, xx = np.mgrid[0:H, 0:W]
    yellow = (rgb[..., 0] > 215) & (rgb[..., 1] > 170) & (rgb[..., 2] < 120) & (al > 0.5)
    bulbs = []
    for grp in (0, 1):
        m_all = np.zeros((H, W), bool)
        for i, (bx, by) in enumerate(BULBS):
            if i % 2 != grp:
                continue
            near = ((xx - bx) ** 2 + (yy - by) ** 2) < 46 ** 2
            n, lab, st, ce = cv2.connectedComponentsWithStats((yellow & near).astype(np.uint8), 8)
            big = 1 + int(np.argmax(st[1:, 4]))
            m = lab == big
            m_all |= m
            bulbs.append((i, float(ce[big][0]), float(ce[big][1]), int(st[big, 4])))
        lit = rgb * 0.38 + np.array([255, 251, 214], np.float32) * 0.62
        a_l = cv2.GaussianBlur(m_all.astype(np.float32), (0, 0), 0.8)
        # mỗi nhóm hai ảnh: đèn trên vòm (bám cứng khối đầu) và đèn ở cản dưới (bám cứng khối hông): trùng khít với lưới thân
        nm = "den_a" if grp == 0 else "den_b"
        save(nm + "_d", lit, a_l * (al > 0.5) * (yy < 700))
        save(nm + "_h", lit, a_l * (al > 0.5) * (yy >= 700))
    geo["bulbs"] = sorted(bulbs)
    # ---------- chi rời (L3) ----------
    rgb3, al3 = key("L3_chi.png", holes=False)
    cs = sorted(comps(al3), key=lambda c: (c[1][1] // 200, c[1][0]))
    names = ["sao_lo_xo", "may", "can", "chan_t", "chan_p"]
    assert len(cs) == 5, [c[1].tolist() for c in cs]
    C = {n: (m, st) for n, (m, st) in zip(names, cs)}
    # sao (vàng) / lò xo (nâu sẫm)
    m, st = C["sao_lo_xo"]
    lum = rgb3.mean(2)
    is_star = (rgb3[..., 0] > 190) & (rgb3[..., 1] > 150)
    is_star = cv2.morphologyEx(is_star.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)) > 0
    star_m = cv2.dilate((is_star & m).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    # màu của mỗi mảnh loang từ chính nó (không lẫn màu mảnh kia ở mép chung)
    save("sao", bleed(rgb3, is_star & m & (al3 > 0.97), 6), al3 * star_m * m)
    spring_m = m & ~is_star
    save("lo_xo", bleed(rgb3, spring_m & (al3 > 0.97) & (lum < 120), 6), al3 * cv2.GaussianBlur(spring_m.astype(np.float32), (0, 0), 0.7))
    # dải mày: hai nửa, mỗi nửa lấn qua giữa 12 px
    m, st = C["may"]
    xs = np.where(m.any(0))[0]
    ys_mid = np.where(m[:, 500:514].any(1))[0]
    xc = 506
    geo["may"] = {"x0": int(xs.min()), "x1": int(xs.max()), "xc": xc, "dip_y": int(ys_mid.max())}
    save("may_t", rgb3, al3 * m * (xx < xc + 12))
    save("may_p", rgb3, al3 * m * (xx >= xc - 12))
    # cần + núm
    m, st = C["can"]
    save("can", rgb3, al3 * m)
    red = m & (rgb3[..., 0] > 170) & (rgb3[..., 1] < 110)
    ys, xs = np.where(red)
    geo["num"] = {"cx": float(xs.mean()), "cy": float(ys.mean()), "r": float((xs.max() - xs.min() + ys.max() - ys.min()) / 4)}
    gold = m & ~red & (al3 > 0.5)
    ys, xs = np.where(gold)
    lo = ys > ys.max() - 14
    geo["can_duoi"] = [float(xs[lo].mean()), float(ys.max() - 14)]
    # chân: giày + cổ giày (mảnh thật), ống chân dựng lại
    for s in ("t", "p"):
        m, st = C["chan_" + s]
        x0, y0, w, h = st[:4]
        cx = LEG_X[s]
        tube = m & (np.abs(xx - cx) < LEG_W / 2 + 4) & (lum < 105) & (yy < 1300)
        shoe = m & (yy > 1262) & ~cv2.dilate(tube.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
        shoe = cv2.morphologyEx(shoe.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0
        n, lab, stt, _ = cv2.connectedComponentsWithStats(shoe.astype(np.uint8), 8)
        shoe = lab == (1 + int(np.argmax(stt[1:, 4])))
        shoe = fill_holes(shoe)
        # chỗ ống chân cắm vào cổ giày: lấp kín bằng màu kem (bao lồi của cổ giày); ống chân vẽ SAU giày nên nghiêng không lộ khe
        cuff = shoe & (rgb3[..., 0] > 220) & (rgb3[..., 2] > 150)
        pts = cv2.findNonZero(cuff.astype(np.uint8))
        hull = np.zeros((H, W), np.uint8)
        cv2.fillConvexPoly(hull, cv2.convexHull(pts), 1)
        shoe = shoe | (hull > 0)
        col = bleed(np.where(tube[..., None], 0, rgb3), cuff | (shoe & ~tube & (al3 > 0.97)), 40)
        save("giay_" + s, col, cv2.GaussianBlur(shoe.astype(np.float32), (0, 0), 0.8))
        ys, xs = np.where(cuff)
        geo["co_giay_" + s] = [float(xs.mean()), float(ys.min()), float(ys.max())]
        ys, xs = np.where(shoe)
        geo["giay_" + s] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
        # ống: dải thẳng, vân từ đoạn ống sạch (y 940..1250)
        tex = rgb3[940:1250, cx - LEG_W // 2:cx + LEG_W // 2]
        Lt = ANKLE_Y - SOCKET_Y
        hh, ww = Lt + LEG_W, LEG_W + 2
        img = np.zeros((hh, ww, 3), np.float32)
        for y in range(hh):
            img[y, 1:1 + LEG_W] = tex[(y * 7 + (40 if s == "p" else 0)) % tex.shape[0] if False else y % tex.shape[0]]
        img[:, 0] = img[:, 1]
        img[:, -1] = img[:, -2]
        gy, gx = np.mgrid[0:hh, 0:ww]
        r = LEG_W / 2
        cxm = ww / 2 - 0.5
        dcap = np.where(gy < r, np.hypot(gx - cxm, gy - r), np.where(gy > hh - 1 - r, np.hypot(gx - cxm, gy - (hh - 1 - r)), np.abs(gx - cxm)))
        a_t = np.clip(r - dcap + 0.5, 0, 1)
        out = np.dstack([img, a_t * 255]).clip(0, 255).astype(np.uint8)
        Image.fromarray(out).save(os.path.join(IMG, f"chan_{s}.png"))
        PARTS[f"chan_{s}"] = {"left": int(cx - ww / 2), "top": int(SOCKET_Y - r), "w": ww, "h": hh}
    # ---------- mắt (L4) ----------
    rgb4, al4 = key("L4_mat.png")
    cs = comps(al4, dil=9, minarea=3000)
    cs = sorted(cs, key=lambda c: ((c[1][1] + c[1][3] / 2) // 384, c[1][0]))
    assert len(cs) == 8, len(cs)
    # mắt L1: mép trái, phải, đáy của vùng mắt (L1 khác L2, dưới dải mày)
    rgb2, al2 = key("L2_than.png")
    diff = (np.abs(l1 - rgb2).sum(2) > 90) & (yy > 440) & (yy < 580) & (xx > 300) & (xx < 720)
    diff = cv2.morphologyEx(diff.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)) > 0
    ys, xs = np.where(diff)
    ex0, ex1, ey1 = int(xs.min()), int(xs.max()), int(ys.max())
    w_ref = cs[0][1][2] - 8   # bề rộng cặp mắt trung tính trên tờ (bỏ phần nới)
    k_eye = (ex1 - ex0) / w_ref * 0.93   # nhỏ hơn L1 chút: đỉnh mắt nằm gọn dưới dải mày
    geo["mat_l1"] = [ex0, ex1, ey1]
    geo["k_eye"] = round(k_eye, 4)
    sizes = []
    for i, (m, st) in enumerate(cs, 1):
        mm = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
        x0, y0, w, h = st[:4]
        c, a = resize(rgb4[y0:y0 + h, x0:x0 + w], (al4 * mm)[y0:y0 + h, x0:x0 + w], k_eye)
        out = save(f"mat_{i:02d}", c, a)
        sizes.append(out.shape[:2])
    geo["mat"] = {"cx": (ex0 + ex1) / 2, "cy": ey1 + 6 - (sizes[0][0] - 8) / 2}   # tâm cặp mắt (đáy thấp hơn L1 6 px)
    # ---------- miệng (L5) ----------
    rgb5, al5 = key("L5_mieng.png")
    cs = comps(al5, dil=5, minarea=3000)
    cs = sorted(cs, key=lambda c: ((c[1][1] + c[1][3] / 2) // 512, c[1][0]))
    assert len(cs) == 6, len(cs)
    diff = (np.abs(l1 - rgb2).sum(2) > 90) & (yy > 945) & (xx > 200) & (xx < 800) & (yy < 1200) & ~(np.abs(xx - 329) < 40) & ~(np.abs(xx - 636) < 40)
    diff = cv2.morphologyEx(diff.astype(np.uint8), cv2.MORPH_OPEN, np.ones((7, 7), np.uint8)) > 0
    ys, xs = np.where(diff)
    geo["mieng_l1"] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    geo["mieng"] = {"cx": ORIGIN[0], "top": 953}   # mép trên vành môi (nằm đè lên thanh dưới của khung cuộn, răng trùng răng L1)
    for i, (m, st) in enumerate(cs, 1):
        mm = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
        x0, y0, w, h = st[:4]
        save(f"mieng_{i:02d}", rgb5[y0:y0 + h, x0:x0 + w], (al5 * mm)[y0:y0 + h, x0:x0 + w])
    geo["parts"] = PARTS
    json.dump(geo, open(os.path.join(ATOM, "geo.json"), "w", encoding="utf-8"), indent=1)
    for k in ("mat_l1", "k_eye", "mat", "mieng_l1", "may", "num", "can_duoi", "co_giay_t", "co_giay_p", "giay_t", "giay_p"):
        print(k, geo[k])
    for k, v in PARTS.items():
        print(f"  {k:10s} {v}")


if __name__ == "__main__":
    main()
