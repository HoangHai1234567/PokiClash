# -*- coding: utf-8 -*-
"""Quái đảo Kim (nhím thép, thay Giáp Vệ): cắt concept một ảnh thành mảnh để rig bằng AtomSpine (2026-11-20).

    py -3 -I ArtGen/Spine/quai_kim_cat.py o      # tách ô màu phẳng giữa nét mực, ghi ảnh đánh số + o_cells.json
    py -3 -I ArtGen/Spine/quai_kim_cat.py cat    # gom ô theo PARTS, vẽ bù phần bị che, ghi mảnh vào atom/images + parts.json

Concept: inbox/quai_kim/tai_ve/L1.png (1536x1024, nền trắng). Ô = vùng không phải mực, nối 4 hướng; mực chia cho ô gần nhất.
"""
import json
import os
import sys

import cv2
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "inbox", "quai_kim", "tai_ve", "L1.png")
OUT = os.path.join(HERE, "quai_kim")
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
    br = img[:, :, 2].astype(int) - img[:, :, 0].astype(int)
    # mực nâu sẫm (B-R âm); lông xanh đá phiến tối (B-R dương) không phải mực
    ink = fg & ((luma < 55) | ((luma < 125) & (br < 5)))
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


# Gốc toạ độ rig (điểm ảnh concept): giữa hai bàn chân, mặt đất dưới bàn chân. x thế giới = px - OX, y = OY - py.
OX, OY = 760, 962

# Ô 399 = lông đầu + thân + mặt (kem) + tay xa (lông sẫm) dính nhau (nét mực hở): tách theo màu (split_399) thành
# "FUR" (lông đầu + thân), "TAN" (mặt, mõm), "ARM" (tay xa).
# Bộ phận theo thứ tự vẽ sau → trước: tên, các ô (số ở o_cells.png), cách vẽ bù phần bị che
#   "hull": bù phần nằm trong bao lồi của mảnh mà bị mảnh vẽ sau che
#   ("grow", r): nới mảnh r điểm dưới các mảnh vẽ sau (gốc lưỡi bờm)
#   ("toward", cx, cy, d): kéo dài từng ô (lưỡi bờm) thẳng về tâm (cx, cy) tới d điểm dưới các mảnh vẽ sau
#   ("disk", x, y, r): bù hình tròn tâm (x,y) bán kính r chỗ bị mảnh vẽ sau che (gốc tay, gốc tai)
#   ("up", h): kéo dài phần trên của mảnh lên h điểm dưới mảnh vẽ sau (đỉnh chân dưới bụng)
PARTS = [
    ("bom_duoi", [1130, 1391], [("toward", 790, 600, 150), ("grow", 30)]),
    ("bom_giua", [554, 767], [("toward", 790, 600, 150), ("grow", 30)]),
    ("bom_tren", [23, 83, 270, 703], [("toward", 790, 600, 150), ("grow", 30)]),
    ("chan_xa", [1433], [("disk", 585, 800, 52), "hull"]),
    ("tay_xa", ["ARM", 549, 594, 660], [("disk", 640, 612, 40), "hull"]),
    ("tai_xa", [385, 435], [("disk", 990, 322, 30)]),
    ("tay_gan", [858], ["hull", ("disk", 985, 615, 42)]),
    ("vuot_gan", [870, 1044, 1131], []),
    ("chan_gan", [1428], [("disk", 945, 805, 55), "hull"]),
    ("than", ["FUR", 1014, 449], ["hull"]),
    ("mat", ["TAN", 525, 613, 599, 581, 805], []),
]
INK_W = 7          # bề dày viền mực kẻ lại ở chỗ vẽ bù (điểm ảnh concept)
SPLIT = 399


def split_399(img, lab):
    """ô 399 tách theo màu làm mờ (chỉ trong ô): kem (B-R âm) = mặt; lông sẫm (độ sáng < 89) = tay xa; còn lại = lông đầu, thân."""
    m = lab == SPLIT
    f = img.astype(np.float32)
    luma = f @ np.array([0.299, 0.587, 0.114], np.float32)
    br = f[..., 2] - f[..., 0]
    w = m.astype(np.float32)

    def blur(x, s=7):
        return cv2.GaussianBlur(x * w, (0, 0), s) / np.maximum(cv2.GaussianBlur(w, (0, 0), s), 1e-3)
    L, B = blur(luma), blur(br)
    tan = m & (B < 0)
    dark = m & ~tan & (L < 89)
    fur = m & ~tan & ~dark

    def biggest(x):
        n, cl, st, _ = cv2.connectedComponentsWithStats(x.astype(np.uint8), connectivity=4)
        if n <= 1:
            return x
        i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        return cl == i
    tan, dark = biggest(tan), biggest(dark)
    fur = m & ~tan & ~dark
    return {"TAN": tan, "ARM": dark, "FUR": fur}


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
    sub = split_399(img, lab)
    ink_rgb = np.median(img[ink], axis=0).astype(np.uint8)
    # mực / vụn của ô 399 chia cho phần con gần nhất
    own_split = own == SPLIT
    dists = {k: cv2.distanceTransform((~v).astype(np.uint8), cv2.DIST_L2, 5) for k, v in sub.items()}
    keys_sub = list(sub)
    arg = np.argmin(np.stack([dists[k] for k in keys_sub]), axis=0)
    own_sub = {k: own_split & (arg == j) for j, k in enumerate(keys_sub)}
    h, w = lab.shape

    def cell_mask(i):
        return sub[i] if isinstance(i, str) else lab == i

    # mực + viền khử răng cưa của nét (pha nâu mực vào màu tô: B-R âm, tối hơn màu tô) đi theo chủ vòng viền
    f32 = img.astype(np.float32)
    luma_all = f32 @ np.array([0.299, 0.587, 0.114], np.float32)
    ink_soft = fg & (ink | ((luma_all < 185) & ((f32[..., 2] - f32[..., 0]) < 5)))
    ring_k = np.ones((2 * INK_W + 1, 2 * INK_W + 1), np.uint8)

    def mask_of(ids):
        m = np.zeros((h, w), bool)
        c = np.zeros((h, w), bool)
        for i in ids:
            m |= own_sub[i] if isinstance(i, str) else own == i
            c |= cell_mask(i)
        # trọn vòng mực quanh ô của mảnh (mực ở chỗ giáp mảnh khác cũng thuộc mảnh này)
        m |= cv2.dilate(c.astype(np.uint8), ring_k).astype(bool) & ink_soft
        return m

    masks = {name: mask_of(ids) for name, ids, _ in PARTS}
    # nét mực chung giữa hai mảnh: phần còn sót bên mảnh vẽ trước (sát mảnh vẽ sau) chuyển hẳn cho mảnh vẽ sau, để mảnh vẽ sau giữ
    # trọn nét và mảnh vẽ trước không mang bản sao nét đó (xoay lệch là lộ viền đôi)
    order = [p[0] for p in PARTS]
    near_k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    for k, name in enumerate(order):
        for later in order[k + 1:]:
            moi = cv2.dilate(masks[later].astype(np.uint8), near_k).astype(bool) & masks[name] & ink_soft
            masks[later] |= moi
            masks[name] &= ~moi
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
        # mực chung ở chỗ giáp mảnh vẽ sau thuộc về mảnh vẽ sau (viền đầu, viền nắm tay...): mảnh sau bỏ phần đó (vùng bù lấp
        # bằng vân của nó), không thì bản sao đường viền xoay theo mảnh sau -> viền đôi
        m &= ~front
        add = np.zeros((h, w), bool)
        sweep_id = np.zeros((h, w), np.int32)   # vùng bù "toward": ô (1-based theo ids) kéo dài tới điểm này
        no_edge = np.zeros((h, w), bool)    # vùng bù "grow" (gốc lưỡi bờm luôn nằm dưới mảnh khác): không kẻ viền mép (kẻ thì lộ viền đôi khi bờm xoay)
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
            elif f[0] == "toward":
                # kéo dài từng lưỡi (từng ô) thẳng về tâm (f[1], f[2]) tới f[3] điểm dưới các mảnh vẽ sau: gốc lưỡi khuất vẫn đúng hình
                # lưỡi, ranh giữa hai lưỡi có nét mảnh (sweep_id ghi ô của từng điểm)
                cx, cy, dist = f[1], f[2], f[3]
                order_ids = sorted(ids, key=lambda i: -int(cell_mask(i).sum()))
                for i in order_ids:
                    cmk = (cell_mask(i) & ~ink).astype(np.uint8)
                    ys_, xs_ = np.nonzero(cmk)
                    vx, vy = cx - xs_.mean(), cy - ys_.mean()
                    nv = max(1e-6, (vx * vx + vy * vy) ** 0.5)
                    vx, vy = vx / nv, vy / nv
                    sw = np.zeros((h, w), bool)
                    for kk in range(1, dist // 6 + 1):
                        M = np.float32([[1, 0, vx * 6 * kk], [0, 1, vy * 6 * kk]])
                        sw |= cv2.warpAffine(cmk, M, (w, h), flags=cv2.INTER_NEAREST) > 0
                    new_px = sw & front & ~m & ~add
                    sweep_id[new_px] = ids.index(i) + 1
                    add |= new_px
                    no_edge |= new_px
            elif f[0] == "grow":
                # nới mảnh f[1] điểm dưới các mảnh vẽ sau (gốc lưỡi bờm lấp dưới thân, đầu), bo tròn
                k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * f[1] + 1, 2 * f[1] + 1))
                g = cv2.dilate(m.astype(np.uint8), k).astype(bool) & front & ~m
                sm = cv2.GaussianBlur((m | g).astype(np.float32), (0, 0), 10) > 0.5
                add |= g & sm
                no_edge |= g & sm
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
            which = np.where(sweep_id > 0, sweep_id, which)
            ys, xs = np.nonzero(add)
            for j, i in enumerate(keys):
                sel = which[ys, xs] == j + 1
                t = tex[i]
                rgba[ys[sel], xs[sel], :3] = t[ys[sel] % 32, xs[sel] % 32]
            if (no_edge & (sweep_id == 0)).any():
                # vùng "grow" (gốc lưỡi bờm, lộ ra khi bờm xoay): tông lưỡi phía xa (ô tối nhất của mảnh) -> đọc như lớp lưỡi sau
                dk = min(keys, key=lambda i: float(tex[i].reshape(-1, 3).astype(float).mean()))
                gy, gx_ = np.nonzero(no_edge & (sweep_id == 0))
                rgba[gy, gx_, :3] = tex[dk][gy % 32, gx_ % 32]
            rgba[add, 3] = 255
            # đường ranh giữa hai ô khác nhau trong vùng bù (nối tiếp các đường đốt / mép tấm giáp), nét mảnh
            wm = np.zeros((h, w), np.int32)
            wm[ys, xs] = which[ys, xs]
            gx = np.zeros((h, w), bool)
            gx[:, 1:] |= (wm[:, 1:] != wm[:, :-1]) & (wm[:, 1:] > 0) & (wm[:, :-1] > 0)
            gx[1:, :] |= (wm[1:, :] != wm[:-1, :]) & (wm[1:, :] > 0) & (wm[:-1, :] > 0)
            seam = cv2.dilate(gx.astype(np.uint8), np.ones((4, 4), np.uint8)).astype(bool) & add & ~(no_edge & (sweep_id == 0))
            rgba[seam, :3] = ink_rgb
            # viền mực mới: mép của mảnh mở rộng nằm trong vùng bù
            full = (m | add).astype(np.uint8)
            inner = cv2.erode(full, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (INK_W, INK_W)))
            edge = (full > 0) & (inner == 0) & cv2.dilate((add & ~no_edge).astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
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
