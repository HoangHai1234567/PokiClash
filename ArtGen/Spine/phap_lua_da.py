# -*- coding: utf-8 -*-
"""Pháp sư lửa (phap_lua, tướng thứ 6 đảo Hỏa): RESKIN đúng nghĩa trên con gốc monster_3481 (skill pokiclash-spine-rig mục 23, mẫu cung_lua_da.py).

Mỗi mảnh của con gốc một mảnh của mình, vẽ trên CHÍNH khung ảnh vùng của mảnh đó; tờ hướng dẫn là các mảnh GỐC (cắt theo lưới, phóng to).
GPT chỉ đổi da theo concept đã duyệt, giữ hình bóng và đường cấu trúc. Ảnh con gốc chỉ nằm trong máy và gửi GPT làm mẫu, không đăng công khai.

Riêng TRƯỢNG (con gốc: một ảnh liền con mắt) tách ba lớp: khung trượng (tờ D: ảnh gốc đã XOÁ quả cầu mắt), cầu lửa + tim lửa + ba lưỡi lửa
+ ba cuộn khói (tờ E: tờ hướng dẫn vẽ bằng mã, mảnh mới của mình, không có ở con gốc).

    phap_lua_da.py to [hướng]   tờ mảnh gốc + file prompt → inbox/phap_lua_1/mau/goc_<A..E>.png (+ .json), gui_gpt/phap_lua_1/luot_2_da_<A..E>.txt
    phap_lua_da.py cat [tờ..]   cắt tờ D_A.. đã gen → inbox/phap_lua_1/manh/<vùng>.png (cỡ ảnh vùng × RES) + _so_<tờ>.png, _iou.json
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import phap_lua as G  # noqa: E402

W, H = 1536, 1024
RES = 2                      # ảnh mảnh của mình = ảnh vùng của họ × RES
MANH = os.path.join(G.BASE, "manh")
GUI = os.path.join(HERE, "gui_gpt", "phap_lua_1")
CONCEPT = os.path.join(G.TAI, "L1_duyet.png")
KIEM_SI = os.path.join(HERE, "inbox", "kiem_si_1", "tai_ve", "L1_duyet.png")
INK = (43, 33, 24)
LUA = ((224, 68, 31), (247, 144, 42), (255, 212, 90))
KHOI = ((58, 52, 58), (104, 98, 106), (150, 145, 152))

# tờ → các hàng [(vùng, phóng)]
TO = {      # mảnh GIỮ hình bóng con gốc (tóc, hai cổ tay khói, dây bện, hai gai sao; ngón / vuốt; khung trượng). Áo, khăn vai, đầu đổi hẳn dáng:
            # gen từ concept đã duyệt (prompt_concept), không nằm trên tờ mảnh gốc.
    "B": [[("maofa_01", 3.0)],
          [("shouzhangR_01", 4.0), ("shouzhangL_01", 4.0), ("shenti", 2.8), ("zhuangshi_02", 4.5), ("zhuangshi_01", 4.5)]],
    "C": [[("shouzhiR_01", 6.0), ("shouzhiR_02", 6.0), ("shouzhiR_03", 6.0), ("shouzhiR_04", 6.0)],
          [("shouzhiL_01", 6.0), ("shouzhiL_02", 6.0), ("shouzhiL_03", 6.0), ("shouzhiL_04", 6.0), ("shouzhiL_05", 6.0)],
          [("shouzhiL_06", 6.0), ("shouzhiL_07", 6.0), ("shouzhiL_08", 6.0), ("shouzhiL_09", 6.0), ("shouzhiL_10", 6.0)]],
    "D": [[("wuqi", 2.9)]],
}
# tờ E (mảnh mới): tên → (ô x, y, rộng, cao) trên tờ 1536 × 1024
E_O = {
    "cau": (60, 90, 420, 420), "tim": (80, 580, 300, 300),
    "lua_0": (540, 60, 250, 560), "lua_1": (830, 150, 210, 470), "lua_2": (1080, 230, 180, 390), "lua_3": (1300, 300, 170, 320),
    "khoi_0": (470, 690, 300, 280), "khoi_1": (820, 700, 260, 250), "khoi_2": (1130, 720, 220, 210),
}


def Wp(p):
    return os.path.normpath(p)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def vung():
    """{vùng: (hình đầu tiên dùng vùng đó, ảnh part cắt theo lưới)}."""
    G._C.pop("att", None)
    _, imgs, atts = G.nap("att_goc.json")
    out = {}
    for a in atts:
        if a["region"] not in out:
            out[a["region"]] = (a, G.part_goc(a))
    return out


def cau_trong_truong(im):
    """quả cầu mắt trong ảnh trượng gốc: (cx, cy, R) px ảnh vùng + mặt nạ vùng cầu lộ ra (không bị khung trượng che)."""
    A = np.asarray(im).astype(np.int32)
    al, rgb = A[..., 3], A[..., :3]
    sang = ((al > 110) & (rgb.sum(-1) > 480)).astype(np.uint8)
    dong = cv2.morphologyEx(sang, cv2.MORPH_CLOSE, el(6))
    n, lab, st, _ = cv2.connectedComponentsWithStats(dong)
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    (cx, cy), R = cv2.minEnclosingCircle(np.argwhere(lab == k)[:, ::-1].astype(np.float32))
    tron = np.zeros(al.shape, np.uint8)
    cv2.circle(tron, (int(round(cx)), int(round(cy))), int(round(R + 2.5)), 1, -1)
    # khung trượng: xám tím ít bão hoà (kể cả mảng sáng hơn của nó); quả cầu: trắng / tím bão hoà
    toi = ((al > 110) & (rgb.sum(-1) < 470) & (rgb[..., 2] - rgb[..., 1] < 45)).astype(np.uint8)
    day = cv2.morphologyEx(toi, cv2.MORPH_OPEN, el(3))          # nét mực mảnh của viền quả cầu (nằm trên vành tròn) thì bỏ
    yy, xx = np.mgrid[0:al.shape[0], 0:al.shape[1]]
    vanh = np.abs(np.hypot(xx - cx, yy - cy) - R) < 3.5
    khung = np.where(vanh, cv2.dilate(day, el(2)).astype(bool) & toi.astype(bool), toi.astype(bool))
    lo = tron.astype(bool) & ~khung
    return float(cx), float(cy), float(R), lo


def luoi_lua(base, d, L, w, seed=0, cong=0.45):
    rng = np.random.default_rng(seed)
    up = np.array([-0.45, -1.0])
    up /= np.linalg.norm(up)
    perp = np.array([-d[1], d[0]])
    ts = np.linspace(0, 1, 70)
    mix = np.clip(ts - 0.3, 0, None) / 0.7 * cong
    dirs = d[None] * (1 - mix[:, None]) + up[None] * mix[:, None]
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    sp = base[None] + np.cumsum(dirs * (L / len(ts)), 0)
    sp += perp[None] * (0.07 * L * np.sin(ts * math.pi * 1.7 + rng.uniform(0, 1)))[:, None]
    wd = w * 0.5 * (1 - ts) ** 0.8 * (1 + 0.25 * np.sin(ts * math.pi))
    dx, dy = np.gradient(sp[:, 0]), np.gradient(sp[:, 1])
    nn = np.hypot(dx, dy) + 1e-6
    A = np.stack([sp[:, 0] - dy / nn * wd, sp[:, 1] + dx / nn * wd], 1)
    B = np.stack([sp[:, 0] + dy / nn * wd, sp[:, 1] - dx / nn * wd], 1)
    return np.concatenate([A, B[::-1]], 0)


def to_E():
    """tờ hướng dẫn E vẽ bằng mã: cầu lửa, tim lửa, bốn lưỡi lửa (gốc ở đáy ô), ba cuộn khói."""
    can = np.full((H, W, 3), 255, np.uint8)

    def vien(m, r=3):
        return m & ~cv2.erode(m.astype(np.uint8), el(r)).astype(bool)

    yy, xx = np.mgrid[0:H, 0:W]
    x, y, w, h = E_O["cau"]
    cx, cy, R = x + w / 2, y + h / 2, w / 2 - 8
    ang = np.arctan2(yy - cy, xx - cx)
    dd = np.hypot(xx - cx, yy - cy)
    m = dd < R
    can[m] = LUA[0]
    can[m & (dd < R * (0.80 + 0.05 * np.sin(ang * 7 + 0.4)))] = LUA[1]
    can[vien(m, 4)] = INK
    x, y, w, h = E_O["tim"]
    cx, cy, R = x + w / 2, y + h / 2, w / 2 - 10
    ang = np.arctan2(yy - cy, xx - cx)
    dd = np.hypot(xx - cx, yy - cy)
    m = dd < R * (0.84 + 0.12 * np.sin(ang * 6 + 1.0))
    can[m] = LUA[2]
    can[vien(m, 3)] = LUA[1]
    for k in range(4):
        x, y, w, h = E_O[f"lua_{k}"]
        m = np.zeros((H, W), np.uint8)
        P = luoi_lua(np.array([x + w * 0.55, y + h - 8.0]), np.array([0.0, -1.0]), h - 30, w * 0.78, seed=3 + k, cong=0.42)
        cv2.fillPoly(m, [P.astype(np.int32)], 1)
        cv2.ellipse(m, (int(x + w * 0.55), int(y + h - 8 - w * 0.2)), (int(w * 0.36), int(w * 0.24)), 0, 0, 360, 1, -1)
        m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 3) > 0.5
        can[m] = LUA[0]
        can[cv2.erode(m.astype(np.uint8), el(w * 0.085)).astype(bool)] = LUA[1]
        can[cv2.erode(m.astype(np.uint8), el(w * 0.19)).astype(bool)] = LUA[2]
        can[vien(m, 4)] = INK
    rng = np.random.default_rng(5)
    for k in range(3):
        x, y, w, h = E_O[f"khoi_{k}"]
        m = np.zeros((H, W), np.uint8)
        for j in range(7):
            a = j / 7 * 2 * math.pi
            r = min(w, h) * rng.uniform(0.22, 0.30)
            cv2.circle(m, (int(x + w / 2 + math.cos(a) * (w / 2 - r - 6)), int(y + h / 2 + math.sin(a) * (h / 2 - r - 6))), int(r), 1, -1)
        cv2.ellipse(m, (int(x + w / 2), int(y + h / 2)), (int(w * 0.3), int(h * 0.3)), 0, 0, 360, 1, -1)
        m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 3) > 0.5
        can[m] = KHOI[k]
        can[vien(m, 4)] = INK
    return Image.fromarray(can, "RGB")


def to(huong=None):
    V = vung()
    os.makedirs(G.MAU, exist_ok=True)
    os.makedirs(GUI, exist_ok=True)
    os.makedirs(G.TAI, exist_ok=True)
    O = {}
    for ma, hang in TO.items():
        can = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        o = {}
        cao = []
        for h_ in hang:
            cs = []
            for r, z in h_:
                im = V[r][1]
                cs.append((r, z, im, int(round(im.width * z)), int(round(im.height * z))))
            cao.append((cs, max(c[4] for c in cs)))
        ke_y = (H - sum(c[1] for c in cao)) // (len(cao) + 1)
        y = ke_y
        for cs, hh in cao:
            ke = (W - sum(c[3] for c in cs)) // (len(cs) + 1)
            x = ke
            for r, z, im, cw, ch in cs:
                y0 = y + (hh - ch) // 2
                if r == "wuqi":                       # xoá quả cầu mắt: chỉ còn khung trượng
                    cx, cy, R, lo = cau_trong_truong(im)
                    a = np.asarray(im).copy()
                    a[cv2.dilate(lo.astype(np.uint8), el(1)).astype(bool)] = (255, 255, 255, 0)
                    n_, lab_, st_, _ = cv2.connectedComponentsWithStats((a[..., 3] > 60).astype(np.uint8), 8)
                    for i_ in range(1, n_):
                        if st_[i_, 4] < 40:               # mẩu vụn còn sót của viền quả cầu
                            a[lab_ == i_] = (255, 255, 255, 0)
                    im = Image.fromarray(a, "RGBA")
                    o["_cau"] = [cx, cy, R]
                big = im.resize((cw, ch), Image.LANCZOS)
                can.alpha_composite(big, (x, y0))
                o[r] = dict(hop=[x, y0, cw, ch], z=z)
                x += cw + ke
            y += hh + ke_y
        p = os.path.join(G.MAU, f"goc_{ma}.png")
        can.convert("RGB").save(p)
        json.dump(o, open(p[:-4] + ".json", "w", encoding="utf-8"), indent=1)
        O[ma] = o
        print(p)
    pe = os.path.join(G.MAU, "goc_E.png")
    to_E().save(pe)
    json.dump({k: dict(hop=list(v), z=1.0) for k, v in E_O.items()}, open(pe[:-4] + ".json", "w", encoding="utf-8"), indent=1)
    print(pe)
    prompt_goc(O)


def nen(A):
    trang = (A.min(2) > 238).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    Hh, Ww = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == Ww or y + h == Hh:
            bg |= lab == i
    return bg


def moi_nhat(tien_to):
    fs = sorted([f for f in os.listdir(G.TAI) if f.startswith(tien_to) and f.endswith(".png")], key=lambda f: os.path.getmtime(os.path.join(G.TAI, f)))
    return os.path.join(G.TAI, fs[-1]) if fs else None


def cat(tos=None):
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    pi = os.path.join(MANH, "_iou.json")
    ious = json.load(open(pi)) if os.path.exists(pi) else {}
    for ma in (tos or list(TO) + ["E"]):
        f = moi_nhat(f"D_{ma}")
        if not f:
            print(f"tờ {ma}: chưa gen")
            continue
        A = np.asarray(Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        o = json.load(open(os.path.join(G.MAU, f"goc_{ma}.json"), encoding="utf-8"))
        Gd = np.asarray(Image.open(os.path.join(G.MAU, f"goc_{ma}.png")).convert("RGB")).astype(np.int32)
        bg = nen(A)
        fg = ~bg
        fgG = Gd.min(2) < 238
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        so = []
        print(f"tờ {ma}: {os.path.basename(f)}")
        for r, d in o.items():
            if r.startswith("_"):
                continue
            x, y, cw, ch = d["hop"]
            pad = 14 if ma != "E" else 26
            x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + cw + pad), min(H, y + ch + pad)
            gm = cv2.dilate(fgG[y0:y1, x0:x1].astype(np.uint8), el(10)).astype(bool)
            sub = lab[y0:y1, x0:x1]
            ids = [i for i in np.unique(sub[gm]) if i > 0 and st[i, 4] > 60]
            m = np.isin(lab, ids)
            m[:y0] = m[y1:] = False
            m[:, :x0] = m[:, x1:] = False
            if ma == "E":                                   # mảnh mới: lấy theo khung bao của chính nó
                ys, xs = np.nonzero(m)
                x, y, cw, ch = int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)
            rgb = A[y:y + ch, x:x + cw].astype(np.uint8)
            mm = m[y:y + ch, x:x + cw]
            if r == "wuqi":                                 # lòng khung trượng (chỗ quả cầu cũ): giấy trắng khép kín → trong suốt
                tr = (A[y:y + ch, x:x + cw].min(2) > 236)
                n2, lab2, st2, _ = cv2.connectedComponentsWithStats((tr & mm).astype(np.uint8), 4)
                for i2 in range(1, n2):
                    if st2[i2, 4] > 350:
                        mm = mm & ~(lab2 == i2)
            al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
            vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
            sang = rgb.min(2).astype(np.float32)
            al = np.where(vien, np.minimum(al, np.clip((250.0 - sang) / 70.0, 0, 1)), al)
            im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
            if ma == "E":
                im.save(os.path.join(MANH, r + ".png"))
                print(f"  {r:14s} {im.size}")
                so.append((im.convert("RGB"), im))
                continue
            goc = V[r][1]
            tw, th = goc.width * RES, goc.height * RES
            im2 = im.convert("RGBa").resize((tw, th), Image.LANCZOS).convert("RGBA")
            a2 = np.asarray(im2).copy()
            ag = np.asarray(goc.resize((tw, th), Image.LANCZOS))[..., 3] > 60
            if r == "wuqi":
                cx, cy, R, lo = cau_trong_truong(goc)
                ag &= ~cv2.resize(lo.astype(np.uint8), (tw, th), interpolation=cv2.INTER_NEAREST).astype(bool)
            gioi = cv2.dilate(ag.astype(np.uint8), el(3)).astype(bool)
            a2[..., 3] = np.where(gioi, a2[..., 3], 0)
            if r == "shenti":                               # lỗ của dây bện: giấy trắng → trong suốt (dây vàng không có chỗ nào trắng)
                tr2 = a2[..., :3].astype(np.int32).min(2) > 228
                a2[..., 3] = np.where(cv2.dilate(tr2.astype(np.uint8), el(1)).astype(bool) & ~cv2.erode(ag.astype(np.uint8), el(2)).astype(bool) | tr2, 0, a2[..., 3])
            Image.fromarray(a2, "RGBA").save(os.path.join(MANH, r + ".png"))
            pj = os.path.join(MANH, "_tam.json")
            if os.path.exists(pj):
                json.dump([x for x in json.load(open(pj)) if x != r], open(pj, "w"))
            a = mm
            b = fgG[y:y + ch, x:x + cw]
            iou = float((a & b).sum()) / max(1, (a | b).sum())
            ious[r] = round(iou, 3)
            vis = np.full((ch, cw, 3), 255, np.uint8)
            vis[a & b] = (170, 170, 170)
            vis[b & ~a] = (230, 60, 60)
            vis[a & ~b] = (60, 190, 60)
            so.append((Image.fromarray(vis), Image.fromarray(a2, "RGBA")))
            print(f"  {r:14s} IoU {iou:.3f}")
        w_ = sum(max(s[0].width, s[1].width) + 10 for s in so)
        hh = max(s[0].height for s in so)
        h2 = max(s[1].height for s in so)
        out = Image.new("RGB", (w_ + 10, hh + h2 + 30), (150, 150, 150))
        xx = 10
        for vis, kh in so:
            out.paste(vis, (xx, 10))
            out.paste(kh, (xx, hh + 20), kh)
            xx += max(vis.width, kh.width) + 10
        out.save(os.path.join(MANH, f"_so_{ma}.png"))
        print(os.path.join(MANH, f"_so_{ma}.png"))
    json.dump(ious, open(pi, "w"), indent=1)


BG = ("Plain pure-white background (#FFFFFF), no paper grain outside the pieces, no labels, no numbers, no frame, nothing added.")


def o_E(r):
    x, y, w, h = E_O[r]
    return f"about x = {x} to x = {x + w}, y = {y} to y = {y + h}"


def prompt_E(concept=None):
    """tờ E: mảnh MỚI của mình (con gốc không có): cầu lửa, tim lửa, bốn lưỡi lửa, ba cuộn khói. Ảnh mẫu: tờ bố trí vẽ bằng mã + bản concept
    (nét, cách vẽ lửa). Không phụ thuộc dáng áo / mặt nên gen trước được."""
    concept = concept or CONCEPT
    mau = os.path.join(G.MAU, "goc_E.png")
    out = os.path.join(G.TAI, "D_E.png")
    p = os.path.join(GUI, "luot_4_da_E.txt")
    os.makedirs(GUI, exist_ok=True)
    R = [(mau, "LAYOUT SHEET, 1536x1024, white background, a rough flat computer-made sketch: WHERE each of the nine pieces goes on the "
               "sheet and HOW BIG it is: a big round ball (upper left), a smaller star-like yellow blob under it, four upright flame "
               "tongues of decreasing size (top row), three round lumpy puffs from dark to light grey (bottom row). Take only the "
               "placement, the size and the kind of colour of each piece; the sketch shapes are crude (the flames look like claws): "
               "design the real shapes yourself as described."),
         (concept, "a picture of OUR character (a fire-mage spirit), 1536x1024, white background: use it ONLY for the drawing style: the "
                   "wobbly dark-brown ink outline, the crayon hatching, and the way FIRE is drawn (three nested flat colour zones with "
                   "wavy borders, no glow). The ball of fire in its staff and the flames above it are what these pieces will rebuild.")]
    t = ["IMAGES (attached in this order; open each from its path):"]
    t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en) in enumerate(R, 1)]
    t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
          "If a file with that name already exists, save as D_E_2.png, D_E_3.png ... in the same folder. Do not edit, move or delete any "
          "other file.", "",
          "TASK: draw a sheet of NINE SEPARATE PIECES on a pure-white 1536x1024 canvas. They are the loose parts of an animated ball of "
          "fire (the burning orb in the head of a mage's staff): a 2D skeleton will stack them (smoke behind, then the flame tongues, then "
          "the ball, then its bright heart) and wave them. Each piece is drawn ALONE, complete, not touching any other piece, at the "
          "place and size of the layout sheet (image 1), with at least 40 px of white between pieces.", "",
          "THE PIECES (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):",
          f"1. THE BALL ({o_E('cau')}): a perfectly round ball of fire: a ring of red-orange (#E0441F) along the rim and a big orange "
          "(#F7902A) inside, the border between the two colours wavy like small flame tongues. A closed ink outline all the way round "
          "the circle. No face, no highlight, nothing else on it.",
          f"2. THE HEART ({o_E('tim')}): the bright core that sits on the ball: ONE soft blob of yellow (#FFD45A) with five or six rounded "
          "wavy lobes (like a small flower or a splash), a slightly paler yellow (#FFE89A) spot in its middle. NO dark ink outline: its "
          "edge is only a thin orange (#F7902A) line.",
          f"3. FLAME TONGUE 1, the tallest ({o_E('lua_0')}): ONE single upright flame, drawn like a real hand-drawn flame, NOT a horn "
          "or a claw: a thick rounded base at the BOTTOM, a body that sways in a soft S-curve, and one sharp tip at the TOP curling a "
          "little to the left; one small side lick halfway up is allowed. Three nested flat colour zones following its shape: "
          "red-orange (#E0441F) outside, orange (#F7902A), and a yellow (#FFD45A) zone inside that starts at the base and ends in a "
          "point below the tip. A closed ink outline all the way round, also round the base.",
          f"4. FLAME TONGUE 2 ({o_E('lua_1')}): the same kind of single flame, a little smaller, its S-curve different from tongue 1.",
          f"5. FLAME TONGUE 3 ({o_E('lua_2')}): the same, smaller, its tip curling a little to the RIGHT.",
          f"6. FLAME TONGUE 4, the smallest ({o_E('lua_3')}): the same, short and plump.",
          f"7. SMOKE PUFF 1, the darkest ({o_E('khoi_0')}): a round, lumpy puff of thick smoke like a small cloud: six or seven rounded "
          "lobes around its edge, two or three short curl lines inside. Flat charcoal black (#3A343A). A closed ink outline.",
          f"8. SMOKE PUFF 2 ({o_E('khoi_1')}): the same kind of puff, a different lumpy shape, flat dark grey (#68626A).",
          f"9. SMOKE PUFF 3, the lightest ({o_E('khoi_2')}): the same kind, smaller and wispier, flat mid grey (#96919A).", "",
          "STYLE: hand-drawn like image 2: wobbly dark-brown ink outline (#2B2118, about 6 px), every area ONE flat colour with visible "
          "coloured-pencil / wax-crayon hatching; bold, simple, readable shapes. FLAT COLOUR ONLY: the fire looks hot only because its "
          "colours are bright: NO glow, NO halo, NO gradients, NO blur, NO highlights, NO shadows, no sparks, no embers, no extra bits.",
          "", BG]
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 4: mảnh cầu lửa")[0].rstrip("\n") if os.path.exists(hd) else ""
    gd = [cu, "", "## Lượt 4: mảnh cầu lửa, lưỡi lửa, khói (tờ E, 2026-11-13)", "",
          "Mảnh MỚI của mình (con gốc là một con mắt vẽ liền trong ảnh trượng): cầu lửa, tim lửa, bốn lưỡi lửa, ba cuộn khói. Rig xếp khói → "
          "lưỡi lửa → cầu → tim → khung trượng; lửa uốn bằng xương, khói bốc sau cầu lửa. Không phụ thuộc dáng áo / mặt nên gen trước.", "",
          f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
          "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
          f"| 1 | `{Wp(mau)}` | Tờ bố trí vẽ bằng mã (1536 × 1024, nền trắng): quả cầu cam viền đỏ cam (trên trái), đốm vàng hình sao bo tròn "
          "(dưới nó), bốn lưỡi lửa đứng nhỏ dần (hàng trên), ba cuộn tròn xám từ sẫm tới nhạt (hàng dưới). Chỉ lấy chỗ đặt, cỡ, loại màu |",
          f"| 2 | `{Wp(concept)}` | Bản concept của mình (1536 × 1024, nền trắng): pháp sư lửa cầm trượng có cầu lửa. Chỉ lấy nét bút, vân sáp, cách vẽ lửa |",
          "", "Kiểm: đủ 9 mảnh rời nhau đúng chỗ tờ bố trí; cầu tròn hai vùng màu viền mực kín; tim vàng không viền mực; bốn lưỡi lửa đơn (gốc tròn "
          "ở đáy, ngọn nhọn ở trên, ba vùng màu, viền kín cả gốc), không ra sừng / vuốt; ba cuộn khói than, xám sẫm, xám; tô phẳng, không quầng sáng. "
          "Cắt: `py -3 -I ArtGen/Spine/phap_lua_da.py cat E`."]
    open(hd, "w", encoding="utf-8", newline="\n").write("\n".join(gd) + "\n")
    print(p)


# ---------------------------------------------------------------- tờ B, C, D: reskin trên mảnh GỐC (giữ hình bóng)
def cho(o, r):
    x, y, cw, ch = o[r]["hop"]
    return f"about x = {x} to x = {x + cw}, y = {y} to y = {y + ch}"


CHUNG = (
    "TASK: RESKIN. Image 1 is a sheet of separate body PARTS of a 2D animation puppet (a floating robed spirit mage), each part drawn "
    "alone on white. Redraw the SAME sheet with every part REPAINTED as described below, so that the parts can be put back on the same "
    "puppet. For EVERY part keep exactly: its silhouette (the same outline), its size, its orientation and its place on the sheet (if the "
    "new picture were laid over image 1, every part must coincide with the old one). Do NOT merge parts, do NOT add parts, do NOT move, "
    "rotate or straighten parts. Pure white (#FFFFFF) between the parts.")
STYLE = (
    "NEW LOOK (the same for all parts; see image 2, the approved picture of OUR character, for the exact colours and drawing style): "
    "hand-drawn on paper: a wobbly dark-brown ink outline (#2B2118, about {px} px on this sheet) running all the way round every part "
    "exactly on its silhouette, a few thinner ink lines inside where listed, and every area filled with ONE flat colour with visible "
    "coloured-pencil / wax-crayon hatching. The parts of image 1 are painted in a smooth digital cel style with grey-violet and white "
    "colours and light / dark shading shapes: do NOT copy that painting style, those colours or those shading shapes; no shading, no "
    "highlights, no gradients, no glow, no shadows: flat colour only. Only the colours listed: no blue, purple, violet, pink or green.")

MO_TA = {
    "B": [
        ("maofa_01", "THE HAIR MANE (the big piece of the top row: a huge wave of hair with pointed locks, a hooked curl at its upper "
                     "left, a notch in the middle of its lower edge and a pointed tuft at the right): flat pale ash-cream (#E9E1D2). "
                     "Inside, six to eight long flowing STRAND LINES in a slightly darker warm grey-brown (#B9A98F), following the sweep "
                     "of the locks from the lower right to the upper left. No white, no lilac."),
        ("shouzhangR_01", "A WISPY WRIST (a rounded lump with a thin curling tail at the right): a wisp of pale smoke: flat pale "
                          "ash-cream (#E9E1D2), one or two short curl lines (#B9A98F) inside."),
        ("shouzhangL_01", "A SECOND WISPY WRIST (a lump at the top that trails down into a wavy tail with a curl at the bottom): the "
                          "same pale ash-cream smoke, two short curl lines."),
        ("shenti", "A BRAIDED CORD (two flat straps coming down from the upper left and upper right, crossing and twisting into a "
                   "zigzag braid that ends in a point at the bottom): flat pale gold (#E2B24C); keep the ink lines where the straps "
                   "cross over each other and the small openings of the braid (white)."),
        ("zhuangshi_02", "A FOUR-POINTED STAR SPIKE (like a compass needle, the lower point longest): flat charcoal black (#2F2A30) "
                         "with one thin ridge line down its middle in a lighter grey (#5A5258)."),
        ("zhuangshi_01", "A SECOND FOUR-POINTED STAR SPIKE: the same."),
    ],
    "C": [(f"shouzhi{b}_{i:02d}", t) for b, i, t in
          [("R", 1, "a finger segment"), ("R", 2, "a finger segment"), ("R", 3, "a finger segment"), ("R", 4, "a finger segment")]
          + [("L", i, "a claw segment") for i in range(1, 11)]],
    "D": [
        ("wuqi", "THE STAFF, alone (the only part on this sheet): a tall thin staff lying diagonally. Its head (upper left) is an "
                 "angular claw-like FRAME: a pointed hood, a sharp spike reaching to the left across the round opening, a prong under "
                 "the opening pointing left, and two thin icicle spikes hanging down; then the long thin shaft runs down to the right "
                 "and ends in a zigzag lightning-bolt tip. Repaint it flat charcoal black (#2F2A30) with a few thin lighter-grey "
                 "(#5A5258) ridge lines along the frame and one along the shaft. VERY IMPORTANT: the big ROUND OPENING inside the "
                 "frame (where a ball will be placed behind it later) stays EMPTY PURE WHITE, exactly as in image 1: do NOT draw a "
                 "ball, an eye, a gem or fire in it. The ink outline also runs along the inner edges of the frame around the opening."),
    ],
}
VI = {"B": "bờm tóc, hai cổ tay khói, dây bện ngực, hai gai sao", "C": "bốn đốt ngón tay trượng + mười đốt vuốt tay vuốt (phóng 6 lần)",
      "D": "khung trượng (đã xoá quả cầu mắt, lòng khung để trắng)"}
SO_MANH = {"B": "Six parts: top row the big hair mane; bottom row two wispy wrist pieces, a braided cord and two small four-pointed "
                "star spikes.",
           "C": "Fourteen small parts drawn very big, in three rows (4 + 5 + 5): the finger and claw segments of two clawed hands "
                "(short knuckle blocks and long curved pointed nails).",
           "D": "One part: a tall staff whose claw-like head has an empty round opening."}
PX = {"B": "6 (about 8 on the two wrists, the cord and the stars of the bottom row)", "C": "11", "D": "6"}


def prompt_goc(O):
    gd_them = ["", "## Lượt 5: da các mảnh giữ hình bóng con gốc (tờ B, C, D; 2026-11-13)", "",
               "Concept đã duyệt: `tai_ve/L1_duyet.png` (bản G: mũ trùm mắt lửa trên áo cháy thành lửa). Tóc, hai cổ tay khói, dây bện, gai sao, "
               "ngón / vuốt, khung trượng giữ hình bóng part gốc: mỗi tờ là các mảnh GỐC cắt ra từ rig (phóng to), GPT vẽ lại da đúng chỗ, đúng "
               "cỡ, đúng hình bóng. Ảnh mảnh gốc là của game tham khảo: chỉ dùng trong máy làm mẫu, không đăng công khai.", ""]
    for ma, o in O.items():
        mau = os.path.join(G.MAU, f"goc_{ma}.png")
        out = os.path.join(G.TAI, f"D_{ma}.png")
        p = os.path.join(GUI, f"luot_5_da_{ma}.txt")
        R = [(mau, "the PARTS SHEET, 1536x1024, white background: separate parts of the puppet, each drawn alone, at the exact size and "
                   "place to keep. " + SO_MANH[ma],
              f"Tờ mảnh gốc cắt từ rig con gốc (1536 × 1024, nền trắng), phóng 2,8–6 lần: {VI[ma]}. Hình cel số màu xám tím, trắng"),
             (CONCEPT, "the APPROVED picture of OUR character, 1536x1024, white background: a floating fire-mage spirit in a charcoal "
                       "hood with burning eyes, a pale ash-cream mane, a charcoal-black staff holding a ball of fire, charcoal-black "
                       "clawed hands with pale smoke wrists, a pale gold braid and two charcoal star spikes on the chest. Take from it "
                       "ONLY the colours, the materials and the hand-drawn look (wobbly brown ink line, crayon hatching, flat colour). "
                       "Do NOT copy its shapes or its pose: the shapes come from image 1.",
              "Concept đã duyệt của mình (bản G, 1536 × 1024, nền trắng): chỉ lấy màu, chất liệu, nét vẽ tay")]
        t = ["IMAGES (attached in this order; open each from its path):"]
        t += [f"image {i} = {Wp(r)}: {en}" for i, (r, en, _) in enumerate(R, 1)]
        t += ["", f"SAVE: save it as a PNG to {Wp(out)}",
              f"If a file with that name already exists, save as D_{ma}_2.png, D_{ma}_3.png ... in the same folder. Do not edit, move or "
              "delete any other file.", "", CHUNG, "", STYLE.format(px=PX[ma]),
              "", "THE PARTS (coordinates are pixels on the 1536x1024 sheet, x from the left, y from the top):"]
        if ma == "C":
            t += ["All fourteen parts are the finger and claw SEGMENTS of the two clawed hands: short blocky knuckle segments and long "
                  "curved pointed nail segments. Repaint EVERY one of them flat charcoal black (#2F2A30), with a closed ink outline; on "
                  "each long nail one thin lighter-grey (#5A5258) ridge line along its curve; no grey-to-white fading, no lighter tips. "
                  "Each part stays exactly where it is:"]
            t += [f"{i}. ({cho(o, r)}) {mt}." for i, (r, mt) in enumerate(MO_TA[ma], 1)]
        else:
            t += [f"{i}. ({cho(o, r)}) {mt}" for i, (r, mt) in enumerate(MO_TA[ma], 1)]
        t += ["", BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        print(p)
        gd_them += [f"### Tờ `{ma}`: {VI[ma]}", "",
                    f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. GPT tự mở ảnh mẫu và lưu ảnh vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
                    "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|"]
        gd_them += [f"| {i} | `{Wp(r)}` | {vi} |" for i, (r, _, vi) in enumerate(R, 1)]
        gd_them += [""]
    gd_them += ["Kiểm: mỗi mảnh ĐÚNG chỗ, đúng cỡ, đúng hình bóng mảnh gốc; tóc và cổ tay tro kem, dây bện vàng nhạt, sao + ngón + vuốt + trượng "
                "đen than; lòng khung trượng để TRẮNG; không còn xám tím, trắng lạnh; tô phẳng, nét bút nâu rung. Cắt: "
                "`py -3 -I ArtGen/Spine/phap_lua_da.py cat B C D`."]
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 5: da các mảnh giữ hình bóng")[0].rstrip("\n") if os.path.exists(hd) else ""
    open(hd, "w", encoding="utf-8", newline="\n").write("\n".join([cu] + gd_them) + "\n")


# ---------------------------------------------------------------- mảnh ĐỔI DÁNG: gen "đúng chỗ, đúng cỡ" từ concept đã duyệt
TU_CONCEPT = {
    "dau_lua": dict(
        vi="chỉ còn cái đầu mũ trùm (trên) và khối lưỡi lửa dưới áo (dưới), mỗi thứ vẽ đủ phần khuất",
        en=("KEEP ONLY TWO THINGS, each redrawn COMPLETE:\n"
            "(1) THE HOODED HEAD: the charcoal hood with its gold hem and its pointed tip, the dark face opening with the two burning "
            "eyes, the gem on the brow, and the two short lappets hanging at the sides of the face opening. Complete the hood into ONE "
            "closed shape with an ink outline all the way round: where the hair, the shoulders or the braid covered its edge, finish "
            "the edge as a simple rounded hood (the lappets end in soft points at about y = 545).\n"
            "(2) THE MASS OF FLAMES under the robe: all the flame tongues that stream down below the burnt edge of the crimson robe. "
            "Complete it into ONE closed flame shape with an ink outline all the way round: the tongues join in a broad body of fire "
            "that continues UPWARD behind where the robe was, up to about y = 600, with a simple rounded top (red-orange outside, "
            "orange, yellow inside, the same three flat colours); where the staff shaft crossed the flames, fill in the flames.\n"
            "The two things do not touch each other.")),
    "ao": dict(
        vi="chỉ còn áo vải đỏ thẫm (thân trên), vẽ đủ cả phần bị áo vai, dây bện, sao, trượng, tay che",
        en=("KEEP ONLY THE CRIMSON ROBE CLOTH (the dark-crimson upper body with its wavy burnt lower edge and its thin charred rim), "
            "redrawn COMPLETE as ONE closed shape with an ink outline all the way round: a simple bell-shaped body that starts as a "
            "rounded neck at about x = 800 to x = 930, y = 470 (it was hidden under the hood and the mantle) and widens down to the "
            "burnt edge exactly where it is in image 1. Everywhere the mantle, the braid, the star spikes, the staff, the staff hand or "
            "the wisps covered it, fill in plain flat crimson cloth (#A32E22) with the same crayon hatching; keep the burnt edge and "
            "its charred rim exactly as drawn.")),
    "vai": dict(
        vi="chỉ còn áo vai than viền vàng (cả hai vai + đuôi nhọn dài bên trái), vẽ đủ phần bị tóc, mũ, tay, trượng che",
        en=("KEEP ONLY THE CHARCOAL MANTLE (the shoulder cape of charcoal cloth with its pale gold trim along the lower edge, lying "
            "over both shoulders, and its long narrow pointed tail flying out to the lower left), redrawn COMPLETE as ONE closed shape "
            "with an ink outline all the way round: the two shoulder halves join in a collar behind where the hood was (the collar "
            "top at about y = 470, between about x = 790 and x = 940); in front, between the two halves, the mantle is OPEN in a "
            "V-shape exactly as in image 1 (leave that V white). Everywhere the hair, the hood, the wispy wrists, the staff or the "
            "staff hand covered it, fill in plain flat charcoal (#3C353B) and continue the gold trim line smoothly; the tail stays "
            "exactly where it is.")),
    "toc": dict(
        vi="chỉ còn bờm tóc tro kem, vẽ đủ phần bị mũ trùm, áo vai, đầu trượng, cổ tay che",
        en=("KEEP ONLY THE HAIR MANE (the huge pale ash-cream mane with its flowing strand lines: the big wave sweeping up and back to "
            "the upper left with its hooked curl, and the curls at the right behind the claw hand), redrawn COMPLETE as ONE closed shape "
            "with an ink outline all the way round: everywhere the hood, the mantle, the staff head, the fire or the wispy wrist covered "
            "it, continue the hair (same flat pale ash-cream #E9E1D2, same flowing strand lines): behind the hood the mane is one full "
            "mass down to about y = 520, where it ends in a simple soft lower edge (it will be hidden under the hood and the mantle). "
            "The outer outline of the mane (top, left and right) stays exactly where it is in image 1.")),
}


def prompt_concept():
    os.makedirs(GUI, exist_ok=True)
    gd = ["", "## Lượt 6: mảnh đổi dáng, gen đúng chỗ đúng cỡ từ concept (2026-11-13)", "",
          "Đầu mũ trùm, khối lửa dưới áo, áo vải, áo vai khác hẳn hình bóng part gốc nên không vẽ trên tờ mảnh gốc: mỗi lượt vẽ lại concept, chỉ "
          "giữ một (hai) mảnh ĐÚNG CHỖ, ĐÚNG CỠ và vẽ đủ phần khuất. Rig cắt theo cụm liền, đặt theo toạ độ concept.", ""]
    for ten, d in TU_CONCEPT.items():
        out = os.path.join(G.TAI, f"M_{ten}.png")
        p = os.path.join(GUI, f"luot_6_manh_{ten}.txt")
        t = ["IMAGES (attached in this order; open each from its path):",
             f"image 1 = {Wp(CONCEPT)}: the approved picture of OUR character, 1536x1024, white background: a floating fire-mage spirit: "
             "a charcoal hood with burning eyes, a big pale mane, a staff at the left holding a ball of fire, a staff hand, an open claw "
             "hand at the right, a gold braid and two star spikes on the chest, a charcoal mantle with gold trim and a long pointed tail "
             "at the left, a crimson robe with a burnt lower edge, and a mass of flames streaming down below the robe.",
             "", f"SAVE: save it as a PNG to {Wp(out)}",
             f"If a file with that name already exists, save as M_{ten}_2.png, M_{ten}_3.png ... in the same folder. Do not edit, move or "
             "delete any other file.", "",
             "TASK: redraw image 1 on the same 1536x1024 pure-white canvas, keeping ONLY the piece(s) named below, in EXACTLY THE SAME "
             "POSITION and at EXACTLY THE SAME SIZE as in image 1 (if the new picture were laid over image 1, the visible parts of the "
             "piece must coincide), and REMOVE everything else (pure white). The piece will be cut out and animated on a 2D skeleton, "
             "so the parts of it that were hidden behind other things must be drawn too.", "",
             d["en"], "",
             "STYLE: exactly as image 1: the same colours, the same wobbly dark-brown ink outline (#2B2118, about 5 px), flat colours "
             "with visible crayon hatching; NO shading, NO shadows, NO highlights, NO glow, NO gradients. Do not add anything that is "
             "not listed (no hands, no hair, no staff, no braid, no sparks).", "", BG]
        open(p, "w", encoding="utf-8", newline="\n").write("\n".join(t) + "\n")
        print(p)
        gd += [f"### `{ten}`: {d['vi']}", "",
               f"**Chỉ gửi GPT đường dẫn:** `{Wp(p)}`. Ảnh lưu vào `{Wp(out)}` (trùng tên thì `_2`, `_3`…).", "",
               "| Ảnh mẫu | Đường dẫn | Trông như thế nào |", "|---|---|---|",
               f"| 1 | `{Wp(CONCEPT)}` | Concept đã duyệt (bản G, 1536 × 1024, nền trắng): pháp sư lửa mũ trùm mắt lửa, áo vai than viền vàng, áo đỏ cháy thành lửa |", ""]
    gd += ["Kiểm: mảnh nằm đúng chỗ concept (chồng lên phải trùng phần lộ), một hình kín viền mực, phần khuất đã vẽ đủ, không dính thứ khác. "
           "Cắt: `py -3 -I ArtGen/Spine/phap_lua_da.py cat_concept`."]
    hd = os.path.join(GUI, "HUONG_DAN.md")
    cu = open(hd, encoding="utf-8").read().split("\n## Lượt 6: mảnh đổi dáng")[0].rstrip("\n") if os.path.exists(hd) else ""
    open(hd, "w", encoding="utf-8", newline="\n").write("\n".join([cu] + gd) + "\n")


def tg_concept():
    """đổi toạ độ concept (px) → thế giới rig (đơn vị, y lên): concept = s · sơ đồ + (dx, dy); sơ đồ = phap_lua_bo_cuc.khung_T."""
    import phap_lua_bo_cuc as BC
    SC, T = BC.khung_T()
    o = T(np.array([0.0, 0.0]))                      # px sơ đồ của gốc toạ độ rig
    k = json.load(open(os.path.join(G.MAU, "khop_concept.json")))
    s, dx, dy = k["s"], k["dx"], k["dy"]
    ti = 1.0 / (SC * s)                              # đơn vị rig cho mỗi px concept
    return (lambda x, y: (((x - dx) / s - o[0]) / SC, (o[1] - (y - dy) / s) / SC)), ti


def cat_concept():
    """cắt các ảnh M_<tên> (mảnh đúng chỗ trên khung concept) → manh/<mảnh>.png + manh/dat_moi.json (rig đọc: slot nào dùng lưới của mình)."""
    os.makedirs(MANH, exist_ok=True)
    tg, ti = tg_concept()
    moi = {}

    def lay(ten_anh, chon):
        f = moi_nhat(f"M_{ten_anh}")
        if not f:
            print(f"  M_{ten_anh}: chưa gen")
            return []
        A = np.asarray(Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS)).astype(np.int32)
        fg = ~nen(A)
        fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, el(1)).astype(bool)
        n, lab, st, _ = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
        cum = sorted([i for i in range(1, n) if st[i, 4] > 2500], key=lambda i: st[i, 1])     # trên → dưới
        out = []
        for ten, k in chon:
            if k >= len(cum):
                print(f"  M_{ten_anh}: thiếu cụm cho {ten}")
                continue
            i = cum[k]
            m = lab == i
            for j in range(1, n):                     # mẩu nhỏ sát cụm thì nhập vào
                if j != i and st[j, 4] <= 2500 and (cv2.dilate(m.astype(np.uint8), el(14)).astype(bool) & (lab == j)).any():
                    m |= lab == j
            ys, xs = np.nonzero(m)
            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
            mm = m[y0:y1, x0:x1]
            al = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
            rgb = A[y0:y1, x0:x1].astype(np.uint8)
            vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
            al = np.where(vien, np.minimum(al, np.clip((250.0 - rgb.min(2).astype(np.float32)) / 70.0, 0, 1)), al)
            im = Image.fromarray(np.dstack([rgb, (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA")
            out.append((ten, im, int(x0), int(y0)))
            print(f"  {ten:10s} từ {os.path.basename(f)}: {im.size} ở ({x0}, {y0})")
        return out

    def ghi(ten, im, x0, y0):
        im.save(os.path.join(MANH, ten + ".png"))
        X, Y = tg(x0, y0)
        return dict(anh=ten, goc=[round(X, 2), round(Y, 2)], ti=round(ti, 5), px=1.25)

    for ten, im, x0, y0 in lay("dau_lua", [("dau", 0), ("lua_ao", 1)]):
        moi[ten] = ghi(ten, im, x0, y0)
    for ten, im, x0, y0 in lay("ao", [("ao", 0)]):
        moi[ten] = ghi(ten, im, x0, y0)
    for ten, im, x0, y0 in lay("toc", [("toc", 0)]):
        moi[ten] = ghi(ten, im, x0, y0)
    for ten, im, x0, y0 in lay("vai", [("vai", 0)]):
        # tách hai nửa (trái bám lưới khăn vai trái pifeng_02, phải bám pifeng_01), chờm nhau 36 px quanh đường giữa cổ
        a = np.asarray(im)
        xg = int(round(865 - x0))                    # đường giữa cổ trên concept ≈ x = 865
        tr, ph = a.copy(), a.copy()
        tr[:, min(a.shape[1], xg + 36):, 3] = 0
        ph[:, :max(0, xg - 36), 3] = 0
        moi["vai_trai"] = ghi("vai_trai", Image.fromarray(tr, "RGBA"), x0, y0)
        moi["vai_phai"] = ghi("vai_phai", Image.fromarray(ph, "RGBA"), x0, y0)
    json.dump(moi, open(os.path.join(MANH, "dat_moi.json"), "w", encoding="utf-8"), indent=1)
    print(os.path.join(MANH, "dat_moi.json"), list(moi))


def tam_than(chi=None):
    """mảnh TẠM tô bằng mã cho các part một màu đen than (khung trượng, ngón, vuốt) khi Codex hết hạn mức: đúng hình bóng part gốc, tô than
    (72, 62, 66: màu đo trên concept) có vân sáp chéo, viền mực nâu rung 3–5 px. Ghi tên vào manh/_tam.json; `cat C D` ghi đè khi tờ GPT về."""
    V = vung()
    os.makedirs(MANH, exist_ok=True)
    rng = np.random.default_rng(7)
    ds = []
    for r, (a, im) in V.items():
        if not (r == "wuqi" or r.startswith("shouzhi")) or (chi and r not in chi):
            continue
        A = np.asarray(im).copy()
        if r == "wuqi":
            _, _, _, lo = cau_trong_truong(im)
            A[cv2.dilate(lo.astype(np.uint8), el(1)).astype(bool), 3] = 0
            n_, lab_, st_, _ = cv2.connectedComponentsWithStats((A[..., 3] > 60).astype(np.uint8), 8)
            for i_ in range(1, n_):
                if st_[i_, 4] < 40:
                    A[lab_ == i_, 3] = 0
        w, h = im.width * RES, im.height * RES
        al = cv2.resize(A[..., 3].astype(np.float32) / 255.0, (w, h), interpolation=cv2.INTER_CUBIC)
        al = cv2.GaussianBlur(al, (0, 0), 1.3)
        m = al > 0.5
        # vân sáp chéo: nhiễu kéo dài theo đường chéo
        nz = rng.normal(0, 1, (h + 64, w + 64)).astype(np.float32)
        k = np.zeros((15, 15), np.float32)
        for i in range(15):
            k[14 - i, i] = 1 / 15
        nz = cv2.filter2D(nz, -1, k)[32:32 + h, 32:32 + w]
        nz = nz / (nz.std() + 1e-6)
        rgb = np.clip(np.array([72, 62, 66], np.float32)[None, None] * (1.0 + 0.09 * nz[..., None]) + 3.0 * nz[..., None], 0, 255)
        # viền mực rung: bề dày đổi chậm dọc mép
        dist = cv2.distanceTransform(m.astype(np.uint8), cv2.DIST_L2, 5)
        g = cv2.GaussianBlur(rng.normal(0, 1, (h, w)).astype(np.float32), (0, 0), 9)
        day = np.clip(3.6 + 1.1 * g / (g.std() + 1e-6), 2.6, 5.0)
        muc = m & (dist <= day)
        rgb[muc] = (48, 27, 12)
        a8 = (np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.7), 0, 1) * 255).astype(np.uint8)
        Image.fromarray(np.dstack([rgb.astype(np.uint8), a8]), "RGBA").save(os.path.join(MANH, r + ".png"))
        ds.append(r)
    pj = os.path.join(MANH, "_tam.json")
    cu = json.load(open(pj)) if os.path.exists(pj) else []
    json.dump(sorted(set(cu) | set(ds)), open(pj, "w"))
    print("mảnh tạm tô bằng mã:", ", ".join(ds))


def tam():
    """bộ mảnh TẠM để dựng thử rig trước khi có da của mình: ảnh part GỐC × RES (trượng đã xoá quả cầu) + mảnh tờ E vẽ bằng mã →
    inbox/phap_lua_1/manh_goc/ (chỉ để thử trong máy)."""
    V = vung()
    ra = os.path.join(G.BASE, "manh_goc")
    os.makedirs(ra, exist_ok=True)
    for r, (a, im) in V.items():
        if r == "wuqi":
            cx, cy, R, lo = cau_trong_truong(im)
            arr = np.asarray(im).copy()
            arr[cv2.dilate(lo.astype(np.uint8), el(1)).astype(bool)] = (255, 255, 255, 0)
            im = Image.fromarray(arr, "RGBA")
        im.convert("RGBa").resize((im.width * RES, im.height * RES), Image.LANCZOS).convert("RGBA").save(os.path.join(ra, r + ".png"))
    E = np.asarray(to_E()).astype(np.int32)
    for r, (x, y, w, h) in E_O.items():
        sub = E[y:y + h, x:x + w]
        m = sub.min(2) < 238
        ys, xs = np.nonzero(m)
        sub, m = sub[ys.min():ys.max() + 1, xs.min():xs.max() + 1], m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        al = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.8)
        Image.fromarray(np.dstack([sub.astype(np.uint8), (np.clip(al, 0, 1) * 255).astype(np.uint8)]), "RGBA").save(os.path.join(ra, r + ".png"))
    print(ra, len(os.listdir(ra)), "ảnh")


if __name__ == "__main__":
    if sys.argv[1:2] == ["tam"]:
        tam()
    elif sys.argv[1:2] == ["tam_than"]:
        tam_than(sys.argv[2:] or None)
    elif sys.argv[1:2] == ["prompt_E"]:
        prompt_E(*sys.argv[2:3])
    elif sys.argv[1:2] == ["prompt_concept"]:
        prompt_concept()
    elif sys.argv[1:2] == ["cat_concept"]:
        cat_concept()
    elif sys.argv[1:2] == ["to"]:
        to(*sys.argv[2:3])
    elif sys.argv[1:2] == ["cat"]:
        cat(sys.argv[2:] or None)
    else:
        print(__doc__)
