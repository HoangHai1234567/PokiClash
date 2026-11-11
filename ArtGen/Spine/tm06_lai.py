# -*- coding: utf-8 -*-
"""tm06 dạng 2, cách lai (đặc tả mục 5): thân + đầu trên + vòng cổ + vây lưng/đuôi + chân + bình + nắp CẮT THẲNG TỪ CONCEPT (vùng
loang từ hạt giống, nét mực là tường, nét mực và ô kín lấy nhãn gần nhất), mảnh GPT đã đặt (place.json) làm nguồn vẽ bù chỗ bị che
(lưng dưới bình, gáy dưới mang, thân dưới đỉnh chân, miệng bình dưới nắp). Hàm dưới, lòng miệng, mí, lá mang vẫn dùng mảnh GPT.
Ra inbox/tm06_2/lai/: <lớp>.png (cắt sát), nhan_than.png (nhãn vùng của lớp thân, để chia trọng số), meta.json (khung từng lớp, px
concept), nhan.png và lop.png để soi. Cần cv2:

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm06_lai.py
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tm06_place as PL  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
K = 2
NAMES = ["duoi", "than", "co", "dau", "ham", "mang", "binh", "nap", "chan1", "chan2", "chan3", "chan4"]
# hạt giống (px concept dạng 2): ("line", [điểm], dày) | ("poly", [điểm])
SEED = {
    "duoi": [("line", [(150, 470), (260, 520), (380, 555), (440, 565)], 12)],
    "than": [("line", [(455, 668), (780, 676)], 10), ("line", [(975, 676), (1060, 650)], 8), ("line", [(330, 560), (520, 555)], 10),
             ("line", [(960, 575), (1005, 580)], 8), ("line", [(570, 588), (875, 600)], 6)],
    "co": [("line", [(1030, 505), (1050, 560), (1062, 618)], 9)],
    "dau": [("poly", [(1150, 482), (1330, 472), (1382, 520), (1360, 556), (1172, 562)])],
    "ham": [("line", [(1125, 600), (1250, 612), (1360, 604)], 7)],
    "binh": [("poly", [(565, 402), (878, 402), (888, 498), (566, 518)]), ("line", [(610, 540), (850, 546)], 6)],
    "nap": [("poly", [(684, 264), (868, 264), (868, 316), (684, 316)]), ("line", [(786, 206), (856, 206)], 6)],
    "chan1": [("poly", [(362, 612), (428, 606), (430, 682), (372, 690)]), ("line", [(392, 690), (392, 772)], 14)],
    "chan2": [("line", [(640, 702), (645, 772)], 10)],
    "chan3": [("poly", [(848, 616), (938, 610), (944, 690), (862, 700)]), ("line", [(900, 700), (902, 772)], 14)],
    "chan4": [("poly", [(1162, 642), (1228, 640), (1248, 700), (1182, 710)]), ("line", [(1232, 712), (1262, 772)], 14)],
}
# vùng được phép của một phần (đa giác px concept): phần lọt ra ngoài trả cho nhãn bên cạnh
CLAMP = {"binh": [(520, 285), (915, 285), (915, 572), (520, 572)]}
# ép vùng sau khi loang (đa giác px concept): sửa chỗ loang lấn
OVERRIDE = {}
MAIN = ("duoi", "than", "co", "dau")      # lớp thân liền một lưới
NEAR_LEGS = ("chan1", "chan3", "chan4")   # chân trước thân
GROW = 38                                  # px concept: lớp dưới mọc thêm dưới lớp trên
DUI = 22                                   # px concept: đùi phần cao hơn đường bụng - DUI (vồng thêm CUNG) thuộc thân
CUNG = 22
HAM_GIU_X = 1165                           # px concept: phần hàm concept bên trái x này (góc hàm dưới má) ở lại lớp thân


def inbox(*p):
    return os.path.join(HERE, "inbox", f"tm06_{K}", *p)


def seeds(shape):
    mk = np.full(shape, -1, np.int32)
    for i, n in enumerate(NAMES):
        for s in SEED.get(n, []):
            if s[0] == "line":
                cv2.polylines(mk, [np.array(s[1], np.int32)], False, i, int(s[2]))
            else:
                cv2.fillPoly(mk, [np.array(s[1], np.int32)], i)
    return mk


def fill_nearest(lab, need):
    src = (lab >= 0) & ~need
    if not need.any() or not src.any():
        return lab
    d, li = cv2.distanceTransformWithLabels((~src).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(src)
    out = lab.copy()
    out[need] = lab[ys, xs][li[need] - 1]
    return out


def labels(rgb, fg):
    lab = seeds(fg.shape)
    lab[fg == 0] = -1
    r, g, b = (rgb[:, :, c].astype(np.int16) for c in range(3))
    red = (r > 150) & (g < 115) & (b < 115) & (r - g > 70) & (np.abs(g - b) < 45) & (fg > 0)
    red = cv2.morphologyEx(red.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8)) > 0
    lab[red] = NAMES.index("mang")
    fin = (b > 200) & (r < 175) & (g > 150) & (b - g > 18) & (fg > 0)
    ys, xs = np.mgrid[0:fg.shape[0], 0:fg.shape[1]]
    finb = fin & (ys < 640)
    lab[finb & (xs < 470)] = NAMES.index("duoi")
    lab[finb & (xs >= 470) & (lab < 0)] = NAMES.index("than")
    ink = (rgb.mean(2) < 72) & (fg > 0)
    dom = (fg > 0) & ~ink
    k3 = np.ones((3, 3), np.uint8)
    for _ in range(800):
        miss = dom & (lab < 0)
        gg = cv2.dilate(lab.astype(np.float32) + 1, k3).astype(np.int32) - 1
        upd = miss & (gg >= 0)
        if not upd.any():
            break
        lab[upd] = gg[upd]
    lab = fill_nearest(lab, (fg > 0) & (lab < 0))
    cnt = np.stack([cv2.boxFilter((lab == i).astype(np.float32), -1, (7, 7), normalize=False) for i in range(len(NAMES))], 0)
    lab2 = np.where(fg > 0, cnt.argmax(0), -1).astype(np.int32)
    lab2[red] = NAMES.index("mang")
    for n, polys in OVERRIDE.items():
        for pg in polys:
            m = np.zeros(fg.shape, np.uint8)
            cv2.fillPoly(m, [np.array(pg, np.int32)], 1)
            lab2[(m > 0) & (fg > 0)] = NAMES.index(n)
    for i in range(len(NAMES)):
        nc, cl, st, _ = cv2.connectedComponentsWithStats((lab2 == i).astype(np.uint8), connectivity=8)
        if nc <= 2:
            continue
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        for c in range(1, nc):
            if c != big and st[c, cv2.CC_STAT_AREA] < 400 and NAMES[i] != "mang":
                lab2[cl == c] = -1
    for n, pg in CLAMP.items():
        m = np.zeros(fg.shape, np.uint8)
        cv2.fillPoly(m, [np.array(pg, np.int32)], 1)
        out_ = (lab2 == NAMES.index(n)) & (m == 0)
        lab2[out_] = -1
    lab2 = fill_nearest(lab2, (fg > 0) & (lab2 < 0))
    return lab2


def bo_muc(rgba, vung, ink):
    """ảnh màu nguồn đã xoá nét mực (loang màu vào chỗ nét) để vẽ bù không kéo vệt sẫm."""
    src = rgba[:, :, :3].copy()
    m = (ink & vung).astype(np.uint8) * 255
    return cv2.inpaint(src, m, 5, cv2.INPAINT_TELEA) if m.any() else src


def ve_bu(rgba, vung, nguon_mask, ink):
    """tô vung (chưa có hình) bằng màu loang từ nguon_mask (đã xoá nét mực)."""
    if not vung.any():
        return rgba
    src = bo_muc(rgba, nguon_mask, ink)
    src[~nguon_mask & ~vung] = 0
    inp = cv2.inpaint(src, (vung | (~nguon_mask & (rgba[:, :, 3] == 0))).astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)
    rgba[vung, :3] = inp[vung]
    rgba[vung, 3] = 255
    return rgba


def gpt_layer(parts, out, n):
    """ảnh RGBA cỡ concept của một mảnh GPT đã đặt (place.json)."""
    return PL.ghep(REF_SHAPE, {n: parts[n]}, out, [n])


def soft_alpha(m):
    a = cv2.GaussianBlur(m.astype(np.float32), (3, 3), 0.8)
    return (np.clip(a * 1.15, 0, 1) * 255).astype(np.uint8)


def ke_ranh(rgba, ranh, day=3):
    """kẻ nét mực (#2B2118) dọc ranh cắt (mép lớp trên chồng lên lớp dưới, chỗ concept không có nét)."""
    m = cv2.dilate(ranh.astype(np.uint8), np.ones((day, day), np.uint8)) > 0
    m &= rgba[:, :, 3] > 0
    rgba[m, 0], rgba[m, 1], rgba[m, 2] = 43, 33, 24
    return rgba


def main():
    global REF_SHAPE
    rgb = np.array(Image.open(inbox("tai_ve", "L1_duyet.png")).convert("RGB"))
    REF_SHAPE = rgb.shape
    fg = PL.fg_mask(rgb) > 0
    lab = labels(rgb, fg)
    pj = json.load(open(inbox("place.json"), encoding="utf-8"))
    out = pj["parts"]
    parts = {}
    for n in ("than", "dau", "binh", "nap", "duoi"):
        if n in out:
            parts[n] = PL.nap(K, out[n].get("img", n))
    G = {n: gpt_layer(parts, out, n) for n in parts}
    gm = {n: G[n][:, :, 3] > 128 for n in G}
    ink = (rgb.mean(2) < 72) & fg
    L = {n: lab == NAMES.index(n) for n in NAMES}
    layers = {}

    def put(dst, src, m):
        dst[m, :3] = src[m, :3]
        dst[m, 3] = 255

    # ---- lớp thân liền (thân, đuôi, vòng cổ, đầu trên)
    mainm = np.zeros(fg.shape, bool)
    for n in MAIN:
        mainm |= L[n]
    # góc hàm sát bản lề (dưới má) giữ trên lớp thân: hàm GPT mờ dần vào đây, há miệng không lộ lỗ ở bản lề
    xx0 = np.arange(fg.shape[1])[None, :]
    goc_ham = L["ham"] & (xx0 < HAM_GIU_X)
    mainm |= goc_ham
    lab[goc_ham] = NAMES.index("dau")
    T = np.zeros(rgb.shape[:2] + (4,), np.uint8)
    T[mainm, :3] = rgb[mainm]
    T[mainm, 3] = 255
    # vẽ bù: lưng dưới bình / nắp, gáy và lưng dưới lá mang, thân dưới đỉnh chân (mọc thêm GROW px), lấy từ mảnh GPT đã đặt
    dist_main = cv2.distanceTransform((~mainm).astype(np.uint8), cv2.DIST_L2, 5)
    # lưng dưới bình: đường lưng nội suy qua các cột có bình / mang (như đường bụng dưới đùi)
    cover = L["binh"] | L["nap"] | L["mang"]
    topy = np.full(fg.shape[1], -1)
    covcol = cv2.dilate(cover.astype(np.uint8), np.ones((1, 9), np.uint8)).any(axis=0)
    rr0, gg0, bb0 = (rgb[:, :, c].astype(np.int16) for c in range(3))
    vay = (bb0 > 190) & (bb0 - gg0 > 18)                  # vây lam nhạt: không tính vào đường lưng
    vay = cv2.dilate(vay.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    lung = mainm & ~vay & ~ink
    for x in np.nonzero(lung.any(axis=0))[0]:
        if covcol[x]:
            continue
        ys_ = np.nonzero(lung[:, x])[0]
        topy[x] = ys_.min()
    okx = np.nonzero(topy >= 0)[0]
    back = np.interp(np.arange(fg.shape[1]), okx, topy[okx]) if len(okx) else np.zeros(fg.shape[1])
    yy0 = np.arange(fg.shape[0])[:, None]
    # lưng dưới bình: thân GPT đã đặt (có lưng, vây thấp) + dải đáy bình 45 px (chỗ thân GPT hụt, lộ khi bình chúc)
    ub = np.full(fg.shape[1], 10 ** 6)
    for x in np.nonzero(L["binh"].any(axis=0))[0]:
        ub[x] = np.nonzero(L["binh"][:, x])[0].max()
    day_binh = L["binh"] & (yy0 >= ub[None, :] - 45)
    under_urn = (L["binh"] | L["nap"]) & (gm.get("than", False) | day_binh)
    _ = back
    gmd = gm.get("dau", np.zeros(fg.shape, bool))
    under_gill_gpt = L["mang"] & (gm.get("than", False) | gmd)
    under_gill_near = np.zeros(fg.shape, bool)   # mang lòi ra ngoài thân, đầu: sau nó là nền, không vẽ bù
    if "than" in G:
        put(T, G["than"], (under_urn | under_gill_gpt) & gm["than"] & ~mainm)
    if "dau" in G:
        put(T, G["dau"], under_gill_gpt & gmd & ~mainm)
    # thân dưới đỉnh chân gần: mọc thêm GROW px nhưng không quá đường bụng (nội suy mép bụng hai bên chân)
    legs_near = np.zeros(fg.shape, bool)
    for n in NEAR_LEGS:
        legs_near |= L[n]
    bot = np.full(fg.shape[1], -1)
    cols = np.nonzero(mainm.any(axis=0))[0]
    legcol = cv2.dilate(legs_near.astype(np.uint8), np.ones((1, 15), np.uint8)).any(axis=0)
    for x in cols:
        if legcol[x]:
            continue                       # cột có chân: đường bụng nội suy từ hai bên
        ys = np.nonzero(mainm[:, x])[0]
        if len(ys):
            bot[x] = ys.max()
    xs_ok = np.nonzero(bot >= 0)[0]
    belly = np.interp(np.arange(fg.shape[1]), xs_ok, bot[xs_ok]) if len(xs_ok) else np.zeros(fg.shape[1])
    yy = np.arange(fg.shape[0])[:, None]
    under_leg = legs_near & (yy <= belly[None, :] + 2)            # cả phần đùi nằm trong thân (trên đường bụng)
    under_leg |= legs_near & (dist_main < GROW) & (yy <= belly[None, :] + 2)
    # đỉnh đùi (cao hơn đường bụng quá DUI px) ở lại lớp thân: chân chỉ từ đường cong này xuống, ranh kẻ nét mực theo cung
    # pixel cam bụng / lam vây lọt vào nhãn chân (mép đùi giáp bụng, đuôi): trả về lớp thân
    rr, gg2, bb = (rgb[:, :, c].astype(np.int16) for c in range(3))
    lan = ((rr > 200) & (gg2 > 90) & (gg2 < 190) & (bb < 100)) | ((bb > 200) & (bb - gg2 > 18) & (yy < belly[None, :] + 4))
    lan = cv2.dilate(lan.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    for n in NEAR_LEGS:
        m_ = L[n] & lan & (yy < belly[None, :] + 4)
        if m_.any():
            T[m_, :3] = rgb[m_]
            T[m_, 3] = 255
            mainm |= m_
            L[n] &= ~m_
            lab[m_] = NAMES.index("than")
    dui = np.zeros(fg.shape, bool)
    for n in NEAR_LEGS:          # đường cắt cong như khớp hông (vồng lên giữa chân), không thẳng
        xs_n = np.nonzero(L[n].any(axis=0))[0]
        if not len(xs_n):
            continue
        xl, xr = xs_n.min(), xs_n.max()
        u = np.clip((np.arange(fg.shape[1]) - xl) / max(1, xr - xl), 0, 1)
        cut = belly - DUI - CUNG * np.sin(np.pi * u)
        dui |= L[n] & (yy < cut[None, :])
    if dui.any():
        T[dui, :3] = rgb[dui]
        T[dui, 3] = 255
        mainm |= dui
        for n in NEAR_LEGS:
            L[n] &= ~dui
        lab[dui] = NAMES.index("than")
        legs_near &= ~dui
        under_leg &= ~dui
    if "than" in G:   # thân dưới đùi: ưu tiên thân GPT đã đặt (cùng nét, vân), phần còn lại loang màu
        put(T, G["than"], under_leg & gm["than"] & ~mainm)
    vung = (under_leg | under_gill_near | under_urn) & (T[:, :, 3] == 0)
    T = ve_bu(T, vung, T[:, :, 3] > 0, ink)
    # nét mực mép bụng dưới các chân gần (lộ ra khi chân đung đưa): kẻ theo đường bụng nội suy
    for n in NEAR_LEGS:
        xs_n = np.nonzero((L[n] | dui).any(axis=0))[0]
        if not len(xs_n):
            continue
        pts = np.array([(x, belly[x]) for x in range(xs_n.min() - 4, xs_n.max() + 5)], np.int32)
        lm = np.zeros(fg.shape, np.uint8)
        cv2.polylines(lm, [pts], False, 1, 5)
        lm = (lm > 0) & (T[:, :, 3] > 0)
        T[lm, 0], T[lm, 1], T[lm, 2] = 43, 33, 24
    T[:, :, 3] = np.where(T[:, :, 3] > 0, soft_alpha(T[:, :, 3] > 0), 0)
    layers["than"] = T
    # nhãn vùng của lớp thân (để chia trọng số): vùng vẽ bù lấy nhãn thân gần nhất
    labm = np.where(mainm, lab, -1)
    labm = fill_nearest(labm, (T[:, :, 3] > 0) & ~mainm)
    labm[T[:, :, 3] == 0] = -1
    # ---- bình (không nắp): miệng bình dưới nắp và chỗ bị mang che lấy từ bình GPT
    B = np.zeros_like(T)
    put(B, np.dstack([rgb, np.full(fg.shape, 255, np.uint8)]), L["binh"])
    if "binh" in G:
        put(B, G["binh"], (L["nap"] | L["mang"]) & gm["binh"] & ~L["binh"])
    B[:, :, 3] = np.where(B[:, :, 3] > 0, soft_alpha(B[:, :, 3] > 0), 0)
    layers["binh"] = B
    # ---- nắp (cắt từ concept; chỗ mang che lấy từ nắp GPT)
    N = np.zeros_like(T)
    put(N, np.dstack([rgb, np.full(fg.shape, 255, np.uint8)]), L["nap"])
    if "nap" in G:
        put(N, G["nap"], L["mang"] & gm["nap"])
    N[:, :, 3] = np.where(N[:, :, 3] > 0, soft_alpha(N[:, :, 3] > 0), 0)
    layers["nap"] = N
    # ---- chân: chân gần trước thân (mép trên kẻ nét mực theo ranh, chỗ concept không có nét), chân xa sau thân mọc thêm lên trên
    for n in NEAR_LEGS + ("chan2",):
        C = np.zeros_like(T)
        put(C, np.dstack([rgb, np.full(fg.shape, 255, np.uint8)]), L[n])
        if n in NEAR_LEGS:
            border = L[n] & (cv2.dilate(mainm.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0)
            border &= ~cv2.dilate(ink.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
            C = ke_ranh(C, border, 4)
        else:
            dl = cv2.distanceTransform((~L[n]).astype(np.uint8), cv2.DIST_L2, 5)
            up = np.zeros(fg.shape, bool)
            ys, xs = np.nonzero(L[n])
            top = ys.min()
            up[max(0, top - GROW):top + 10, xs.min():xs.max() + 1] = True
            grow = up & (dl < GROW) & ~L[n]
            C = ve_bu(C, grow, L[n], ink)
        C[:, :, 3] = np.where(C[:, :, 3] > 0, soft_alpha(C[:, :, 3] > 0), 0)
        layers[n] = C
    # ---- lưu: cắt sát, ghi khung
    os.makedirs(inbox("lai"), exist_ok=True)
    meta = {"ref_size": [rgb.shape[1], rgb.shape[0]], "ground": pj["ground"], "layers": {}, "names": NAMES}
    for n, im in layers.items():
        a = im[:, :, 3]
        ys, xs = np.nonzero(a)
        x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1
        Image.fromarray(im[y0:y1, x0:x1], "RGBA").save(inbox("lai", n + ".png"))
        meta["layers"][n] = [x0, y0, x1, y1]
        if n == "than":
            sub = labm[y0:y1, x0:x1]
            Image.fromarray((sub + 1).astype(np.uint8), "L").save(inbox("lai", "nhan_than.png"))
    json.dump(meta, open(inbox("lai", "meta.json"), "w", encoding="utf-8"), indent=1)
    # ---- soi: bản đồ nhãn, từng lớp trên nền xám
    pal = np.array([[60, 120, 220], [120, 90, 160], [40, 170, 150], [230, 150, 40], [250, 120, 30], [220, 40, 40], [30, 140, 100],
                    [200, 200, 40], [150, 60, 200], [90, 90, 90], [200, 80, 160], [80, 200, 80]], np.uint8)
    vis = np.full(rgb.shape, 255, np.uint8)
    for i in range(len(NAMES)):
        vis[lab == i] = pal[i]
    vis = (0.55 * vis + 0.45 * rgb).astype(np.uint8)
    vis[ink] = (vis[ink] * 0.4).astype(np.uint8)
    for i, n in enumerate(NAMES):
        cv2.putText(vis, n, (10, 30 + 26 * i), cv2.FONT_HERSHEY_SIMPLEX, 0.8, tuple(int(c) for c in pal[i]), 2)
    Image.fromarray(vis).save(inbox("lai", "nhan.png"))
    tiles = []
    for n, im in layers.items():
        g = np.full(rgb.shape, 150, np.uint8)
        a = im[:, :, 3:4] / 255.0
        g = (im[:, :, :3] * a + g * (1 - a)).astype(np.uint8)
        cv2.putText(g, n, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 0), 3)
        tiles.append(cv2.resize(g, (768, 512)))
    while len(tiles) % 3:
        tiles.append(np.full((512, 768, 3), 255, np.uint8))
    rows = [np.concatenate(tiles[i:i + 3], 1) for i in range(0, len(tiles), 3)]
    Image.fromarray(np.concatenate(rows, 0)).save(inbox("lai", "lop.png"))
    for n in NAMES:
        print(f"  {n:6s} {int(L[n].sum()):7d} px")
    print("  lớp:", ", ".join(f"{n} {v[2] - v[0]}x{v[3] - v[1]}" for n, v in meta["layers"].items()))


if __name__ == "__main__":
    main()
