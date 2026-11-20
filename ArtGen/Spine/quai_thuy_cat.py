# -*- coding: utf-8 -*-
"""Quái đảo Thủy (tôm tít đấm bốc, thay con cua xanh): cắt concept một ảnh thành mảnh để rig bằng AtomSpine (2026-11-20).

    py -3 -I ArtGen/Spine/quai_thuy_cat.py o      # tách ô màu phẳng giữa nét mực, ghi ảnh đánh số + o_cells.json
    py -3 -I ArtGen/Spine/quai_thuy_cat.py cat    # gom ô theo PARTS, vẽ bù phần bị che, ghi mảnh vào atom/images + parts.json

Concept: inbox/quai_thuy/tai_ve/L1.png (1536x1024, nền trắng). Ô = vùng không phải mực, nối 4 hướng; mực chia cho ô gần nhất.
"""
import json
import os
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "inbox", "quai_thuy", "tai_ve", "L1.png")
OUT = os.path.join(HERE, "quai_thuy")
INK_LUMA = 95      # điểm tối hơn mức này là mực
MIN_CELL = 60      # ô nhỏ hơn (điểm) gộp vào mực rồi chia cho ô kề


def load():
    img = cv2.cvtColor(cv2.imread(SRC, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]
    luma = img @ np.array([0.299, 0.587, 0.114])
    white = (img.min(axis=2) > 236)
    # nền = vùng trắng nối với mép ảnh
    n, lab = cv2.connectedComponents(white.astype(np.uint8), connectivity=4)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(edge)) & white
    fg = ~bg
    ink = fg & (luma < INK_LUMA)
    return img, fg, ink


def cells(fg, ink):
    inner = (fg & ~ink).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(inner, connectivity=4)
    keep = np.zeros(n, bool)
    keep[1:] = st[1:, cv2.CC_STAT_AREA] >= MIN_CELL
    lab = np.where(keep[lab], lab, 0)
    # mọi điểm fg còn lại (mực, ô vụn) gán cho ô gần nhất
    src = (lab == 0).astype(np.uint8)
    dist, near = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    # near: nhãn điểm 0 gần nhất -> lấy nhãn ô tại điểm đó
    ys, xs = np.nonzero(lab)
    pix_lab = np.zeros(near.max() + 1, np.int32)
    zero_pts = np.argwhere(src == 0)  # các điểm thuộc ô
    # distanceTransformWithLabels đánh số theo thứ tự quét các điểm 0 của src (= điểm thuộc ô)
    pix_lab[1:len(zero_pts) + 1] = lab[zero_pts[:, 0], zero_pts[:, 1]]
    own = np.where(lab > 0, lab, pix_lab[near])
    own[~fg] = 0
    return lab, own, keep


def cmd_o():
    os.makedirs(OUT, exist_ok=True)
    img, fg, ink = load()
    lab, own, keep = cells(fg, ink)
    ids = [i for i in range(len(keep)) if keep[i]]
    info = []
    vis = img.copy()
    rng = np.random.default_rng(3)
    for i in ids:
        m = lab == i
        ys, xs = np.nonzero(m)
        col = img[m].mean(axis=0)
        info.append({"id": int(i), "area": int(m.sum()), "cx": int(xs.mean()), "cy": int(ys.mean()),
                     "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                     "rgb": [int(c) for c in col]})
        tint = rng.integers(60, 255, 3)
        vis[m] = (0.55 * vis[m] + 0.45 * tint).astype(np.uint8)
    for c in info:
        s = str(c["id"])
        cv2.putText(vis, s, (c["cx"] - 8 * len(s), c["cy"] + 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(vis, s, (c["cx"] - 8 * len(s), c["cy"] + 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imwrite(os.path.join(OUT, "o_cells.png"), cv2.cvtColor(vis, cv2.COLOR_RGB2BGR))
    json.dump(info, open(os.path.join(OUT, "o_cells.json"), "w"), indent=0)
    print(f"{len(info)} ô; fg {int(fg.sum())} px; ảnh {os.path.join(OUT, 'o_cells.png')}")


# Gốc toạ độ rig (điểm ảnh concept): giữa bốn chân, mặt đất dưới bàn chân. x thế giới = px - OX, y = OY - py.
OX, OY = 720, 950

# Bộ phận theo thứ tự vẽ sau → trước: tên, các ô (số ở o_cells.png), cách vẽ bù phần bị che
#   "hull": bù phần nằm trong bao lồi của mảnh mà bị mảnh vẽ sau che (thân); ("hull", tên...): thêm vùng các mảnh vẽ
#   trước có tên đó đè lên (râu trước đè lên mép đầu)
#   ("disk", x, y, r): bù hình tròn tâm (x,y) bán kính r chỗ bị mảnh vẽ sau che (gốc càng, gốc râu)
#   ("up", h): kéo dài phần trên của mảnh lên h điểm dưới mảnh vẽ sau (đỉnh chân dưới bụng)
PARTS = [
    ("rau_sau", [21], [("disk", 790, 182, 16)]),
    ("rau_truoc", ["ANT"], [("disk", 742, 352, 16)]),
    ("vay_trai", [888, 1233], [("disk", 735, 345, 14)]),
    ("vay_phai", [1214], [("disk", 1000, 338, 12)]),
    ("cang_xa_bap", [1678], [("disk", 975, 598, 34)]),
    ("cang_xa_cang", [1333], []),
    ("cang_xa_chuy", [1210, 686], []),
    ("quat", [2182, 2293, 2391, 2314], []),
    ("duoi2", [2124, 2237], []),
    ("duoi1", [2033], []),
    ("chan3", [2260, 2568], [("up", 30)]),
    ("chan4", [2247, 2551], [("up", 30)]),
    ("chan1", [2240, 2561], [("up", 30)]),
    ("chan2", [2266, 2588], [("up", 30)]),
    ("than", [1507, 1894, 1508, 2013, 2082, 2189, 2177, 2249, 2262, 1861], ["hull"]),
    ("dau", ["HEAD", 1492, 1585, 1590], [("hull", "rau_truoc")]),
    ("mat_sau", [1118, 513, 367, 793], [("disk", 812, 338, 14)]),
    ("mat_truoc", [1046, 326, 514, 596], [("disk", 948, 330, 14)]),
    ("cang_gan_vai", [1763, 1930], []),
    ("cang_gan_co", [2008], []),
    ("cang_gan_chuy", [1952, 1814], []),
]
INK_W = 7          # bề dày viền mực kẻ lại ở chỗ vẽ bù (điểm ảnh concept)


def split_antenna(lab):
    """ô 240 = đầu + râu trước (không có nét mực ngăn): mở hình thái bỏ râu mảnh; râu = khối dài nhất của phần bị bỏ nằm
    bên trái gốc râu, các mẩu vụn khác (mỏm mũi mảnh) trả lại cho đầu."""
    m = (lab == 240).astype(np.uint8)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))
    opened = cv2.morphologyEx(m, cv2.MORPH_OPEN, k)
    rest = ((m == 1) & (opened == 0)).astype(np.uint8)
    n, cl, st, cen = cv2.connectedComponentsWithStats(rest, connectivity=8)
    best, best_a = 0, 0
    for i in range(1, n):
        if cen[i][0] < 745 and st[i, cv2.CC_STAT_AREA] > best_a:
            best, best_a = i, st[i, cv2.CC_STAT_AREA]
    ant = cl == best
    head = (m == 1) & ~ant
    return head, ant


def textures(img, lab, ids_masks):
    """mẫu vân 32x32 lấy trong lòng từng ô (để tô bù có vân sáp, không kéo vệt); ô nhỏ quá thì màu trung vị phẳng."""
    tex = {}
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 35))
    for key, cm in ids_masks.items():
        er = cv2.erode(cm.astype(np.uint8), k)
        ys, xs = np.nonzero(er)
        if len(ys):
            cy, cx = np.nonzero(cm)
            j = int(np.argmin((ys - cy.mean()) ** 2 + (xs - cx.mean()) ** 2))
            y, x = ys[j], xs[j]
            tex[key] = img[y - 16:y + 16, x - 16:x + 16].copy()
        else:
            med = np.median(img[cm], axis=0).astype(np.uint8)
            tex[key] = np.tile(med, (32, 32, 1))
    return tex


def cmd_cat():
    img, fg, ink = load()
    lab, own, keep = cells(fg, ink)
    head_m, ant_m = split_antenna(lab)
    ink_rgb = np.median(img[ink], axis=0).astype(np.uint8)
    # vùng "của" từng ô (gồm mực chia cho ô gần nhất); râu / đầu tách từ ô 240
    own_head = (own == 240)
    # mực của ô 240: điểm mực gần râu hơn thì thuộc râu
    d_ant = cv2.distanceTransform((~ant_m).astype(np.uint8), cv2.DIST_L2, 5)
    d_head = cv2.distanceTransform((~head_m).astype(np.uint8), cv2.DIST_L2, 5)
    own_ant = own_head & (d_ant < d_head)
    own_head = own_head & ~own_ant
    h, w = lab.shape

    def cell_mask(i):
        return ant_m if i == "ANT" else head_m if i == "HEAD" else lab == i

    ring_k = np.ones((2 * INK_W + 1, 2 * INK_W + 1), np.uint8)

    def mask_of(ids):
        m = np.zeros((h, w), bool)
        c = np.zeros((h, w), bool)
        for i in ids:
            m |= own_ant if i == "ANT" else own_head if i == "HEAD" else own == i
            c |= cell_mask(i)
        # trọn vòng mực quanh ô của mảnh (mực ở chỗ giáp mảnh khác cũng thuộc mảnh này)
        m |= cv2.dilate(c.astype(np.uint8), ring_k).astype(bool) & ink
        return m

    masks = {name: mask_of(ids) for name, ids, _ in PARTS}
    all_ids = [i for _, ids, _ in PARTS for i in ids]
    tex = textures(img, lab, {i: cell_mask(i) & ~ink for i in all_ids})
    names = [p[0] for p in PARTS]
    os.makedirs(os.path.join(OUT, "atom", "images"), exist_ok=True)
    info = []
    for k, (name, ids, fills) in enumerate(PARTS):
        m = masks[name].copy()
        front = np.zeros((h, w), bool)
        for later in names[k + 1:]:
            front |= masks[later]
        add = np.zeros((h, w), bool)
        for f in fills:
            if f == "hull" or f[0] == "hull":
                pts = cv2.findNonZero(m.astype(np.uint8))
                hull = np.zeros((h, w), np.uint8)
                cv2.fillConvexPoly(hull, cv2.convexHull(pts), 1)
                over = front.copy()
                if f != "hull":
                    for other in f[1:]:
                        over |= masks[other]
                cand = (hull > 0) & over & ~m
                # bo tròn: làm mờ hình (mảnh + vùng bù) rồi lấy ngưỡng, bỏ cạnh thẳng của bao lồi
                full = (m | cand).astype(np.float32)
                sm = cv2.GaussianBlur(full, (0, 0), 18) > 0.5
                add |= cand & sm
            elif f[0] == "disk":
                d = np.zeros((h, w), np.uint8)
                cv2.circle(d, (f[1], f[2]), f[3], 1, -1)
                add |= (d > 0) & front & ~m
            elif f[0] == "up":
                ys, xs = np.nonzero(m)
                top = ys.min()
                band = m[top:top + 12]                       # 12 hàng trên cùng của mảnh
                cols = np.nonzero(band.any(axis=0))[0]
                ext = np.zeros((h, w), bool)
                ext[max(0, top - f[1]):top + 12, cols.min():cols.max() + 1] = True
                add |= ext & front & ~m
        rgba = np.zeros((h, w, 4), np.uint8)
        rgba[m, :3] = img[m]
        rgba[m, 3] = 255
        if add.any():
            # tô bù: ô gần nhất của mảnh, lát mẫu vân của ô đó (màu phẳng có vân sáp)
            idmap = np.zeros((h, w), np.int32)
            keys = list(ids)
            for j, i in enumerate(keys):
                idmap[cell_mask(i) & ~ink] = j + 1
            src = (idmap == 0).astype(np.uint8)
            _, near = cv2.distanceTransformWithLabels(src, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            zp = np.argwhere(src == 0)
            lut = np.zeros(near.max() + 1, np.int32)
            lut[1:len(zp) + 1] = idmap[zp[:, 0], zp[:, 1]]
            which = lut[near]
            ys, xs = np.nonzero(add)
            for j, i in enumerate(keys):
                sel = which[ys, xs] == j + 1
                t = tex[i]
                rgba[ys[sel], xs[sel], :3] = t[ys[sel] % 32, xs[sel] % 32]
            rgba[add, 3] = 255
            # đường ranh giữa hai ô khác nhau trong vùng bù (nối tiếp các đường đốt / mép tấm giáp), nét mảnh
            wm = np.zeros((h, w), np.int32)
            wm[ys, xs] = which[ys, xs]
            gx = np.zeros((h, w), bool)
            gx[:, 1:] |= (wm[:, 1:] != wm[:, :-1]) & (wm[:, 1:] > 0) & (wm[:, :-1] > 0)
            gx[1:, :] |= (wm[1:, :] != wm[:-1, :]) & (wm[1:, :] > 0) & (wm[:-1, :] > 0)
            seam = cv2.dilate(gx.astype(np.uint8), np.ones((4, 4), np.uint8)).astype(bool) & add
            rgba[seam, :3] = ink_rgb
            # viền mực mới: mép của mảnh mở rộng nằm trong vùng bù
            full = (m | add).astype(np.uint8)
            inner = cv2.erode(full, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (INK_W, INK_W)))
            edge = (full > 0) & (inner == 0) & cv2.dilate(add.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
            rgba[edge, :3] = ink_rgb
            rgba[edge, 3] = 255
        a = rgba[:, :, 3] > 0
        ys, xs = np.nonzero(a)
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        crop = rgba[y0:y1, x0:x1]
        cv2.imwrite(os.path.join(OUT, "atom", "images", name + ".png"), cv2.cvtColor(crop, cv2.COLOR_RGBA2BGRA))
        info.append({"name": name, "at": [int(x0), int(y0)], "size": [int(x1 - x0), int(y1 - y0)],
                     "added": int(add.sum())})
    json.dump({"canvas": [w, h], "origin": [OX, OY], "parts": info}, open(os.path.join(OUT, "parts.json"), "w"), indent=1)
    # kiểm: ghép lại theo thứ tự vẽ phải ra đúng concept (trừ chỗ vẽ bù bị che)
    comp = np.full((h, w, 3), 255, np.uint8)
    for p in info:
        im = cv2.cvtColor(cv2.imread(os.path.join(OUT, "atom", "images", p["name"] + ".png"), cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA)
        x0, y0 = p["at"]
        hh, ww = im.shape[:2]
        al = im[:, :, 3:4] / 255.0
        comp[y0:y0 + hh, x0:x0 + ww] = (comp[y0:y0 + hh, x0:x0 + ww] * (1 - al) + im[:, :, :3] * al).astype(np.uint8)
    diff = np.abs(comp.astype(int) - np.where(fg[..., None], img, 255).astype(int)).max(axis=2)
    cv2.imwrite(os.path.join(OUT, "ghep_lai.png"), cv2.cvtColor(comp, cv2.COLOR_RGB2BGR))
    print(f"{len(info)} mảnh -> {os.path.join(OUT, 'atom', 'images')}; lệch ghép lại >40: {int((diff > 40).sum())} px")
    for p in info:
        print(f"  {p['name']:<14} at={p['at'][0]},{p['at'][1]} {p['size'][0]}x{p['size'][1]} bù {p['added']}")


if __name__ == "__main__":
    {"o": cmd_o, "cat": cmd_cat}[sys.argv[1]]()
