# -*- coding: utf-8 -*-
"""Rig Spine 4.2 cho tướng từ ảnh GPT (thử nghiệm với repo spine-animation-ai).

    py -3 -I ArtGen/Spine/rig.py cut   giot_suong   # cắt mảnh từ L2a/L2b -> inbox/<mã>/parts/
    py -3 -I ArtGen/Spine/rig.py place giot_suong   # khớp từng mảnh vào ảnh trọn con L1_duyet.png
    py -3 -I ArtGen/Spine/rig.py build giot_suong   # xương, slot, atlas, animation, trang xem
    py -3 -I ArtGen/Spine/rig.py all   giot_suong

Cần Python có opencv-python, Pillow, numpy (venv của repo: <ProjectAtomik>/spine-animation-ai/.venv).
Repo spine-animation-ai nằm cạnh thư mục PokiWar (hoặc đặt biến môi trường SPINE_AI).
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SPINE_AI = os.environ.get("SPINE_AI") or os.path.normpath(os.path.join(HERE, "..", "..", "..", "spine-animation-ai"))
sys.path.insert(0, os.path.join(SPINE_AI, "scripts"))
try:
    from build_spine_json import _convert_timeline  # noqa: E402  (đổi keyframe sang dạng 4.2)
    from make_atlas import pack  # noqa: E402
except ImportError:  # máy không có repo spine-animation-ai: bản tự viết, cùng cách dùng (spine_compat.py)
    sys.path.insert(0, HERE)
    from spine_compat import _convert_timeline, pack  # noqa: E402

PLAYER_VER = "4.2.119"

# ---------------------------------------------------------------- spec tướng
# l/r = bên trái/phải theo người xem. Con nhìn sang phải: bên phải là phía gần người xem.
SPEC = {
    "giot_suong": {
        "sheets": {
            "L2a_head_pieces.png": [["head", "head_blink"], ["plume", "wing_l", "wing_r"]],
            "L2b_body_pieces.png": [["torso", "tail", "sword"], ["arm_l", "fist_l", "arm_r", "fist_r"],
                                    ["thigh_l", "boot_l", "thigh_r", "boot_r"]],
        },
        "side": {"wing_l": "l", "wing_r": "r", "arm_l": "l", "fist_l": "l", "arm_r": "r", "fist_r": "r",
                 "thigh_l": "l", "boot_l": "l", "thigh_r": "r", "boot_r": "r", "tail": "l", "sword": "r"},
        # vẽ từ sau ra trước
        "draw": ["tail", "arm_l", "fist_l", "thigh_l", "boot_l", "thigh_r", "boot_r", "torso", "plume", "wing_l",
                 "wing_r", "head", "arm_r", "sword", "fist_r"],
        "swap": {"head": ["head_blink"]},  # attachment phụ trong cùng slot
        # xương: (tên, cha, mảnh gắn vào, khớp)  khớp = "parent" (giao với mảnh của xương cha) hoặc tên mảnh để giao
        "bones": [
            ("hip", "root", None, "hip"),
            ("body", "hip", "torso", "hip"),
            ("head", "body", "head", "torso"),
            ("plume", "head", "plume", "head"),
            ("wing_l", "head", "wing_l", "head"),
            ("wing_r", "head", "wing_r", "head"),
            ("arm_l", "body", "arm_l", "torso"),
            ("fist_l", "arm_l", "fist_l", "arm_l"),
            ("arm_r", "body", "arm_r", "torso"),
            ("fist_r", "arm_r", "fist_r", "arm_r"),
            ("sword", "fist_r", "sword", "fist_r"),
            ("tail", "body", "tail", "torso"),
            ("thigh_l", "hip", "thigh_l", "torso"),
            ("boot_l", "thigh_l", "boot_l", "thigh_l"),
            ("thigh_r", "hip", "thigh_r", "torso"),
            ("boot_r", "thigh_r", "boot_r", "thigh_r"),
        ],
    },
}


def paths(code):
    base = SPEC[code].get("base") or os.path.join(HERE, "inbox", code)
    return {"base": base, "raw": os.path.join(base, "tai_ve"), "ref": SPEC[code].get("src") or os.path.join(base, "L1_duyet.png"),
            "parts": os.path.join(base, "parts"), "rig": os.path.join(base, "rig")}


# ---------------------------------------------------------------- nền trắng -> trong suốt
def fg_mask(rgb, light=222, sat=32):
    """Nền = vùng sáng ít màu nối với mép ảnh. Trắng bên trong hình (lòng trắng mắt, cánh) giữ nguyên."""
    mn = rgb.min(2).astype(np.int16)
    mx = rgb.max(2).astype(np.int16)
    lite = ((mn > light) & (mx - mn < sat)).astype(np.uint8)
    n, lab = cv2.connectedComponents(lite, connectivity=4)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bg = np.isin(lab, border[border > 0]) & (lite > 0)
    fg = (~bg).astype(np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    return fg


def to_rgba(rgb, mask):
    a = cv2.GaussianBlur(mask.astype(np.float32), (3, 3), 0.7)
    a = np.clip(a * 255, 0, 255).astype(np.uint8)
    return np.dstack([rgb, a])


# ---------------------------------------------------------------- cut
def cut(code):
    sp, P = SPEC[code], paths(code)
    os.makedirs(P["parts"], exist_ok=True)
    report = []
    tiles = []
    for sheet, rows in sp["sheets"].items():
        f = os.path.join(P["base"], sheet) if os.path.exists(os.path.join(P["base"], sheet)) else os.path.join(P["raw"], sheet)
        rgb = np.array(Image.open(f).convert("RGB"))
        H, W = rgb.shape[:2]
        fg = fg_mask(rgb)
        n, lab, stats, cent = cv2.connectedComponentsWithStats(fg, connectivity=8)
        need = sum(len(r) for r in rows)
        comps = sorted(range(1, n), key=lambda i: -stats[i, cv2.CC_STAT_AREA])
        comps = [i for i in comps if stats[i, cv2.CC_STAT_AREA] > 0.0002 * W * H]
        if len(comps) < need:
            boxes = [tuple(int(v) for v in stats[i, :4]) for i in comps]
            sys.exit(f"{sheet}: thấy {len(comps)} mảnh, cần {need}. Khung (x, y, w, h): {boxes}")
        group = {i: [i] for i in comps}
        area = {i: int(stats[i, cv2.CC_STAT_AREA]) for i in comps}
        # thừa mảnh: gộp mẩu nhỏ nhất vào nhóm sát nó nhất (mẩu rời của cùng một mảnh), tới khi đủ số
        while len(group) > need:
            j = min(group, key=lambda g: area[g])
            mj = np.isin(lab, group[j])
            dj = cv2.distanceTransform((~mj).astype(np.uint8), cv2.DIST_L2, 3)
            d = {g: float(dj[np.isin(lab, group[g])].min()) for g in group if g != j}
            g = min(d, key=d.get)
            if d[g] > 45:
                boxes = [tuple(int(v) for v in stats[i, :4]) for i in group]
                sys.exit(f"{sheet}: thừa mảnh ({len(group)}, cần {need}); mẩu nhỏ nhất cách mảnh khác {d[g]:.0f} px. "
                         f"Khung (x, y, w, h): {boxes}")
            group[g] += group.pop(j)
            area[g] += area[j]
            report.append(f"  gộp mẩu {area[j]} px vào mảnh bên cạnh (cách {d[g]:.0f} px)")
        big = list(group)
        for i in big:  # tâm của cả nhóm
            ys, xs = np.where(np.isin(lab, group[i]))
            cent[i] = (xs.mean(), ys.mean())
        report.append(f"{sheet}: đủ {need} mảnh")
        cy = {i: cent[i][1] for i in big}
        big.sort(key=lambda i: cy[i])
        k = 0
        names = {}
        for row in rows:
            grp = sorted(big[k:k + len(row)], key=lambda i: cent[i][0])
            k += len(row)
            for name, i in zip(row, grp):
                names[name] = i
        for name, i in names.items():
            gm = np.isin(lab, group[i])
            ys, xs = np.where(gm)
            x, y, w, h = xs.min(), ys.min(), xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
            pad = 6
            x0, y0, x1, y1 = max(0, x - pad), max(0, y - pad), min(W, x + w + pad), min(H, y + h + pad)
            m = gm[y0:y1, x0:x1].astype(np.uint8)
            # lỗ trong mảnh (trắng nội) giữ: lấp lỗ không nối mép
            inv = (1 - m).astype(np.uint8)
            nn, ll = cv2.connectedComponents(inv, connectivity=4)
            edge = np.unique(np.concatenate([ll[0], ll[-1], ll[:, 0], ll[:, -1]]))
            m = (m | (~np.isin(ll, edge) & (inv > 0))).astype(np.uint8)
            rgba = to_rgba(rgb[y0:y1, x0:x1], m)
            Image.fromarray(rgba).save(os.path.join(P["parts"], name + ".png"))
            tiles.append((name, rgba))
            report.append(f"  {name:11s} {w}x{h} tại ({x},{y})")
    # tờ kiểm
    cell = 220
    cols = 6
    rows_n = math.ceil(len(tiles) / cols)
    sheet = Image.new("RGB", (cols * cell, rows_n * (cell + 22)), (235, 238, 245))
    d = ImageDraw.Draw(sheet)
    for j, (name, rgba) in enumerate(tiles):
        im = Image.fromarray(rgba)
        im.thumbnail((cell - 10, cell - 10))
        cx, cy = (j % cols) * cell, (j // cols) * (cell + 22)
        sheet.paste(im, (cx + (cell - im.width) // 2, cy + 22 + (cell - im.height) // 2), im)
        d.text((cx + 6, cy + 4), name, fill=(20, 20, 20))
    os.makedirs(P["rig"], exist_ok=True)
    sheet.save(os.path.join(P["rig"], "kiem_manh.png"))
    print("\n".join(report))


# ---------------------------------------------------------------- place
def lab_f(rgb):
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)


def warp(rgba, s, r):
    """xoay r độ (ngược kim, như mắt nhìn) và phóng s quanh tâm; trả về ảnh vừa khít."""
    h, w = rgba.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), r, s)
    c, si = abs(M[0, 0]), abs(M[0, 1])
    nw, nh = int(h * si + w * c) + 2, int(h * c + w * si) + 2
    M[0, 2] += nw / 2 - w / 2
    M[1, 2] += nh / 2 - h / 2
    out = cv2.warpAffine(rgba, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    return out


def match(ref_lab, part, scales, rots, f, allow=None, around=None, win=None):
    """dò (s, r, x, y) cực tiểu SQDIFF có mặt nạ / diện tích mặt nạ, ở độ phân giải f."""
    best = None
    R = cv2.resize(ref_lab, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
    for s in scales:
        for r in rots:
            wp = warp(part, s * f, r)
            if wp.shape[0] >= R.shape[0] or wp.shape[1] >= R.shape[1] or min(wp.shape[:2]) < 6:
                continue
            m = (wp[:, :, 3] > 200).astype(np.float32)
            area = m.sum()
            if area < 20:
                continue
            t = lab_f(np.ascontiguousarray(wp[:, :, :3]))
            res = cv2.matchTemplate(R, t, cv2.TM_SQDIFF, mask=np.dstack([m, m, m]))
            res = res / area
            th, tw = wp.shape[:2]
            if allow is not None or around is not None:
                ys, xs = np.mgrid[0:res.shape[0], 0:res.shape[1]]
                cx, cy = (xs + tw / 2) / f, (ys + th / 2) / f
                bad = np.zeros(res.shape, bool)
                if allow is not None:
                    bad |= ~allow(cx, cy)
                if around is not None:
                    bad |= (np.abs(cx - around[0]) > win) | (np.abs(cy - around[1]) > win)
                res = np.where(bad, np.inf, res)
            mn, _, loc, _ = cv2.minMaxLoc(res)
            if not np.isfinite(mn):
                continue
            if best is None or mn < best[0]:
                best = (mn, s, r, (loc[0] + tw / 2) / f, (loc[1] + th / 2) / f)
    return best


def place(code):
    sp, P = SPEC[code], paths(code)
    ref = np.array(Image.open(P["ref"]).convert("RGB"))
    H, W = ref.shape[:2]
    rfg = fg_mask(ref)
    ys, xs = np.where(rfg > 0)
    bcx = xs.mean()
    ref_lab = lab_f(ref)
    out = {}
    pdir = os.path.join(P["rig"], "placed")
    os.makedirs(pdir, exist_ok=True)
    extras_all = {e for v in sp.get("swap", {}).values() for e in v}

    def refine(part, c, allow):
        c = match(ref_lab, part, np.arange(c[1] * 0.96, c[1] * 1.041, c[1] * 0.01), np.arange(c[2] - 6, c[2] + 6.1, 2),
                  0.5, allow, (c[3], c[4]), 40)
        return match(ref_lab, part, np.arange(c[1] * 0.99, c[1] * 1.011, c[1] * 0.004), np.arange(c[2] - 2, c[2] + 2.1, 1),
                     1.0, allow, (c[3], c[4]), 12)

    for sheet, rows in sp["sheets"].items():
        names = [n for row in rows for n in row if n not in extras_all]
        img = {n: np.array(Image.open(os.path.join(P["parts"], n + ".png")).convert("RGBA")) for n in names}
        # mảnh lớn nhất dò tỉ lệ cả tờ (GPT vẽ tờ mảnh to nhỏ tuỳ ý), các mảnh khác dò quanh tỉ lệ đó
        anchor = max(names, key=lambda n: int((img[n][:, :, 3] > 128).sum()))
        order = [anchor] + [n for n in names if n != anchor]
        S = None
        for name in order:
            part = img[name]
            side = sp["side"].get(name)
            allow = None
            if side == "l":
                allow = lambda cx, cy: cx < bcx + 0.06 * W  # noqa: E731
            elif side == "r":
                allow = lambda cx, cy: cx > bcx - 0.06 * W  # noqa: E731
            if S is None:
                c = match(ref_lab, part, 0.35 * 1.06 ** np.arange(36), range(-24, 25, 8), 0.2, allow)
            else:
                c = match(ref_lab, part, S * np.arange(0.75, 1.31, 0.04), range(-30, 31, 6), 0.25, allow)
            err, s, r, cx, cy = refine(part, c, allow)
            if S is None:
                S = s
                print(f"  tờ {sheet}: tỉ lệ ~{S:.3f} (theo {anchor})")
            out[name] = {"s": round(float(s), 4), "r": round(float(r), 2), "cx": round(float(cx), 1),
                         "cy": round(float(cy), 1), "err": round(float(err), 1)}
            print(f"  {name:11s} s={s:.3f} r={r:+.0f} tâm=({cx:.0f},{cy:.0f}) sai={err:.0f}", flush=True)
    # mảnh phụ cùng slot: khớp vào mảnh chính đã đặt
    for main, extras in sp.get("swap", {}).items():
        mp = np.array(Image.open(os.path.join(P["parts"], main + ".png")).convert("RGBA"))
        for ex in extras:
            e = np.array(Image.open(os.path.join(P["parts"], ex + ".png")).convert("RGBA"))
            # nền: mảnh chính trên trắng, cỡ gốc
            pad = 80
            canvas = np.full((mp.shape[0] + 2 * pad, mp.shape[1] + 2 * pad, 3), 255, np.uint8)
            a = mp[:, :, 3:4] / 255.0
            canvas[pad:-pad, pad:-pad] = (mp[:, :, :3] * a + 255 * (1 - a)).astype(np.uint8)
            c = match(lab_f(canvas), e, np.arange(0.85, 1.16, 0.01), np.arange(-4, 4.1, 1), 1.0)
            _, s2, r2, ex_cx, ex_cy = c
            m = out[main]
            # đổi về toạ độ ảnh trọn con theo phép biến đổi của mảnh chính
            dx, dy = ex_cx - (pad + mp.shape[1] / 2), ex_cy - (pad + mp.shape[0] / 2)
            th = math.radians(-m["r"])
            rx = m["s"] * (dx * math.cos(th) - dy * math.sin(th))
            ry = m["s"] * (dx * math.sin(th) + dy * math.cos(th))
            out[ex] = {"s": round(m["s"] * s2, 4), "r": round(m["r"] + r2, 2), "cx": round(m["cx"] + rx, 1),
                       "cy": round(m["cy"] + ry, 1), "err": round(float(c[0]), 1), "of": main}
            print(f"  {ex:11s} theo {main}: s={s2:.3f} r={r2:+.0f} lệch=({dx:.0f},{dy:.0f})")
    # ảnh đã biến đổi + ghép thử
    comp = np.full((H, W, 3), 255, np.float32)
    for name, t in out.items():
        part = np.array(Image.open(os.path.join(P["parts"], name + ".png")).convert("RGBA"))
        wp = warp(part, t["s"], t["r"])
        Image.fromarray(wp).save(os.path.join(pdir, name + ".png"))
        t["w"], t["h"] = int(wp.shape[1]), int(wp.shape[0])
        t["x0"], t["y0"] = int(round(t["cx"] - wp.shape[1] / 2)), int(round(t["cy"] - wp.shape[0] / 2))
    for name in sp["draw"]:
        t = out[name]
        wp = np.array(Image.open(os.path.join(pdir, name + ".png")))
        paste(comp, wp, t["x0"], t["y0"])
    comp = comp.astype(np.uint8)
    cfg = fg_mask(comp)
    iou = float((cfg & rfg).sum() / max(1, (cfg | rfg).sum()))
    diff = np.zeros_like(ref)
    diff[(rfg > 0) & (cfg == 0)] = (230, 60, 60)    # ảnh gốc có, ghép thiếu
    diff[(rfg == 0) & (cfg > 0)] = (60, 110, 230)   # ghép thừa
    diff[(rfg > 0) & (cfg > 0)] = (205, 205, 205)
    side = np.concatenate([ref, comp, diff], 1)
    Image.fromarray(side).save(os.path.join(P["rig"], "so_ghep.png"))
    json.dump({"ref_size": [W, H], "iou": round(iou, 4), "parts": out}, open(os.path.join(P["rig"], "placed.json"), "w"),
              indent=1)
    print(f"IoU bóng ghép/ảnh gốc = {iou:.3f}  ->  {os.path.join(P['rig'], 'so_ghep.png')}")


def paste(comp, wp, x0, y0):
    H, W = comp.shape[:2]
    h, w = wp.shape[:2]
    ax0, ay0, ax1, ay1 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if ax1 <= ax0 or ay1 <= ay0:
        return
    sub = wp[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0].astype(np.float32)
    a = sub[:, :, 3:4] / 255.0
    comp[ay0:ay1, ax0:ax1] = comp[ay0:ay1, ax0:ax1] * (1 - a) + sub[:, :, :3] * a


# ---------------------------------------------------------------- build
def placed_mask(t, wp, W, H):
    m = np.zeros((H, W), np.uint8)
    h, w = wp.shape[:2]
    x0, y0 = t["x0"], t["y0"]
    ax0, ay0, ax1, ay1 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    m[ay0:ay1, ax0:ax1] = (wp[ay0 - y0:ay1 - y0, ax0 - x0:ax1 - x0, 3] > 128)
    return m


def joint(mc, mp):
    """khớp = tâm vùng giao (mảnh con lấn dưới mảnh cha); không giao thì điểm giữa hai chỗ gần nhau nhất."""
    inter = mc & cv2.dilate(mp, np.ones((9, 9), np.uint8))
    if inter.sum() > 30:
        ys, xs = np.where(inter > 0)
        return float(xs.mean()), float(ys.mean())
    dt, lab = cv2.distanceTransformWithLabels(1 - mp, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.where(mc > 0)
    i = np.argmin(dt[ys, xs])
    return float(xs[i]), float(ys[i])


def build(code):
    sp, P = SPEC[code], paths(code)
    pl = json.load(open(os.path.join(P["rig"], "placed.json")))
    W, H = pl["ref_size"]
    parts = pl["parts"]
    pdir = os.path.join(P["rig"], "placed")
    img = {n: np.array(Image.open(os.path.join(pdir, n + ".png"))) for n in parts}
    mask = {n: placed_mask(parts[n], img[n], W, H) for n in parts}
    if "root" in sp:  # khớp ghi tay (chế độ một ảnh)
        feet_x, ground = sp["root"]
        world = {"root": (feet_x, ground)}
        for b, parent, part, how in sp["bones"]:
            world[b] = tuple(how)
    else:
        # gốc: giữa hai ủng, mặt đất = đáy hình
        ground = max(parts[n]["y0"] + parts[n]["h"] for n in ("boot_l", "boot_r"))
        feet_x = (parts["boot_l"]["cx"] + parts["boot_r"]["cx"]) / 2
        world = {"root": (feet_x, ground)}
        jl = joint(mask["thigh_l"], mask["torso"])
        jr = joint(mask["thigh_r"], mask["torso"])
        for b, parent, part, how in sp["bones"]:
            if how == "hip":
                world[b] = ((jl[0] + jr[0]) / 2, (jl[1] + jr[1]) / 2)
            else:
                world[b] = joint(mask[part], mask[how])

    def sp_xy(p):  # ảnh -> Spine (y lên, gốc ở chân)
        return p[0] - feet_x, ground - p[1]

    bones = [{"name": "root"}]
    for b, parent, part, how in sp["bones"]:
        bx, by = sp_xy(world[b])
        px, py = sp_xy(world[parent])
        bones.append({"name": b, "parent": parent, "x": round(bx - px, 2), "y": round(by - py, 2), "length": 18})
    bone_of = {part: b for b, _, part, _ in sp["bones"] if part}
    for main, extras in sp.get("swap", {}).items():
        for ex in extras:
            bone_of[ex] = bone_of[main]
    slots, skin = [], {}
    for name in sp["draw"]:
        slots.append({"name": name, "bone": bone_of[name], "attachment": name})
        atts = {}
        for att in [name] + sp.get("swap", {}).get(name, []):
            t = parts[att]
            cx, cy = sp_xy((t["x0"] + t["w"] / 2, t["y0"] + t["h"] / 2))
            bx, by = sp_xy(world[bone_of[att]])
            atts[att] = {"x": round(cx - bx, 2), "y": round(cy - by, 2), "width": t["w"], "height": t["h"]}
        skin[name] = atts
    anims = ANIMS[code]()
    raw = json.loads(json.dumps(anims))  # bản trước khi đổi sang 4.2, cho bộ dựng khung
    for a in anims.values():
        for tl in a.get("bones", {}).values():
            for kind, frames in tl.items():
                _convert_timeline(kind, frames)
    xs = [parts[n]["x0"] for n in parts] + [parts[n]["x0"] + parts[n]["w"] for n in parts]
    ys = [parts[n]["y0"] for n in parts]
    skel = {"skeleton": {"hash": code, "spine": "4.2.0", "x": round(min(xs) - feet_x), "y": 0,
                         "width": round(max(xs) - min(xs)), "height": round(ground - min(ys)), "images": "./images/"},
            "bones": bones, "slots": slots, "skins": [{"name": "default", "attachments": skin}], "animations": anims}
    out = P["rig"]
    json.dump(skel, open(os.path.join(out, code + ".json"), "w"), indent=1)
    # atlas
    ims = {n: Image.fromarray(img[n]) for n in parts}
    aw, ah, place_ = pack(ims, padding=2)
    atlas = Image.new("RGBA", (aw, ah), (0, 0, 0, 0))
    lines = [f"{code}.png", f"size: {aw},{ah}", "format: RGBA8888", "filter: Linear,Linear", "repeat: none"]
    for n, (x, y, w, h) in place_.items():
        atlas.paste(ims[n], (x, y))
        lines += [n, "  rotate: false", f"  xy: {x}, {y}", f"  size: {w}, {h}", f"  orig: {w}, {h}", "  offset: 0, 0",
                  "  index: -1"]
    atlas.save(os.path.join(out, code + ".png"))
    open(os.path.join(out, code + ".atlas"), "w").write("\n".join(lines) + "\n")
    # ảnh xương để soi khớp
    dbg = Image.open(P["ref"]).convert("RGB")
    d = ImageDraw.Draw(dbg)
    for b, parent, part, how in sp["bones"]:
        x, y = world[b]
        px, py = world[parent]
        d.line([px, py, x, y], fill=(255, 0, 160), width=3)
        d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=(255, 0, 160), width=3)
        d.text((x + 9, y - 6), b, fill=(120, 0, 80))
    dbg.save(os.path.join(out, "xuong.png"))
    page(code, list(anims))
    render(code, skel, raw, {n: img[n] for n in parts})
    print(f"{len(bones)} xương, {len(slots)} slot, atlas {aw}x{ah}, animation: {', '.join(anims)}")


# ---------------------------------------------------------------- dựng khung (soi animation không cần trình duyệt)
def bez(c, u):
    """curve chuẩn hoá [cx1, cy1, cx2, cy2]: tìm s để x(s)=u rồi trả y(s)."""
    if not c:
        return u
    x1, y1, x2, y2 = c
    lo, hi = 0.0, 1.0
    for _ in range(30):
        s = (lo + hi) / 2
        x = 3 * (1 - s) ** 2 * s * x1 + 3 * (1 - s) * s * s * x2 + s ** 3
        lo, hi = (s, hi) if x < u else (lo, s)
    s = (lo + hi) / 2
    return 3 * (1 - s) ** 2 * s * y1 + 3 * (1 - s) * s * s * y2 + s ** 3


def sample(frames, t, keys):
    if t <= frames[0]["time"]:
        return [frames[0].get(k, 0) for k in keys]
    for a, b in zip(frames, frames[1:]):
        if t <= b["time"]:
            u = (t - a["time"]) / max(1e-6, b["time"] - a["time"])
            w = bez(b.get("curve"), u)
            return [a.get(k, 0) + (b.get(k, 0) - a.get(k, 0)) * w for k in keys]
    return [frames[-1].get(k, 0) for k in keys]


def pose(skel, anim, t):
    """ma trận thế giới (3x3, y lên) của từng xương + attachment đang hiện của từng slot."""
    world = {}
    tls = anim.get("bones", {})
    for b in skel["bones"]:
        x, y, r, sx, sy = b.get("x", 0), b.get("y", 0), 0.0, 1.0, 1.0
        tl_ = tls.get(b["name"], {})
        if "translate" in tl_:
            dx, dy = sample(tl_["translate"], t, ("x", "y"))
            x, y = x + dx, y + dy
        if "rotate" in tl_:
            r += sample(tl_["rotate"], t, ("angle",))[0]
        if "scale" in tl_:
            fx, fy = sample(tl_["scale"], t, ("x", "y"))
            sx, sy = sx * fx, sy * fy
        c, s = math.cos(math.radians(r)), math.sin(math.radians(r))
        M = np.array([[c * sx, -s * sy, x], [s * sx, c * sy, y], [0, 0, 1]])
        if "parent" not in b:
            world[b["name"]] = M
        else:
            P = world[b["parent"]]
            if b.get("inherit") == "noScale":  # nhận vị trí và góc của cha, bỏ tỉ lệ
                P = P.copy()
                P[:2, 0] /= max(1e-9, np.linalg.norm(P[:2, 0]))
                P[:2, 1] /= max(1e-9, np.linalg.norm(P[:2, 1]))
            world[b["name"]] = P @ M
    show = {}
    for sl in skel["slots"]:
        name = sl["attachment"]
        for k in anim.get("slots", {}).get(sl["name"], {}).get("attachment", []):
            if k["time"] <= t + 1e-6:
                name = k["name"]
        show[sl["name"]] = name
    return world, show


def draw_pose(skel, anim, t, img, k, box):
    """dựng một khung lên nền giấy; box = (rộng, cao, gốc x, gốc y) theo pixel khung."""
    Wb, Hb, ox, oy = box
    canvas = np.full((Hb, Wb, 3), (250, 246, 236), np.float32)
    world, show = pose(skel, anim, t)
    atts = skel["skins"][0]["attachments"]
    to_px = np.array([[k, 0, ox], [0, -k, oy], [0, 0, 1]])
    for sl in skel["slots"]:
        an = show[sl["name"]]
        a = atts[sl["name"]][an]
        im = img[an]
        h, w = im.shape[:2]
        # pixel ảnh (u, v xuống) -> không gian xương
        A = np.array([[1, 0, a["x"] - w / 2], [0, -1, a["y"] + h / 2], [0, 0, 1]])
        M = (to_px @ world[sl["bone"]] @ A)[:2]
        wp = cv2.warpAffine(im, M, (Wb, Hb), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                            borderValue=(0, 0, 0, 0)).astype(np.float32)
        al = wp[:, :, 3:4] / 255.0
        canvas = canvas * (1 - al) + wp[:, :, :3] * al
    return canvas.astype(np.uint8)


def render(code, skel, raw, img, out=None, draw=None, fh=300, gif_scale=1.2):
    out = out or paths(code)["rig"]
    draw = draw or draw_pose
    sk = skel["skeleton"]  # fh: cao mỗi khung
    up = max([f.get("y", 0) for a in raw.values() for f in a.get("bones", {}).get("root", {}).get("translate", [])] + [0])
    k = fh / (sk["height"] * 1.3 + up)
    Wb = int(sk["width"] * 1.7 * k)
    box = (Wb, fh, int(-sk["x"] * k + 0.35 * sk["width"] * k), int(fh - 0.12 * fh))
    rows = []
    for name, anim in raw.items():
        dur = max(f["time"] for tl_ in anim.get("bones", {}).values() for fr in tl_.values() for f in fr)
        n = 9
        frames = [draw(skel, anim, dur * i / (n - 1), img, k, box) for i in range(n)]
        row = np.concatenate(frames, 1)
        lab = Image.fromarray(row)
        d = ImageDraw.Draw(lab)
        d.text((6, 4), f"{name} ({dur:.2f}s)", fill=(43, 33, 24))
        for i in range(n):
            d.text((i * Wb + Wb - 44, fh - 16), f"{dur * i / (n - 1):.2f}", fill=(120, 100, 80))
        rows.append(np.array(lab))
        # GIF 20 hình/giây
        gs = gif_scale
        gk = k * gs
        gbox = (int(Wb * gs), int(fh * gs), int(box[2] * gs), int(box[3] * gs))
        g = [Image.fromarray(draw(skel, anim, t, img, gk, gbox)) for t in np.arange(0, dur + 1e-6, 0.05)]
        g[0].save(os.path.join(out, f"anim_{name}.gif"), save_all=True, append_images=g[1:], duration=50, loop=0)
    Image.fromarray(np.concatenate(rows, 0)).save(os.path.join(out, "khung.png"))


def page(code, anims, out=None):
    cards = "\n".join(
        f'<div class="card"><div id="p_{a}" class="pl"></div><div class="lb">{a}</div></div>' for a in anims)
    js = ",".join(f'"{a}"' for a in anims)
    html = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Spine {code}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://unpkg.com/@esotericsoftware/spine-player@{PLAYER_VER}/dist/spine-player.css">
<script src="https://unpkg.com/@esotericsoftware/spine-player@{PLAYER_VER}/dist/iife/spine-player.js"></script>
<style>body{{margin:0;background:#f4efe4;font:14px system-ui;color:#2b2118}}h1{{font-size:18px;margin:12px 16px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;padding:0 16px 16px}}
.card{{background:#fffaf0;border:1px solid #d8cbb0;border-radius:10px;overflow:hidden}}.pl{{height:320px}}
.lb{{padding:6px 10px;font-weight:600}}#big{{height:520px;margin:0 16px 16px;border:1px solid #d8cbb0;border-radius:10px;overflow:hidden}}</style>
</head><body><h1>{code}: Spine 4.2 (thử nghiệm)</h1><div class="grid">{cards}</div><div id="big"></div>
<script>
const A=[{js}];window.players={{}};
for(const a of A){{window.players[a]=new spine.SpinePlayer("p_"+a,{{skeleton:"{code}.json",atlas:"{code}.atlas",animation:a,
 showControls:false,backgroundColor:"#fffaf000",alpha:true,premultipliedAlpha:false,viewport:{{padLeft:"8%",padRight:"8%",padTop:"6%",padBottom:"4%"}}}});}}
window.big=new spine.SpinePlayer("big",{{skeleton:"{code}.json",atlas:"{code}.atlas",animation:A[0],showControls:true,
 backgroundColor:"#fffaf0ff",premultipliedAlpha:false}});
</script></body></html>"""
    open(os.path.join(out or paths(code)["rig"], "index.html"), "w", encoding="utf-8").write(html)


# ---------------------------------------------------------------- animation
E = [0.25, 0, 0.75, 1]      # êm hai đầu
EO = [0.1, 0.6, 0.3, 1]     # bật nhanh rồi chậm
EI = [0.6, 0, 0.9, 0.4]     # chậm rồi nhanh
L = None                    # thẳng


def tl(keys, kind="rotate"):
    """keys: (t, giá trị, curve) ; translate/scale: (t, x, y, curve). curve gắn với đoạn KẾT THÚC ở khoá đó."""
    fr = []
    for k in keys:
        if kind == "rotate":
            f = {"time": k[0], "angle": k[1]}
            c = k[2] if len(k) > 2 else E
        else:
            f = {"time": k[0], "x": k[1], "y": k[2]}
            c = k[3] if len(k) > 3 else E
        if c:
            f["curve"] = c
        fr.append(f)
    return fr


def tl2(keys):
    return tl(keys, "xy")


def osc(bone_amp, T, phase=0.0, n=4):
    """dao động vòng lặp: khoá ở 0, T/2, T theo pha (giá trị đầu = cuối)."""
    a = bone_amp
    ks = []
    for i in range(n + 1):
        t = T * i / n
        ks.append((round(t, 4), round(a * math.sin(2 * math.pi * (i / n) - phase), 2)))
    return ks


def gs_anims():
    A = {}
    T = 1.6
    sway = lambda amp, ph: tl([(t, v) for t, v in osc(amp, T, ph, 8)])  # noqa: E731
    A["idle"] = {
        "bones": {
            "body": {"translate": tl2([(0, 0, 0), (0.8, 0, -6), (T, 0, 0)]),
                     "scale": tl2([(0, 1, 1), (0.8, 1.025, 0.975), (T, 1, 1)])},
            "head": {"rotate": sway(1.6, 0.6), "translate": tl2([(0, 0, 0), (0.9, 0, -2), (T, 0, 0)])},
            "plume": {"rotate": sway(5, 1.4)},
            "wing_l": {"rotate": sway(7, 1.0)},
            "wing_r": {"rotate": sway(-7, 1.0)},
            "tail": {"rotate": sway(5, 1.8)},
            "arm_l": {"rotate": sway(3, 0.8)},
            "arm_r": {"rotate": sway(-2.5, 0.8)},
            "sword": {"rotate": sway(2, 1.3)},
        },
        "slots": {"head": {"attachment": [{"time": 1.15, "name": "head_blink"}, {"time": 1.27, "name": "head"}]}},
    }
    # chém: lấy đà (tay kiếm vòng lên sau đầu) -> chém xuống trước -> dư lực -> về
    A["attack"] = {"bones": {
        "body": {"rotate": tl([(0, 0), (0.22, 9, EO), (0.3, 9), (0.38, -14, EI), (0.5, -10, EO), (0.8, 0)]),
                 "translate": tl2([(0, 0, 0), (0.22, -10, -4, EO), (0.3, -10, -4), (0.38, 22, -2, EI), (0.5, 18, -3),
                                  (0.8, 0, 0)]),
                 "scale": tl2([(0, 1, 1), (0.22, 0.97, 1.04), (0.3, 0.97, 1.04), (0.38, 1.07, 0.94, EI), (0.5, 1.02, 0.98),
                              (0.8, 1, 1)])},
        "head": {"rotate": tl([(0, 0), (0.22, -5, EO), (0.3, -5), (0.4, 7, EI), (0.55, 3), (0.8, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.22, -135, EO), (0.3, -140), (0.38, 45, EI), (0.5, 35, EO), (0.8, 0)])},
        "fist_r": {"rotate": tl([(0, 0), (0.22, -15, EO), (0.3, -15), (0.38, 20, EI), (0.5, 10), (0.8, 0)])},
        "sword": {"rotate": tl([(0, 0), (0.22, -20, EO), (0.3, -25), (0.38, 15, EI), (0.5, 8), (0.8, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (0.22, 25, EO), (0.3, 25), (0.38, -35, EI), (0.5, -25), (0.8, 0)])},
        "plume": {"rotate": tl([(0, 0), (0.25, 10), (0.36, 12), (0.46, -18, EO), (0.62, 6), (0.8, 0)])},
        "wing_l": {"rotate": tl([(0, 0), (0.25, 10), (0.42, -14, EO), (0.6, 4), (0.8, 0)])},
        "wing_r": {"rotate": tl([(0, 0), (0.25, -10), (0.42, 14, EO), (0.6, -4), (0.8, 0)])},
        "tail": {"rotate": tl([(0, 0), (0.25, -8), (0.42, 14, EO), (0.62, -4), (0.8, 0)])},
        "thigh_l": {"rotate": tl([(0, 0), (0.22, 4), (0.38, -6, EI), (0.8, 0)])},
        "thigh_r": {"rotate": tl([(0, 0), (0.22, -3), (0.38, 8, EI), (0.8, 0)])},
    }}
    # trúng đòn: bật lùi, nhắm mắt, tay hất
    A["hit"] = {"bones": {
        "body": {"rotate": tl([(0, 0), (0.08, 12, EO), (0.45, 0)]),
                 "translate": tl2([(0, 0, 0), (0.08, -16, 2, EO), (0.45, 0, 0)])},
        "head": {"rotate": tl([(0, 0), (0.1, 9, EO), (0.45, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (0.1, 30, EO), (0.45, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.1, 25, EO), (0.45, 0)])},
        "plume": {"rotate": tl([(0, 0), (0.12, -12, EO), (0.3, 6), (0.45, 0)])},
        "tail": {"rotate": tl([(0, 0), (0.12, 10, EO), (0.45, 0)])},
        "wing_l": {"rotate": tl([(0, 0), (0.12, -12, EO), (0.45, 0)])},
        "wing_r": {"rotate": tl([(0, 0), (0.12, 12, EO), (0.45, 0)])},
    }, "slots": {"head": {"attachment": [{"time": 0.02, "name": "head_blink"}, {"time": 0.3, "name": "head"}]}}}
    # chiêu: ngồi lấy đà -> nhảy giơ kiếm -> bổ xuống -> chạm đất nảy
    A["skill"] = {"bones": {
        "root": {"translate": tl2([(0, 0, 0), (0.3, 0, 0), (0.55, 10, 70, EO), (0.72, 18, 78), (0.86, 30, 0, EI),
                                  (1.4, 0, 0)])},
        "body": {"translate": tl2([(0, 0, 0), (0.3, 0, -16, EO), (0.45, 0, 4), (0.86, 0, 0), (0.92, 0, -14, EO),
                                  (1.1, 0, 0)]),
                 "scale": tl2([(0, 1, 1), (0.3, 1.07, 0.9, EO), (0.45, 0.95, 1.08), (0.72, 1, 1), (0.88, 1.08, 0.9, EI),
                              (1.05, 0.98, 1.02), (1.4, 1, 1)]),
                 "rotate": tl([(0, 0), (0.3, 6), (0.72, 10), (0.86, -18, EI), (1.0, -12), (1.4, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.3, 20), (0.55, -175, EO), (0.74, -185), (0.86, 55, EI), (1.0, 45),
                                (1.4, 0)])},
        "sword": {"rotate": tl([(0, 0), (0.55, -30, EO), (0.74, -35), (0.86, 20, EI), (1.0, 10), (1.4, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (0.3, 30), (0.55, -40, EO), (0.86, 40, EI), (1.4, 0)])},
        "head": {"rotate": tl([(0, 0), (0.3, -6), (0.55, 6), (0.86, 8, EI), (1.4, 0)])},
        "thigh_l": {"rotate": tl([(0, 0), (0.3, 6), (0.55, 18, EO), (0.8, 10), (0.88, 0, EI), (1.4, 0)])},
        "thigh_r": {"rotate": tl([(0, 0), (0.3, -6), (0.55, -14, EO), (0.8, -8), (0.88, 0, EI), (1.4, 0)])},
        "boot_l": {"rotate": tl([(0, 0), (0.55, -12, EO), (0.86, 0, EI), (1.4, 0)])},
        "boot_r": {"rotate": tl([(0, 0), (0.55, 10, EO), (0.86, 0, EI), (1.4, 0)])},
        "plume": {"rotate": tl([(0, 0), (0.32, 8), (0.55, -14), (0.75, 10), (0.92, -20, EO), (1.15, 6), (1.4, 0)])},
        "wing_l": {"rotate": tl([(0, 0), (0.45, 18), (0.6, -10), (0.75, 18), (0.92, -12), (1.4, 0)])},
        "wing_r": {"rotate": tl([(0, 0), (0.45, -18), (0.6, 10), (0.75, -18), (0.92, 12), (1.4, 0)])},
        "tail": {"rotate": tl([(0, 0), (0.32, -6), (0.6, 16), (0.92, -14, EO), (1.15, 5), (1.4, 0)])},
    }}
    # chạy tại chỗ (thử)
    R = 0.5
    A["run"] = {"bones": {
        "body": {"translate": tl2([(0, 0, 0), (0.125, 0, 9, EO), (0.25, 0, 0, EI), (0.375, 0, 9, EO), (R, 0, 0, EI)]),
                 "rotate": tl([(0, -7), (R, -7)])},
        "thigh_l": {"rotate": tl([(0, 28), (0.25, -28), (R, 28)])},
        "thigh_r": {"rotate": tl([(0, -28), (0.25, 28), (R, -28)])},
        "boot_l": {"rotate": tl([(0, -10), (0.25, 15), (R, -10)])},
        "boot_r": {"rotate": tl([(0, 15), (0.25, -10), (R, 15)])},
        "arm_l": {"rotate": tl([(0, -35), (0.25, 35), (R, -35)])},
        "arm_r": {"rotate": tl([(0, 30), (0.25, -30), (R, 30)])},
        "head": {"rotate": tl([(0, 2), (0.125, -2), (0.25, 2), (0.375, -2), (R, 2)])},
        "plume": {"rotate": tl([(0, 6), (0.18, -6), (0.31, 6), (0.43, -6), (R, 6)])},
        "tail": {"rotate": tl([(0, 8), (0.25, -8), (R, 8)])},
        "wing_l": {"rotate": tl([(0, 10), (0.25, -6), (R, 10)])},
        "wing_r": {"rotate": tl([(0, -10), (0.25, 6), (R, -10)])},
    }}
    return A


# ---------------------------------------------------------------- chế độ một ảnh liền
# Cắt mảnh ngay trên một ảnh trọn con: đa giác chọn vùng, lọc theo màu, phần chồng (cap) lấn vào mảnh cha,
# vẽ bù (inpaint) chỗ bị mảnh khác che. Khớp xương ghi tay theo toạ độ ảnh.
def poly_mask(shape, poly):
    m = np.zeros(shape[:2], np.uint8)
    cv2.fillPoly(m, [np.array(poly, np.int32)], 1)
    return m > 0


def biggest(m, min_px=40):
    n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
    keep = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= min_px]
    return np.isin(lab, keep)


def one(code):
    sp, P = SPEC[code], paths(code)
    rgb = np.array(Image.open(P["ref"]).convert("RGB"))
    H, W = rgb.shape[:2]
    fg = fg_mask(rgb, *sp.get("fg", (222, 32)))
    fg = cv2.erode(fg, np.ones((3, 3), np.uint8)).astype(np.float32)  # gọt viền lẫn nền (ảnh không nét viền)
    fg = cv2.GaussianBlur(fg, (0, 0), 1.6) > 0.5  # làm mượt mép răng cưa
    dark = rgb.mean(2) < sp.get("dark_thr", 120)
    cls = {"dark": dark, "light": ~dark}
    region, masks, taken = {}, {}, np.zeros((H, W), bool)
    for name, d in sp["one"].items():  # theo thứ tự: mảnh "excl" giành pixel trước
        m = poly_mask(rgb.shape, d["poly"]) & fg
        for o in d.get("minus", []):
            m &= ~poly_mask(rgb.shape, o)
        if d.get("excl"):
            m &= ~taken
            taken |= m
        region[name] = m.copy()
        if "keep" in d:
            m &= cls[d["keep"]]
        masks[name] = biggest(m)
    pdir = os.path.join(P["rig"], "placed")
    os.makedirs(pdir, exist_ok=True)
    out = {}
    for name, d in sp["one"].items():
        core = masks[name]
        src = rgb.copy()
        alpha = core.astype(np.float32)
        if "cap" in d:  # lấn sang mảnh cha r px, mờ dần ra mép
            into, r = d["cap"]
            dist = cv2.distanceTransform((~core).astype(np.uint8), cv2.DIST_L2, 5)
            cap = (dist <= r) & region[into] & ~core
            if "cap_keep" in d:
                cap &= cls[d["cap_keep"]]
            alpha = np.maximum(alpha, np.where(cap, np.clip(1.15 - dist / r, 0, 1), 0))
        if "inpaint" in d:  # vẽ bù pixel lớp màu này trong mảnh (chỗ bị mảnh khác che)
            hole = cv2.dilate((core & cls[d["inpaint"]]).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
            hole &= core
            fill = core & ~hole
            med = np.median(rgb[fill], 0) if fill.any() else np.array([128, 128, 128])
            work = rgb.copy()
            work[~core] = med.astype(np.uint8)
            src = cv2.inpaint(work, hole.astype(np.uint8) * 255, 9, cv2.INPAINT_TELEA)
            src = cv2.GaussianBlur(src, (0, 0), 1.2) * hole[..., None] + src * (~hole[..., None])
            src = src.astype(np.uint8)
        a = cv2.GaussianBlur(alpha, (3, 3), 0.7)
        ys, xs = np.where(a > 0.02)
        x0, y0, x1, y1 = max(0, xs.min() - 2), max(0, ys.min() - 2), min(W, xs.max() + 3), min(H, ys.max() + 3)
        rgba = np.dstack([src[y0:y1, x0:x1], np.clip(a[y0:y1, x0:x1] * 255, 0, 255).astype(np.uint8)])
        Image.fromarray(rgba).save(os.path.join(pdir, name + ".png"))
        out[name] = {"s": 1, "r": 0, "x0": int(x0), "y0": int(y0), "w": int(x1 - x0), "h": int(y1 - y0),
                     "cx": (x0 + x1) / 2, "cy": (y0 + y1) / 2}
        print(f"  {name:8s} {x1 - x0}x{y1 - y0} tại ({x0},{y0})" + (" +chồng" if "cap" in d else "") +
              (" +vẽ bù" if "inpaint" in d else ""))
    comp = np.full((H, W, 3), 255, np.float32)
    for name in sp["draw"]:
        paste(comp, np.array(Image.open(os.path.join(pdir, name + ".png"))), out[name]["x0"], out[name]["y0"])
    comp = comp.astype(np.uint8)
    # tờ kiểm: ảnh gốc | ghép lại | từng mảnh trên nền xám
    tiles = Image.new("RGB", (W, H), (200, 205, 215))
    x = y = 4
    rowh = 0
    for name in sp["draw"]:
        im = Image.open(os.path.join(pdir, name + ".png"))
        im.thumbnail((W // 3 - 8, H // 2 - 8))
        if x + im.width > W:
            x, y, rowh = 4, y + rowh + 6, 0
        tiles.paste(im, (x, y), im)
        ImageDraw.Draw(tiles).text((x + 2, y + 2), name, fill=(0, 0, 0))
        x += im.width + 6
        rowh = max(rowh, im.height)
    side = np.concatenate([rgb, comp, np.array(tiles)], 1)
    Image.fromarray(side).save(os.path.join(P["rig"], "so_ghep.png"))
    json.dump({"ref_size": [W, H], "parts": out}, open(os.path.join(P["rig"], "placed.json"), "w"), indent=1)


SPEC["snorlax"] = {  # ảnh mạng, chỉ để thử
    "base": os.path.join(SPINE_AI, "work", "snorlax"),
    "src": os.path.join(SPINE_AI, "work", "snorlax", "src.png"),
    "fg": (232, 20),
    "dark_thr": 120,
    "draw": ["ear_l", "ear_r", "foot_l", "foot_r", "body", "belly", "head", "arm_l", "arm_r"],
    "one": {
        "head": {"poly": [(180, 15), (340, 15), (338, 100), (332, 130), (188, 130), (182, 100)], "excl": True,
                 "cap": ("body", 10),
                 "minus": [[(182, 12), (218, 12), (214, 42), (186, 50)], [(290, 12), (342, 12), (334, 56), (300, 40)]]},
        "arm_l": {"poly": [(40, 95), (205, 95), (205, 122), (172, 140), (152, 175), (122, 205), (40, 215)], "excl": True,
                  "cap": ("body", 9), "cap_keep": "dark"},
        "arm_r": {"poly": [(478, 95), (312, 95), (312, 122), (345, 140), (365, 175), (395, 205), (478, 215)],
                  "excl": True, "cap": ("body", 9), "cap_keep": "dark"},
        "body": {"poly": [(190, 108), (328, 108), (345, 140), (365, 175), (395, 205), (422, 260), (422, 330), (290, 336),
                          (285, 352), (232, 352), (228, 336), (94, 330), (94, 260), (122, 205), (152, 175), (172, 140)],
                 "excl": True, "inpaint": "light"},
        "belly": {"poly": [(140, 124), (372, 124), (372, 322), (140, 322)], "keep": "light"},
        "ear_l": {"poly": [(182, 15), (218, 15), (218, 62), (182, 72)]},
        "ear_r": {"poly": [(288, 15), (342, 15), (340, 70), (296, 55)]},
        "foot_l": {"poly": [(120, 318), (232, 318), (232, 368), (120, 368)], "inpaint": "dark"},
        "foot_r": {"poly": [(285, 318), (400, 318), (400, 368), (285, 368)], "inpaint": "dark"},
    },
    "root": (258, 362),
    "bones": [
        ("body", "root", "body", (258, 336)),
        ("belly", "body", "belly", (256, 318)),
        ("head", "body", "head", (258, 128)),
        ("ear_l", "head", "ear_l", (200, 50)),
        ("ear_r", "head", "ear_r", (314, 48)),
        ("arm_l", "body", "arm_l", (182, 158)),
        ("arm_r", "body", "arm_r", (334, 158)),
        ("foot_l", "root", "foot_l", (178, 348)),
        ("foot_r", "root", "foot_r", (340, 348)),
    ],
}


def sn_anims():
    """con béo tròn: thở phình bụng, đập hai tay, nảy bụng, nhảy đè, đi lạch bạch."""
    A = {}
    T = 2.4
    A["idle"] = {"bones": {
        "body": {"scale": tl2([(0, 1, 1), (1.1, 0.985, 1.035), (T, 1, 1)])},
        "belly": {"scale": tl2([(0, 1, 1), (0.2, 1, 1), (1.3, 1.045, 1.03), (T, 1, 1)])},
        "head": {"translate": tl2([(0, 0, 0), (1.2, 0, 3), (T, 0, 0)]), "rotate": tl([(0, 0), (1.2, -1.5), (T, 0)])},
        "ear_l": {"rotate": tl([(0, 0), (1.4, 6), (T, 0)])},
        "ear_r": {"rotate": tl([(0, 0), (1.4, -6), (T, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (1.1, -4), (T, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (1.1, 4), (T, 0)])},
    }}
    # đập: giơ hai tay -> đập xuống, cả người dẹp, bụng rung
    A["attack"] = {"bones": {
        "arm_l": {"rotate": tl([(0, 0), (0.28, -55, EO), (0.36, -60), (0.46, 40, EI), (0.6, 30), (0.9, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.28, 55, EO), (0.36, 60), (0.46, -40, EI), (0.6, -30), (0.9, 0)])},
        "body": {"scale": tl2([(0, 1, 1), (0.28, 0.95, 1.07, EO), (0.36, 0.95, 1.08), (0.46, 1.1, 0.88, EI),
                              (0.58, 0.97, 1.04), (0.7, 1.02, 0.98), (0.9, 1, 1)])},
        "belly": {"scale": tl2([(0, 1, 1), (0.46, 1, 1), (0.52, 1.1, 0.92, EO), (0.62, 0.95, 1.06), (0.72, 1.04, 0.97),
                               (0.9, 1, 1)])},
        "head": {"translate": tl2([(0, 0, 0), (0.3, 0, 6), (0.48, 0, -8, EI), (0.62, 0, 2), (0.9, 0, 0)])},
        "ear_l": {"rotate": tl([(0, 0), (0.3, -8), (0.5, 18, EO), (0.68, -6), (0.9, 0)])},
        "ear_r": {"rotate": tl([(0, 0), (0.3, 8), (0.5, -18, EO), (0.68, 6), (0.9, 0)])},
    }}
    A["hit"] = {"bones": {
        "body": {"rotate": tl([(0, 0), (0.07, 7, EO), (0.2, -3), (0.45, 0)]),
                 "scale": tl2([(0, 1, 1), (0.07, 1.06, 0.92, EO), (0.2, 0.97, 1.03), (0.45, 1, 1)]),
                 "translate": tl2([(0, 0, 0), (0.07, -10, 0, EO), (0.45, 0, 0)])},
        "belly": {"scale": tl2([(0, 1, 1), (0.1, 0.92, 1.08, EO), (0.22, 1.06, 0.95), (0.34, 0.98, 1.02), (0.45, 1, 1)])},
        "head": {"rotate": tl([(0, 0), (0.1, 8, EO), (0.45, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (0.1, -25, EO), (0.45, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.1, 20, EO), (0.45, 0)])},
        "ear_l": {"rotate": tl([(0, 0), (0.12, 15, EO), (0.3, -5), (0.45, 0)])},
        "ear_r": {"rotate": tl([(0, 0), (0.12, -10, EO), (0.3, 5), (0.45, 0)])},
    }}
    # nhảy đè: ngồi lấy đà -> bật lên duỗi người -> rơi -> dẹp mạnh, bụng rung lâu
    A["skill"] = {"bones": {
        "root": {"translate": tl2([(0, 0, 0), (0.3, 0, 0), (0.6, 0, 110, EO), (0.75, 0, 118), (0.92, 0, 0, EI),
                                   (1.6, 0, 0)])},
        "body": {"scale": tl2([(0, 1, 1), (0.3, 1.12, 0.84, EO), (0.45, 0.9, 1.14), (0.75, 1, 1), (0.92, 1.03, 0.98),
                              (0.98, 1.22, 0.76, EO), (1.12, 0.94, 1.06), (1.26, 1.04, 0.97), (1.6, 1, 1)])},
        "belly": {"scale": tl2([(0, 1, 1), (0.98, 1, 1), (1.04, 1.14, 0.88, EO), (1.14, 0.93, 1.08), (1.26, 1.05, 0.96),
                               (1.4, 0.98, 1.02), (1.6, 1, 1)])},
        "arm_l": {"rotate": tl([(0, 0), (0.3, 20), (0.6, -70, EO), (0.8, -75), (0.98, 25, EI), (1.2, 10), (1.6, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.3, -20), (0.6, 70, EO), (0.8, 75), (0.98, -25, EI), (1.2, -10), (1.6, 0)])},
        "foot_l": {"translate": tl2([(0, 0, 0), (0.3, 0, 0), (0.6, -6, 10, EO), (0.75, -6, 12), (0.92, 0, 0, EI),
                                     (1.6, 0, 0)]), "rotate": tl([(0, 0), (0.6, -15), (0.9, 0), (1.6, 0)])},
        "foot_r": {"translate": tl2([(0, 0, 0), (0.3, 0, 0), (0.6, 6, 10, EO), (0.75, 6, 12), (0.92, 0, 0, EI),
                                     (1.6, 0, 0)]), "rotate": tl([(0, 0), (0.6, 15), (0.9, 0), (1.6, 0)])},
        "head": {"translate": tl2([(0, 0, 0), (0.3, 0, -8), (0.5, 0, 6), (0.98, 0, -12, EI), (1.15, 0, 3), (1.6, 0, 0)])},
        "ear_l": {"rotate": tl([(0, 0), (0.5, -12), (0.8, 10), (1.0, 22, EO), (1.2, -8), (1.6, 0)])},
        "ear_r": {"rotate": tl([(0, 0), (0.5, 12), (0.8, -10), (1.0, -22, EO), (1.2, 8), (1.6, 0)])},
    }}
    # đi lạch bạch tại chỗ
    R = 1.0
    A["walk"] = {"bones": {
        "body": {"rotate": tl([(0, 0), (0.25, 6), (0.5, 0), (0.75, -6), (R, 0)]),
                 "translate": tl2([(0, 0, 0), (0.25, 4, 6), (0.5, 0, 0), (0.75, -4, 6), (R, 0, 0)])},
        "foot_l": {"translate": tl2([(0, 0, 0), (0.25, 0, 0), (0.5, 0, 0), (0.75, 0, 14, EO), (R, 0, 0, EI)])},
        "foot_r": {"translate": tl2([(0, 0, 0), (0.25, 0, 14, EO), (0.5, 0, 0, EI), (R, 0, 0)])},
        "belly": {"scale": tl2([(0, 1, 1), (0.3, 1.03, 0.98), (0.5, 1, 1), (0.8, 1.03, 0.98), (R, 1, 1)])},
        "arm_l": {"rotate": tl([(0, 0), (0.25, -10), (0.5, 0), (0.75, 8), (R, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.25, -8), (0.5, 0), (0.75, 10), (R, 0)])},
        "head": {"rotate": tl([(0, 0), (0.3, -3), (0.55, 0), (0.8, 3), (R, 0)])},
        "ear_l": {"rotate": tl([(0, 0), (0.35, 6), (0.85, -6), (R, 0)])},
        "ear_r": {"rotate": tl([(0, 0), (0.35, 6), (0.85, -6), (R, 0)])},
    }}
    return A


ANIMS = {"giot_suong": gs_anims, "snorlax": sn_anims}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cmd, code = sys.argv[1], sys.argv[2]
    if cmd == "one1":  # một ảnh liền: cắt rồi dựng luôn
        one(code)
        build(code)
    if cmd == "one":
        one(code)
    if cmd in ("cut", "all"):
        cut(code)
    if cmd in ("place", "all"):
        place(code)
    if cmd in ("build", "all"):
        build(code)
