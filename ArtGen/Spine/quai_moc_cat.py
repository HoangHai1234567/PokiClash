# -*- coding: utf-8 -*-
"""Quái đảo Mộc (sóc dẻ gai, thay Bọ Sừng): cắt concept một ảnh thành mảnh để rig bằng AtomSpine (2026-11-20).

    py -3 -I ArtGen/Spine/quai_moc_cat.py o      # tách ô màu phẳng giữa nét mực, ghi ảnh đánh số + o_cells.json
    py -3 -I ArtGen/Spine/quai_moc_cat.py cat    # gom ô theo PARTS, vẽ bù phần bị che, ghi mảnh vào atom/images + parts.json

Concept: inbox/quai_moc/tai_ve/L1.png (1536x1024, nền trắng). Ô = vùng không phải mực, nối 4 hướng; mực chia cho ô gần nhất.
"""
import json
import os
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "inbox", "quai_moc", "tai_ve", "L1.png")
OUT = os.path.join(HERE, "quai_moc")
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
    # lỗ trắng lớn bị kẹp giữa đuôi, đầu, thân (ô 632) cũng là nền
    for i in range(1, n):
        if i not in edge and (lab == i).sum() > 5000:
            bg |= (lab == i)
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
OX, OY = 790, 945

# Bộ phận theo thứ tự vẽ sau → trước: tên, các ô (số ở o_cells.png), cách vẽ bù phần bị che
#   "hull": bù phần nằm trong bao lồi của mảnh mà bị mảnh vẽ sau che (thân); ("hull", tên...): thêm vùng các mảnh vẽ
#   trước có tên đó đè lên (râu trước đè lên mép đầu)
#   ("disk", x, y, r): bù hình tròn tâm (x,y) bán kính r chỗ bị mảnh vẽ sau che (gốc càng, gốc râu)
#   ("up", h): kéo dài phần trên của mảnh lên h điểm dưới mảnh vẽ sau (đỉnh chân dưới bụng)
# bàn chân gần tách khỏi ô thân 1437 bằng đa giác (không có nét mực giữa đùi và bàn chân)
FOOT_POLY = np.array([(470, 872), (555, 862), (690, 856), (699, 859), (699, 960), (470, 960)], np.int32)
PARTS = [
    ("duoi3", [187], ["hull"]),
    ("duoi2", [656], ["hull"]),
    ("duoi1", [1238, 1246], ["hull"]),
    ("tay_xa", [1193], [("disk", 1008, 628, 30)]),
    ("nam_xa", [996, 1016], []),
    ("chan_xa", [1704], [("ell", 958, 818, 52, 24)]),
    ("than", ["BODY"], ["hull", ("rect", 560, 846, 699, 884), ("ell", 775, 745, 245, 178)]),
    ("chan_gan", ["FOOT"], []),
    ("dau", [633, 711, 781, 759, 745, 962, 955, 963], ["hull"]),
    ("tay_gan", [1278], []),
    ("mu", [20, 796], ["hull"]),
    ("tai_trai", [443, 522], []),
    ("tai_phai", [518, 554], []),
]
FILL_SRC = {"dau": [633]}   # ô làm nguồn màu tô bù (bỏ ô nhỏ mắt, miệng, răng)
ERASE_OLD_INK = {"than", "dau"}   # mảnh mà nét mực cũ ở ranh với mảnh trước nay nằm trong phần bù: xoá
RING_W = 11        # vòng mực quanh ô lấy vào mảnh: đủ dày để mảnh trước phủ trọn nét chung (mảnh sau xoá nét cũ)
INK_W = 7          # bề dày viền mực kẻ lại ở chỗ vẽ bù (điểm ảnh concept)


def split_foot(lab):
    """ô 1437 = thân + đùi + bàn chân gần: bàn chân = phần nằm trong FOOT_POLY."""
    poly = np.zeros(lab.shape, np.uint8)
    cv2.fillPoly(poly, [FOOT_POLY], 1)
    m = lab == 1437
    return m & (poly == 0), m & (poly > 0), poly > 0


def subcells(img, cm, min_frac=0.08, min_d=28.0):
    """ô nhiều màu không có nét mực ngăn (thân nâu + bụng kem): tách theo cụm màu (k-means 2 trên Lab, làm mịn nhãn), trả danh
    sách mặt nạ con; ô một màu trả [cm]."""
    ys, xs = np.nonzero(cm)
    if len(ys) < 400:
        return [cm]
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB).astype(np.float32)
    px = lab[ys, xs]
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
    _, lb, cen = cv2.kmeans(px, 2, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    lb = lb.ravel()
    if np.linalg.norm(cen[0] - cen[1]) < min_d or min((lb == 0).mean(), (lb == 1).mean()) < min_frac:
        return [cm]
    L = np.zeros(cm.shape, np.uint8)
    L[ys, xs] = lb + 1
    L = cv2.medianBlur(L, 15)
    out = []
    ke = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    for k in (1, 2):
        m = cv2.morphologyEx(((L == k) & cm).astype(np.uint8), cv2.MORPH_OPEN, ke)
        n, cl, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
        m = np.isin(cl, [j for j in range(1, n) if st[j, cv2.CC_STAT_AREA] >= 1500])
        if m.sum() > 200:
            out.append(m)
    return out if len(out) == 2 else [cm]


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
    body_m, foot_m, poly = split_foot(lab)
    ink_rgb = np.median(img[ink], axis=0).astype(np.uint8)
    own_body = (own == 1437) & ~poly
    own_foot = (own == 1437) & poly
    h, w = lab.shape

    def cell_mask(i):
        return foot_m if i == "FOOT" else body_m if i == "BODY" else lab == i

    ring_k = np.ones((2 * RING_W + 1, 2 * RING_W + 1), np.uint8)

    def fill_holes(b):
        f = b.astype(np.uint8).copy()
        ff = np.zeros((h + 2, w + 2), np.uint8)
        inv = (1 - f).astype(np.uint8)
        cv2.floodFill(inv, ff, (0, 0), 2)
        return (f > 0) | (inv == 1)

    # chủ của từng điểm mực: mảnh vẽ trên cùng mà bóng kín (ô + viền, lấp lỗ) chứa nó; ngoài mọi bóng thì theo ô gần nhất
    solids = {}
    for name, ids, _ in PARTS:
        c = np.zeros((h, w), bool)
        for i in ids:
            c |= cell_mask(i)
        solids[name] = fill_holes(cv2.dilate(c.astype(np.uint8), ring_k).astype(bool))
    ink_owner = np.full((h, w), -1, np.int32)
    for k, (name, _, _) in enumerate(PARTS):
        ink_owner[solids[name] & ink] = k

    def mask_of(ids):
        k = next(n for n, p in enumerate(PARTS) if p[1] is ids)
        m = np.zeros((h, w), bool)
        c = np.zeros((h, w), bool)
        for i in ids:
            m |= own_foot if i == "FOOT" else own_body if i == "BODY" else own == i
            c |= cell_mask(i)
        m &= ~ink | (ink_owner == k) | (ink_owner < 0)
        # trọn vòng mực quanh ô của mảnh (mực ở chỗ giáp mảnh khác cũng thuộc mảnh này); thân / bàn chân không lấn qua đường cắt
        ring = cv2.dilate(c.astype(np.uint8), ring_k).astype(bool) & ink
        if "FOOT" in ids:
            ring &= poly
        elif "BODY" in ids:
            ring &= ~poly
        m |= ring
        return m

    masks = {name: mask_of(ids) for name, ids, _ in PARTS}
    all_ids = [i for _, ids, _ in PARTS for i in ids]
    sub = {}
    for i in all_ids:
        for j, sm in enumerate(subcells(img, cell_mask(i) & ~ink)):
            sub[(i, j)] = sm
    tex = textures(img, lab, sub)
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
            elif f[0] == "ell":
                e = np.zeros((h, w), np.uint8)
                cv2.ellipse(e, (f[1], f[2]), (f[3], f[4]), 0, 0, 360, 1, -1)
                add |= (e > 0) & front & ~m
            elif f[0] == "rect":
                r = np.zeros((h, w), bool)
                r[f[2]:f[4], f[1]:f[3]] = True
                add |= r & front & ~m
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
            keys = [k for k in sub if k[0] in FILL_SRC.get(name, ids)]
            for j, i in enumerate(keys):
                idmap[sub[i]] = j + 1
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
            cell_no = {i: n + 1 for n, i in enumerate(dict.fromkeys(k[0] for k in keys))}
            lut_cell = np.array([0] + [cell_no[k[0]] for k in keys], np.int32)
            wm[ys, xs] = lut_cell[which[ys, xs]]
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
            if name in ERASE_OLD_INK:
                inner2 = cv2.erode(full, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (INK_W + 6, INK_W + 6)))
                near_add = cv2.dilate(add.astype(np.uint8), np.ones((2 * INK_W + 5, 2 * INK_W + 5), np.uint8)).astype(bool)
                old = m & ink & near_add & (inner2 > 0)
                # cả viền khử răng cưa sáng quanh nét cũ (không phải lòng ô): xoá theo, không để lại vệt sáng mờ
                core = np.zeros((h, w), bool)
                for i in ids:
                    core |= cell_mask(i)
                core = cv2.erode((core & ~ink).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
                old = (cv2.dilate(old.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool) & m & ~core & (inner2 > 0)) | old
                oy, ox = np.nonzero(old)
                for j, i in enumerate(keys):
                    sel = which[oy, ox] == j + 1
                    t = tex[i]
                    rgba[oy[sel], ox[sel], :3] = t[oy[sel] % 32, ox[sel] % 32]
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
    dv = np.where((diff > 40)[..., None], np.array([255, 0, 0], np.uint8), (img * 0.4 + 150).astype(np.uint8))
    cv2.imwrite(os.path.join(OUT, "ghep_lech.png"), cv2.cvtColor(dv, cv2.COLOR_RGB2BGR))
    print(f"{len(info)} mảnh -> {os.path.join(OUT, 'atom', 'images')}; lệch ghép lại >40: {int((diff > 40).sum())} px")
    for p in info:
        print(f"  {p['name']:<14} at={p['at'][0]},{p['at'][1]} {p['size'][0]}x{p['size'][1]} bù {p['added']}")


if __name__ == "__main__":
    {"o": cmd_o, "cat": cmd_cat}[sys.argv[1]]()
