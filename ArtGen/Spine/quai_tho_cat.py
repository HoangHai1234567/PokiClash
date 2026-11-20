# -*- coding: utf-8 -*-
"""Quái đảo Thổ (dê đá húc, thay Chuột Khoan): cắt concept một ảnh thành mảnh để rig bằng AtomSpine (2026-11-20).

    py -3 -I ArtGen/Spine/quai_tho_cat.py o      # tách ô màu phẳng giữa nét mực, ghi ảnh đánh số + o_cells.json
    py -3 -I ArtGen/Spine/quai_tho_cat.py cat    # gom ô theo PARTS, vẽ bù phần bị che, ghi mảnh vào atom/images + parts.json

Concept: inbox/quai_tho/tai_ve/L1.png (1536x1024, nền trắng). Ô = vùng không phải mực, nối 4 hướng; mực chia cho ô gần nhất.
"""
import json
import os
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "inbox", "quai_tho", "tai_ve", "L1.png")
OUT = os.path.join(HERE, "quai_tho")
INK_LUMA = 62      # mực ~20-50; móng, chân xa ~72-100 (con dê)
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


# Gốc toạ độ rig (điểm ảnh concept): giữa bốn móng, mặt đất dưới móng. x thế giới = px - OX, y = OY - py.
OX, OY = 625, 930

# Bộ phận theo thứ tự vẽ sau → trước: tên, các ô (số ở o_cells.png), cách vẽ bù phần bị che
#   "hull": bù phần nằm trong bao lồi của mảnh mà bị mảnh vẽ sau che; ("hull", tên...): thêm vùng các mảnh đó đè lên
#   ("disk", x, y, r): bù hình tròn chỗ bị mảnh vẽ sau che; ("up", h): kéo dài phần trên của mảnh lên h điểm dưới mảnh vẽ sau
PARTS = [
    ("bom", [], [("blob", 1010, 410, 175, 235, 100)]),   # lông gáy sau đầu + sừng xa: chỉ lộ khi đầu cúi / ngửa
    ("sung_xa", [168, 231, 524, 609], ["hull"]),
    ("chan_xa_sau", [1052, 1360, 1361], [("up", 60), "hull"]),
    ("chan_xa_truoc", [1001, 1354, 1363], [("up", 60), "hull"]),
    ("da1", [450], ["hull"]),
    ("da2", [185], ["hull"]),
    ("da3", [24], ["hull"]),
    ("duoi", [604], ["hull"]),
    ("chan_gan_sau", [940, 1358, 1366], [("up", 60), "hull"]),
    ("chan_gan_truoc", [971, 1429], [("up", 60), "hull"]),
    ("than", [100, 895], ["hull"]),
    ("tai_xa", [615], [("disk", 1150, 500, 26)]),
    ("dau", [630, 677, 717, 689, 695, 785], [("hull", "sung_gan")]),
    ("sung_gan", [265, 432, 661, 683, 617], []),
]
RING_W = 13        # vòng mực quanh ô thuộc về mảnh (nét concept dày ~10-12 px)
INK_W = 7          # bề dày viền mực kẻ lại ở chỗ vẽ bù (điểm ảnh concept)


def split_antenna(lab):
    """con dê không có râu dính đầu: không tách."""
    z = np.zeros(lab.shape, bool)
    return z, z


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
    own_head = np.zeros(own.shape, bool)
    # mực của ô 240: điểm mực gần râu hơn thì thuộc râu
    d_ant = cv2.distanceTransform((~ant_m).astype(np.uint8), cv2.DIST_L2, 5)
    d_head = cv2.distanceTransform((~head_m).astype(np.uint8), cv2.DIST_L2, 5)
    own_ant = own_head & (d_ant < d_head)
    own_head = own_head & ~own_ant
    h, w = lab.shape

    def cell_mask(i):
        return ant_m if i == "ANT" else head_m if i == "HEAD" else lab == i

    ring_k = np.ones((2 * RING_W + 1, 2 * RING_W + 1), np.uint8)

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
    # mực ở ranh với mảnh vẽ SAU thuộc mảnh đó (viền sừng gần không in thành vòng trên thân); chỗ đó vẽ bù bằng vân
    _nm = [p[0] for p in PARTS]
    removed = {}
    for k, name in enumerate(_nm):
        later = np.zeros(ink.shape, bool)
        for n2 in _nm[k + 1:]:
            later |= masks[n2]
        rm = cv2.dilate((later & ink).astype(np.uint8), np.ones((7, 7), np.uint8)).astype(bool) & masks[name] & ~later
        removed[name] = rm | (masks[name] & later & ink)      # cả viền khử răng cưa sát nét mực đó
        masks[name] &= ~removed[name]
    all_ids = [i for _, ids, _ in PARTS for i in ids]
    tex = textures(img, lab, {i: cell_mask(i) & ~ink for i in all_ids})
    names = [p[0] for p in PARTS]
    os.makedirs(os.path.join(OUT, "atom", "images"), exist_ok=True)
    info = []
    for k, (name, ids, fills) in enumerate(PARTS):
        m = masks[name].copy()
        front = np.zeros((h, w), bool)
        for later in names[k + 1:]:
            front |= masks[later] | removed[later]
        cover = front.copy()                 # vùng mảnh vẽ sau che lúc đứng yên
        front |= removed[name]
        add = np.zeros((h, w), bool)
        blob = None
        for f in fills:
            if f != "hull" and f[0] == "blob":
                e = np.zeros((h, w), np.uint8)
                cv2.ellipse(e, (f[1], f[2]), (f[3], f[4]), 0, 0, 360, 1, -1)
                add |= (e > 0) & front
                blob = f[5]
            elif f == "hull" or f[0] == "hull":
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
                sig = min(18.0, max(3.0, 0.05 * float(np.sqrt(m.sum()))))     # mảnh nhỏ (chân) làm trơn ít, không xén góc
                sm = cv2.GaussianBlur(full, (0, 0), sig) > 0.5
                add |= cand & sm
            elif f[0] == "disk":
                d = np.zeros((h, w), np.uint8)
                cv2.circle(d, (f[1], f[2]), f[3], 1, -1)
                add |= (d > 0) & front & ~m
            elif f[0] == "up":
                ys, xs = np.nonzero(m)
                top = ys.min()
                band = m[top:top + 40]                       # 40 hàng trên cùng của mảnh (đầu chân dưới lông)
                cols = np.nonzero(band.any(axis=0))[0]
                ext = np.zeros((h, w), bool)
                c0, c1 = cols.min(), cols.max()
                e8 = np.zeros((h, w), np.uint8)              # đầu chân bo tròn (lộ ra dưới lông thì không thành góc vuông)
                cv2.ellipse(e8, ((c0 + c1) // 2, top + 20), ((c1 - c0) // 2, f[1] + 20), 0, 180, 360, 1, -1)
                e8[top + 20:top + 40, c0:c1 + 1] = 1
                ext = e8 > 0
                add |= ext & front & ~m
        if any(f != "hull" and f[0] == "up" for f in fills):
            # chân: đóng hình (lấp khấc lõm giữa đầu chân bo tròn và mép chân) trong phần bị che
            full = (m | add).astype(np.uint8)
            cl = cv2.morphologyEx(full, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))) > 0
            add |= cl & ~m & cover          # chỉ trong phần bị che (không đổi hình lúc đứng yên)
        m |= removed[name] & ~add & ~cover   # viền đã bỏ, không vẽ bù, không bị che (mép ngoài) thì giữ như ảnh gốc
        rgba = np.zeros((h, w, 4), np.uint8)
        rgba[m, :3] = img[m]
        rgba[m, 3] = 255
        if blob is not None:
            ys, xs = np.nonzero(add)
            t = tex[blob]
            rgba[ys, xs, :3] = t[ys % 32, xs % 32]
            rgba[add, 3] = 255
            full = add.astype(np.uint8)
            inner = cv2.erode(full, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (INK_W, INK_W)))
            edge = (full > 0) & (inner == 0)
            rgba[edge, :3] = ink_rgb
        elif add.any():
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
