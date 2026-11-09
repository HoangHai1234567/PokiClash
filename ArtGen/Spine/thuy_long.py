# -*- coding: utf-8 -*-
"""Thủy Long (dòng Giọt Sương vẽ lại, 3 dạng .atomik, 2026-11-08): cắt mảnh, khớp, dựng rig lưới có trọng số, animation
mềm (IK chân, lò xo đuôi, mào, vải, áo choàng), tiến hóa nối liền sang dạng sau, xuất .atomik + chân dung.

    <venv>/Scripts/python -I ArtGen/Spine/thuy_long.py cut <k> | place <k> [mảnh ...] | rig <k> | all
k = 1, 2, 3. "all": dựng và xuất cả 3 dạng (dạng 3 trước, vì tiến hóa của dạng k chứa dạng k+1).
Mảnh: b = tay, chân bên trái người xem (phía sau), f = bên phải (phía trước, tay cầm vũ khí).
"""
import copy
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import longrig as L  # noqa: E402
import rig as riglib  # noqa: E402
from longrig import curve, wave  # noqa: E402

PROJECT = os.path.normpath(os.path.join(HERE, "..", ".."))
FX_DIR = os.path.join(PROJECT, "ArtGen", "Heroes", "inbox", "giot_suong_fx", "tai_ve")
RES = os.path.join(PROJECT, "Assets", "03 Art", "Heroes", "Resources")
H = 360.0  # chiều cao dáng đứng trong rig (sticker vẽ tối đa ~301 điểm)
WEAPON = {1: "spear", 2: "sword", 3: "glaive"}
GRIP = {1: (92, 60, 36), 2: (44, 40, 52), 3: (60, 46, 36)}


def code(k):
    return f"thuy_long_{k}"


def base(k):
    return os.path.join(HERE, "inbox", code(k))


SHEETS = {k: {"L2a_head.png": [["head", "head_blink", "head_roar", "crest"]],
              "L2b_limbs.png": [["arm_b", "fist_b", "arm_f", "hand_f"], ["leg_b", "foot_b", "leg_f", "foot_f"]],
              "L2c_body.png": [["torso", "tail"] + (["cape"] if k == 3 else []), ["weapon", "shoulder", "cloth"]]}
          for k in (1, 2, 3)}
SWAP = {"head": ["head_blink", "head_roar"]}
for _k in (1, 2, 3):
    riglib.SPEC[code(_k)] = {"base": base(_k), "sheets": SHEETS[_k], "swap": SWAP,
                             "draw": [n for rows in SHEETS[_k].values() for r in rows for n in r]}

# tâm từng mảnh trên L1_duyet.png (đọc ở ảnh kẻ lưới), nửa ô dò, tỉ lệ ước theo khung bao trên L1. Dò tỉ lệ tự do bị lệch về
# mảnh nhỏ (so khớp chuẩn hoá theo diện tích nên mảnh nhỏ lọt vào vùng xanh trơn), nên chỉ dò ±12% quanh tỉ lệ ước.
HINT = {
    1: {"head": (565, 300, 60, 0.97), "crest": (400, 290, 80, 0.82), "torso": (505, 600, 60, 0.95),
        "shoulder": (662, 505, 45, 0.53), "arm_b": (270, 640, 60, 0.88), "fist_b": (250, 845, 45, 0.64),
        "arm_f": (685, 630, 60, 0.85), "hand_f": (740, 795, 40, 0.6), "weapon": (832, 655, 50, 0.92),
        "cloth": (527, 1000, 50, 1.03), "leg_b": (330, 1070, 60, 1.1), "foot_b": (220, 1380, 45, 0.8),
        "leg_f": (700, 1085, 60, 1.1), "foot_f": (778, 1380, 45, 0.8), "tail": (190, 1075, 70, 0.72)},
    2: {"head": (568, 278, 60, 0.85), "crest": (410, 270, 70, 0.75), "torso": (483, 638, 55, 0.82),
        "shoulder": (676, 522, 45, 0.63), "fist_b": (206, 860, 40, 0.75), "hand_f": (730, 880, 40, 0.72),
        "foot_b": (215, 1330, 45, 0.86), "foot_f": (750, 1330, 45, 0.86), "tail": (165, 1060, 70, 0.66)},
    3: {"head": (480, 285, 70, 0.95), "crest": (390, 300, 70, 0.9), "torso": (550, 640, 55, 1.0),
        "shoulder": (650, 530, 50, 0.5), "arm_b": (262, 620, 50, 1.05), "fist_b": (270, 875, 40, 0.75),
        "hand_f": (668, 725, 40, 0.55), "foot_b": (226, 1335, 45, 0.8), "foot_f": (790, 1335, 45, 0.89),
        "tail": (160, 960, 70, 0.85)},
}
ROT = {1: {}, 2: {}, 3: {}}
FIXED = {1: {"crest": {"s": 0.85, "r": 0.0, "cx": 405.0, "cy": 290.0},
             "cloth": {"s": 1.03, "r": 0.0, "cx": 528.0, "cy": 1003.0},
             "hand_f": {"s": 0.62, "r": 12.0, "cx": 740.0, "cy": 790.0}},
         2: {"cloth": {"s": 1.02, "r": 0.0, "cx": 473.0, "cy": 1005.0}},
         3: {"cloth": {"s": 1.15, "r": 0.0, "cx": 535.0, "cy": 1000.0},
             "cape": {"s": 1.6, "r": 0.0, "cx": 518.0, "cy": 930.0}}}
# mảnh dài xanh trơn: đặt theo hai đầu khớp đọc trên L1 (đầu gần thân trước), hai đầu mảnh lấy ở phân số f0, f1 của đường
# dài nhất trong mảnh (bỏ phần đầu tròn thừa ra ở chỗ khớp)
TWO = {
    1: {"arm_b": ((345, 520), (232, 785), (0.07, 0.95)), "arm_f": ((655, 520), (712, 772), (0.07, 0.95)),
        "leg_b": ((410, 820), (250, 1345), (0.06, 0.95)), "leg_f": ((610, 830), (770, 1345), (0.06, 0.95)),
        "weapon": ((690, 900), (990, 412), (0.0, 1.0)), "cloth": ((527, 790), (532, 1220), (0.0, 1.0))},
    2: {"arm_b": ((330, 500), (200, 840), (0.07, 0.95)), "arm_f": ((650, 520), (720, 835), (0.07, 0.95)),
        "leg_b": ((390, 820), (240, 1290), (0.06, 0.95)), "leg_f": ((580, 830), (690, 1290), (0.06, 0.95)),
        "weapon": ((618, 799), (988, 1252), (0.0, 1.0))},
    3: {"arm_f": ((650, 545), (718, 742), (0.07, 0.95)), "leg_b": ((370, 830), (250, 1290), (0.06, 0.95)),
        # đao trên concept dài chéo hết khung, mảnh GPT vẽ cán ngắn hơn: lấy tỉ lệ theo cỡ lưỡi (đốc tới ngang đùi)
        "leg_f": ((590, 840), (697, 1290), (0.06, 0.95)), "weapon": ((332, 1023), (928, 62), (0.0, 1.0))},
}


def place_two(part, q0, q1, f0, f1):
    """phép đồng dạng đưa hai điểm dọc mảnh (phân số f0, f1 của đường dài nhất) tới q0, q1 trên L1."""
    m = part[:, :, 3] > 128
    ys, xs = np.nonzero(m)
    c0 = (float(xs.mean()), float(ys.mean()))
    D0 = L.geodesic(m, [c0])
    a = np.unravel_index(int(np.argmax(np.where(np.isfinite(D0), D0, -1))), D0.shape)
    DA = L.geodesic(m, [(a[1], a[0])])
    b = np.unravel_index(int(np.argmax(np.where(np.isfinite(DA), DA, -1))), DA.shape)
    Lm = float(DA[b])

    def at(f):
        if f <= 0:
            return np.array([a[1], a[0]], float)
        if f >= 1:
            return np.array([b[1], b[0]], float)
        band = np.isfinite(DA) & (np.abs(DA - f * Lm) < 1.6)
        yy, xx = np.nonzero(band)
        return np.array([xx.mean(), yy.mean()])

    q0, q1 = np.array(q0, float), np.array(q1, float)
    vis = lambda v: math.degrees(math.atan2(-v[1], v[0]))  # noqa: E731  góc nhìn (y xuống)
    best = None
    for p0, p1 in ((at(f0), at(f1)), (at(1 - f0), at(1 - f1))):
        r = (vis(q1 - q0) - vis(p1 - p0) + 180) % 360 - 180
        if best is None or abs(r) < abs(best[0]):
            best = (r, p0, p1)
    r, p0, p1 = best
    s = float(np.linalg.norm(q1 - q0) / max(1e-6, np.linalg.norm(p1 - p0)))
    cr, sr = math.cos(math.radians(r)), math.sin(math.radians(r))
    M = np.array([[cr, sr], [-sr, cr]])
    h, w = m.shape
    c = q0 + s * M @ (np.array([w / 2, h / 2]) - p0)
    return {"s": round(s, 4), "r": round(r, 2), "cx": round(float(c[0]), 1), "cy": round(float(c[1]), 1), "err": 0.0}


# ---------------------------------------------------------------- cắt, khớp
def fix_grip(k):
    """lòng nắm tay cầm vũ khí GPT vẽ rỗng, bộ cắt lấp trắng: tô màu cán vũ khí."""
    import cv2
    p = os.path.join(base(k), "parts", "hand_f.png")
    im = np.array(Image.open(p).convert("RGBA"))
    rgb, a = im[:, :, :3].astype(np.int16), im[:, :, 3]
    white = ((rgb.min(2) > 200) & (a > 128)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(white, connectivity=4)
    h, w = a.shape
    done = 0
    for i in range(1, n):
        x, y, bw, bh, area = st[i]
        if area < 80 or x == 0 or y == 0 or x + bw >= w or y + bh >= h:
            continue
        m = cv2.dilate((lab == i).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
        m &= rgb.min(2) > 150
        noise = np.random.default_rng(7).integers(-8, 9, (h, w, 1))
        im[:, :, :3][m] = np.clip(np.array(GRIP[k])[None, None, :] + noise, 0, 255)[m].astype(np.uint8)
        done += int(m.sum())
    Image.fromarray(im).save(p)
    print(f"  hand_f: tô lòng nắm {done} điểm ảnh")


def fix_stubs(k):
    """đầu tròn ở khớp (cổ tay, cổ chân, vai, hông) GPT tô xanh nhạt khác màu da: khi ghép lộ chấm tròn nhạt ở mắt cá, cổ
    tay. Tô các khối tròn xanh nhạt gọn (không phải dải bụng dài) về màu da xanh của chính mảnh."""
    import cv2
    pale = np.array([195, 236, 228])
    for n in ("arm_b", "arm_f", "leg_b", "leg_f", "fist_b", "hand_f", "foot_b", "foot_f"):
        p = os.path.join(base(k), "parts", n + ".png")
        im = np.array(Image.open(p).convert("RGBA"))
        rgb, a = im[:, :, :3].astype(np.int16), im[:, :, 3]
        blue = (rgb[:, :, 2] > rgb[:, :, 0] + 70) & (rgb[:, :, 2] > rgb[:, :, 1] + 20) & (a > 128)
        if blue.sum() < 50:
            continue
        col = np.median(rgb[blue], 0)
        m = ((np.abs(rgb - pale).max(2) < 42) & (a > 128)).astype(np.uint8)
        nc, lab, st, _ = cv2.connectedComponentsWithStats(m, connectivity=4)
        done = 0
        for i in range(1, nc):
            x, y, bw, bh, area = st[i]
            if area < 120 or area > 0.25 * (a > 128).sum():
                continue
            if area / float(bw * bh) < 0.5 or not 0.45 < bw / float(bh) < 2.2:
                continue
            mm = lab == i
            noise = np.random.default_rng(i).integers(-9, 10, mm.sum())[:, None]
            im[:, :, :3][mm] = np.clip(col[None, :] + noise, 0, 255).astype(np.uint8)
            done += 1
        if done:
            Image.fromarray(im).save(p)
            print(f"  {n}: tô {done} đầu khớp nhạt về màu da")


def place(k, redo=None):
    P = riglib.paths(code(k))
    ref = np.array(Image.open(P["ref"]).convert("RGB"))
    Hh, Ww = ref.shape[:2]
    ref_lab = riglib.lab_f(ref)
    pj = os.path.join(P["rig"], "placed.json")
    old = json.load(open(pj))["parts"] if os.path.exists(pj) else {}
    out = {}
    pdir = os.path.join(P["rig"], "placed")
    os.makedirs(pdir, exist_ok=True)
    extras = {e for v in SWAP.values() for e in v}
    for sheet, rows in SHEETS[k].items():
        for name in [n for r in rows for n in r if n not in extras]:
            if name in FIXED[k]:
                out[name] = dict(FIXED[k][name], err=0.0)
                continue
            if name in TWO[k]:
                q0, q1, (f0, f1) = TWO[k][name]
                part = np.array(Image.open(os.path.join(P["parts"], name + ".png")).convert("RGBA"))
                out[name] = place_two(part, q0, q1, f0, f1)
                print(f"  {name:9s} hai đầu: s={out[name]['s']:.3f} r={out[name]['r']:+.0f}", flush=True)
                continue
            if name in old and (redo is None or name not in redo):
                out[name] = {q: old[name][q] for q in ("s", "r", "cx", "cy", "err")}
                continue
            part = np.array(Image.open(os.path.join(P["parts"], name + ".png")).convert("RGBA"))
            cx, cy, win, s0 = HINT[k][name]
            r0, r1 = ROT[k].get(name, (-30, 30))
            c = riglib.match(ref_lab, part, s0 * np.arange(0.88, 1.121, 0.03), range(r0, r1 + 1, 6), 0.25, None, (cx, cy), win)
            c = riglib.match(ref_lab, part, np.arange(c[1] * 0.97, c[1] * 1.031, c[1] * 0.01),
                             np.arange(c[2] - 6, c[2] + 6.1, 2), 0.5, None, (c[3], c[4]), 24)
            err, s, r, x, y = riglib.match(ref_lab, part, np.arange(c[1] * 0.985, c[1] * 1.016, c[1] * 0.005),
                                           np.arange(c[2] - 2, c[2] + 2.1, 1), 1.0, None, (c[3], c[4]), 8)
            out[name] = {"s": round(float(s), 4), "r": round(float(r), 2), "cx": round(float(x), 1), "cy": round(float(y), 1),
                         "err": round(float(err), 1)}
            print(f"  {name:9s} s={s:.3f} r={r:+.0f} tâm=({x:.0f},{y:.0f}) gợi ý=({cx},{cy}) sai={err:.0f}", flush=True)
    for main_, exs in SWAP.items():
        for ex in exs:
            out[ex] = dict(out[main_], of=main_)
    comp = np.full((Hh, Ww, 3), 255, np.float32)
    for name, t in out.items():
        part = np.array(Image.open(os.path.join(P["parts"], name + ".png")).convert("RGBA"))
        wp = riglib.warp(part, t["s"], t["r"])
        Image.fromarray(wp).save(os.path.join(pdir, name + ".png"))
        t["w"], t["h"] = int(wp.shape[1]), int(wp.shape[0])
        t["x0"], t["y0"] = int(round(t["cx"] - wp.shape[1] / 2)), int(round(t["cy"] - wp.shape[0] / 2))
    for name in DRAW[k]:
        t = out[name]
        riglib.paste(comp, np.array(Image.open(os.path.join(pdir, name + ".png"))), t["x0"], t["y0"])
    comp = comp.astype(np.uint8)
    rfg, cfg = riglib.fg_mask(ref), riglib.fg_mask(comp)
    iou = float((cfg & rfg).sum() / max(1, (cfg | rfg).sum()))
    Image.fromarray(np.concatenate([ref, comp], 1)).save(os.path.join(P["rig"], "so_ghep.png"))
    json.dump({"ref_size": [Ww, Hh], "iou": round(iou, 4), "parts": out}, open(pj, "w"), indent=1)
    print(f"IoU = {iou:.3f} -> {os.path.join(P['rig'], 'so_ghep.png')}")


# ---------------------------------------------------------------- rig
DRAW = {k: (["cape"] if k == 3 else []) + ["tail", "crest", "leg_b", "foot_b", "arm_b", "fist_b", "leg_f", "foot_f",
                                           "torso", "cloth", "head", "arm_f", "shoulder", "weapon", "hand_f"]
        for k in (1, 2)}
# dạng 3: giáp vai trái nằm liền mảnh tay sau, phải đè lên vai thân nên tay sau vẽ sau thân
DRAW[3] = ["cape", "tail", "crest", "leg_b", "foot_b", "leg_f", "foot_f", "torso", "cloth", "arm_b", "fist_b", "head",
           "arm_f", "shoulder", "weapon", "hand_f"]

FX = {  # ảnh: (tệp, cạnh dài lưu atlas)
    "FX01": ("FX01.png", 150), "FX02": ("FX02.png", 130), "FX03": ("FX03.png", 120), "FX04": ("FX04.png", 80),
    "FX05": ("FX05.png", 56), "FX06": ("FX06.png", 110), "FX07": ("FX07.png", 160), "FX08": ("FX08.png", 150),
    "FX09": ("FX09.png", 160),
}


def fx_image(name):
    f, keep = FX[name]
    rgb = np.array(Image.open(os.path.join(FX_DIR, f)).convert("RGB"))
    m = riglib.fg_mask(rgb)
    rgba = riglib.to_rgba(rgb, m)
    ys, xs = np.where(m > 0)
    im = Image.fromarray(rgba[ys.min():ys.max() + 1, xs.min():xs.max() + 1])
    s = keep / max(im.size)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def shadow_image(w):
    w, h = int(w), int(w * 0.2)
    im = Image.new("L", (w * 4, h * 4), 0)
    ImageDraw.Draw(im).ellipse([4, 4, w * 4 - 4, h * 4 - 4], fill=255)
    a = np.array(im.resize((w, h), Image.LANCZOS)).astype(np.float32) / 255 * 0.2
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[:, :, :3] = (40, 48, 64)
    rgba[:, :, 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(rgba)


class Ctx:
    pass


def build_rig(k):
    """rig một dạng: xương (gốc, move, hông, lưng 3 đốt, cổ + đầu, mào, tay 2 đoạn, chân 2 đoạn, đuôi 4 đốt, vải, áo choàng),
    slot theo thứ tự vẽ, lưới có trọng số cho mảnh chuỗi, hình cứng cho bàn tay, bàn chân, vũ khí, giáp vai; hiệu ứng."""
    P = riglib.paths(code(k))
    pl = json.load(open(os.path.join(P["rig"], "placed.json")))
    W1, H1 = pl["ref_size"]
    parts = pl["parts"]
    pimg = {n: np.array(Image.open(os.path.join(P["rig"], "placed", n + ".png"))) for n in parts}
    mask = {n: riglib.placed_mask(parts[n], pimg[n], W1, H1) for n in parts}
    ground = max(parts[n]["y0"] + parts[n]["h"] for n in ("foot_b", "foot_f")) - 8
    feet_x = (parts["foot_b"]["cx"] + parts["foot_f"]["cx"]) / 2
    top = min(int(np.where(mask[n].any(1))[0].min()) for n in ("head", "crest"))
    ks = H / (ground - top)

    def S(p):
        return ((p[0] - feet_x) * ks, (ground - p[1]) * ks)

    def piece(n):
        im = Image.fromarray(pimg[n])
        im = im.resize((max(1, round(im.width * ks)), max(1, round(im.height * ks))), Image.LANCZOS)
        t = parts[n]
        return L.Piece(n, np.array(im), (t["x0"] - feet_x) * ks, (ground - t["y0"]) * ks)

    def J(a, b):
        return S(riglib.joint(mask[a], mask[b]))

    pc = {n: piece(n) for n in parts}
    R = L.Rig(code(k))
    info, chains = {}, {}  # chains: slot -> (mảnh, xương, cha, khớp, bản đồ s, blend, parent_blend)

    def mk(bones, parent, joints):
        p = parent
        for b, j in zip(bones, joints):
            R.bone(b, p, j[0], j[1])
            p = b

    def top_point(pi):
        ys, xs = np.nonzero(pi.mask)
        return pi.to_rig(float(xs[ys == ys.min()].mean()), float(ys.min()) + 2)

    R.bone("root", None, 0, 0)
    R.bone("move", "root", 0, 0)
    R.bone("shadow", "root", 0, 0)
    hip_b, hip_f = J("leg_b", "torso"), J("leg_f", "torso")
    pelvis = ((hip_b[0] + hip_f[0]) / 2, (hip_b[1] + hip_f[1]) / 2)
    neck = J("head", "torso")
    R.bone("hip", "move", *pelvis)
    # lưng: hông -> cổ, 3 đốt
    j, s = pc["torso"].chain(pelvis, neck, n=3)
    mk(["spine1", "spine2", "chest"], "hip", j)
    chains["torso"] = (["spine1", "spine2", "chest"], "hip", s, 0.22, 0.0)
    # cổ + đầu: 2 đốt từ chỗ cổ cắm vào thân tới điểm xa nhất của đầu (khớp giữa ~ dưới hàm)
    j, s = pc["head"].chain(neck, n=2, end_far=True)
    mk(["neck", "head"], "chest", j)
    chains["head"] = (["neck", "head"], "chest", s, 0.16, 0.0)
    info["head_s"] = s
    # mào / bờm: 3 đốt từ chỗ gắn đầu
    j, s = pc["crest"].chain(J("crest", "head"), n=3, end_far=True)
    mk(["crest1", "crest2", "crest3"], "head", j)
    chains["crest"] = (["crest1", "crest2", "crest3"], "head", s, 0.2, 0.15)
    info["crest_tip"] = j[-1]
    # tay: vai -> khuỷu -> cổ tay; nắm tay cứng
    for sd, hand in (("b", "fist_b"), ("f", "hand_f")):
        wr = J(hand, f"arm_{sd}")
        j, s = pc[f"arm_{sd}"].chain(J(f"arm_{sd}", "torso"), wr, n=2)
        mk([f"arm_{sd}1", f"arm_{sd}2"], "chest", j)
        chains[f"arm_{sd}"] = ([f"arm_{sd}1", f"arm_{sd}2"], "chest", s, 0.2, 0.1)
        R.bone(hand, f"arm_{sd}2", *wr)
    # vũ khí: gắn bàn tay trước tại chỗ nắm; mũi = điểm xa chỗ nắm nhất
    gx, gy = riglib.joint(mask["weapon"], mask["hand_f"])
    grip = S((gx, gy))
    R.bone("weapon", "hand_f", *grip)
    ys, xs = np.where(mask["weapon"] > 0)
    i = int(np.argmax((xs - gx) ** 2 + (ys - gy) ** 2))
    tip = S((float(xs[i]), float(ys[i])))
    R.point("tip", "weapon", *tip)
    info["tip"], info["grip"] = tip, grip
    # chân: hông -> gối -> cổ chân; bàn chân cứng; IK
    for sd, hp in (("b", hip_b), ("f", hip_f)):
        an = J(f"foot_{sd}", f"leg_{sd}")
        j, s = pc[f"leg_{sd}"].chain(hp, an, n=2)
        mk([f"leg_{sd}1", f"leg_{sd}2"], "hip", j)
        chains[f"leg_{sd}"] = ([f"leg_{sd}1", f"leg_{sd}2"], "hip", s, 0.2, 0.08)
        R.bone(f"foot_{sd}", f"leg_{sd}2", *an)
        R.legs[sd] = (f"leg_{sd}1", f"leg_{sd}2", f"foot_{sd}")
    R.ik_space = "root"
    # đuôi 4 đốt
    tr = J("tail", "torso") if (mask["tail"] & mask["torso"]).any() else J("tail", "leg_b")
    j, s = pc["tail"].chain(tr, n=4, end_far=True)
    mk(["tail1", "tail2", "tail3", "tail4"], "hip", j)
    chains["tail"] = (["tail1", "tail2", "tail3", "tail4"], "hip", s, 0.2, 0.1)
    info["tail_tip"] = j[-1]
    # vải trước 3 đốt từ mép trên
    j, s = pc["cloth"].chain(top_point(pc["cloth"]), n=3, end_far=True)
    mk(["cloth1", "cloth2", "cloth3"], "spine1", j)
    chains["cloth"] = (["cloth1", "cloth2", "cloth3"], "spine1", s, 0.22, 0.15)
    info["cloth_tip"] = j[-1]
    if "cape" in pc:  # áo choàng 4 đốt từ vai
        j, s = pc["cape"].chain(top_point(pc["cape"]), n=4, end_far=True)
        mk(["cape1", "cape2", "cape3", "cape4"], "chest", j)
        chains["cape"] = (["cape1", "cape2", "cape3", "cape4"], "chest", s, 0.22, 0.2)
        info["cape_tip"] = j[-1]
    # xương hiệu ứng: theo move (đi theo cú lao), mũi vũ khí theo vũ khí
    cx0, cy0 = R.bw("spine2")
    fxb = {"fx_ring": ("move", cx0, cy0), "fx_ground": ("move", 0.0, 0.02 * H), "fx_slash": ("move", 0.5 * H, 0.5 * H),
           "fx_splash": ("move", 0.72 * H, 0.45 * H), "fx_wave": ("move", 0.9 * H, 0.0), "fx_spark": ("weapon", tip[0], tip[1]),
           "fx_drops": ("chest", R.bw("chest")[0] + 0.12 * H, R.bw("chest")[1]), "fx_tip": ("weapon", tip[0], tip[1]),
           "fx_jet": ("weapon", tip[0], tip[1]), "fx_geyser": ("move", 0.5 * H, 0.0)}
    for b, (par, x, y) in fxb.items():
        R.bone(b, par, x, y)

    # slot theo thứ tự vẽ: bóng, hiệu ứng sau lưng, mảnh, hiệu ứng trước mặt
    for n in FX:
        R.images[n] = fx_image(n)
    R.images["shadow"] = shadow_image(abs(R.bw("foot_f")[0] - R.bw("foot_b")[0]) + 0.2 * H)
    weapon_ang = math.degrees(math.atan2(tip[1] - grip[1], tip[0] - grip[0]))

    def fx(slot, bone, img, size, rot=0.0, ox=0.0, oy=0.0):
        im = R.images[img]
        sc = size / max(im.size)
        bx, by = R.bw(bone)
        R.slot(slot, bone, None, fx=True)
        R.region(slot, slot, img, bone, bx + ox, by + oy, im.width * sc, im.height * sc, rot)

    R.slot("shadow", "shadow", "shadow")
    R.region("shadow", "shadow", "shadow", "shadow", 0, 0)
    fx("fx_ground", "fx_ground", "FX08", 0.95 * H)
    fx("fx_ring_b", "fx_ring", "FX01", 1.0 * H)
    first = {n: c[0][0] for n, c in chains.items()}
    for n in DRAW[k]:
        bone = first.get(n, {"shoulder": "arm_f1"}.get(n, n))
        R.slot(n, bone, n)
        if n in chains:
            bones, parent, s, bl, pb = chains[n]
            L.add_chain_piece(R, pc[n], n, n, bones, parent, None, s, blend=bl, parent_blend=pb, make_bones=False)
        elif n == "shoulder":
            R.images[n] = Image.fromarray(pc[n].rgba)
            h_, w_ = pc[n].mask.shape
            R.region(n, n, n, "arm_f1", *pc[n].to_rig(w_ / 2, h_ / 2))
        else:
            L.add_rigid_piece(R, pc[n], n, n, n)
        if n == "head":  # mặt nhắm mắt, mặt gầm: cùng xương cổ + đầu, trọng số lấy theo bản đồ s của đầu chính
            hp = pc["head"]
            hs = info["head_s"]
            for ex in SWAP["head"]:
                pe = pc[ex]
                pts, nh, tris = pe.make_mesh(9, 16)
                vw = np.array([pe.to_rig(x, y) for x, y in pts])
                pxy = np.array([hp.to_px(X, Y) for X, Y in vw])
                sv = L.sample_map(hs, pxy)
                wts = L.chain_weights(sv, ["neck", "head"], "chest", 0.16, 0.0)
                hh, ww = pe.mask.shape
                R.images[ex] = Image.fromarray(pe.rgba)
                R.mesh("head", ex, ex, vw, np.stack([pts[:, 0] / ww, pts[:, 1] / hh], 1), tris, nh, wts)
    fx("fx_ring_f", "fx_ring", "FX01", 1.0 * H)
    fx("fx_jet", "fx_jet", "FX09", 0.9 * H, rot=weapon_ang,
       ox=0.42 * H * math.cos(math.radians(weapon_ang)), oy=0.42 * H * math.sin(math.radians(weapon_ang)))
    fx("fx_slash", "fx_slash", "FX02", 0.62 * H)
    fx("fx_splash", "fx_splash", "FX03", 0.5 * H)
    fx("fx_wave", "fx_wave", "FX07", 0.85 * H)
    fx("fx_geyser", "fx_geyser", "FX09", 1.0 * H, rot=90, oy=0.5 * H)  # tia nước dựng đứng: cột nước phụt từ đất
    fx("fx_drops", "fx_drops", "FX04", 0.3 * H)
    fx("fx_tip", "fx_tip", "FX06", 0.2 * H)
    fx("fx_spark", "fx_spark", "FX05", 0.22 * H)
    R.weapon_ang = weapon_ang
    R.chain_tips = {n: info[n + "_tip"] for n in ("tail", "crest", "cloth", "cape") if n + "_tip" in info}

    ctx = Ctx()
    ctx.k, ctx.R, ctx.info = k, R, info
    ctx.ank = {sd: R.bw(f"foot_{sd}") for sd in ("b", "f")}
    ctx.parts, ctx.pimg, ctx.ground, ctx.feet_x, ctx.top = parts, pimg, ground, feet_x, top
    return R, ctx


def springs(R, prefix=""):
    """chuỗi mềm: độ cứng giảm dần ra ngọn (ngọn trễ hơn); vải cứng hơn đuôi để không bay ngang như cờ."""
    def tipw(last, tipxy):
        bx, by = R.bw(prefix + last)
        return (tipxy[0] - bx, tipxy[1] - by)
    cfg = {}
    chains = {"tail": (["tail1", "tail2", "tail3", "tail4"], [190, 140, 100, 75], 0.48),
              "crest": (["crest1", "crest2", "crest3"], [230, 170, 125], 0.5),
              "cloth": (["cloth1", "cloth2", "cloth3"], [380, 290, 220], 0.65),
              "cape": (["cape1", "cape2", "cape3", "cape4"], [170, 130, 100, 78], 0.52)}
    for name, (bones, kk, d) in chains.items():
        if prefix + bones[0] not in R.bi:
            continue
        tip = R.chain_tips[name] if not prefix else R.chain_tips[prefix + name]
        cfg[prefix + name] = {"bones": [prefix + b for b in bones], "k": kk, "damp": d, "tip": tipw(bones[-1], tip)}
    return cfg


ARM_F = ["spine1", "spine2", "chest", "arm_f1", "arm_f2"]


def aim(P, R, ang, pre=""):
    """xoay cổ tay để vũ khí chĩa đúng góc ang (độ, trong không gian, ngược kim): vũ khí không vắt qua mặt."""
    acc = sum(P.t.get(pre + b, [0, 0, 0, 1, 1])[2] for b in ARM_F)
    P._g(pre + "hand_f")[2] = ang - R.weapon_ang - acc


def bend(P, v, pre=""):
    """cong lưng (dương: ngả ra sau), chia cho 3 đốt."""
    for b, f_ in (("spine1", 0.3), ("spine2", 0.35), ("chest", 0.35)):
        P.rot(pre + b, f_ * v)


def fx_on(P, slot, t, t0, t1, rise=0.0, fade=None, amax=1.0):
    """hiện hiệu ứng trong [t0, t1): đậm dần trong rise giây, tan dần trong fade giây cuối."""
    if not (t0 <= t < t1):
        P.att[slot] = None
        return
    P.att[slot] = slot
    fade = (t1 - t0) * 0.45 if fade is None else fade
    a = amax
    if rise > 0:
        a *= L.smooth01((t - t0) / rise)
    a *= 1 - L.smooth01((t - (t1 - fade)) / max(1e-6, fade))
    P.alpha[slot] = a


def plant(P, ctx, pre="", fb=(0, 0), ff=(0, 0), ab=0.0, af=0.0):
    """bàn chân bám đất tại chỗ gốc (+ độ lệch)."""
    for sd, d, a in (("b", fb, ab), ("f", ff, af)):
        x, y = ctx.ank[sd]
        P.feet[pre + sd] = (x + d[0], y + d[1], a)


def breathe(P, t, D, amp=1.0, pre=""):
    """thở: hông nhún, lưng cong nhẹ, vai, đầu, tay; mọi dao động bằng 0 ở t = 0 (khung đầu là dáng nghỉ)."""
    u = 2 * math.pi * t / D
    P.move(pre + "hip", 0, amp * 3.0 * (math.cos(u) - 1))
    P.rot(pre + "spine2", amp * 1.2 * math.sin(u))
    P.rot(pre + "chest", amp * 1.5 * math.sin(u))
    P.move(pre + "chest", 0, amp * 1.2 * (1 - math.cos(u)))
    P.rot(pre + "neck", amp * -0.8 * math.sin(u))
    P.rot(pre + "head", amp * (-1.4 * math.sin(u) + 0.6 * math.sin(2 * u)))
    P.rot(pre + "arm_b1", amp * -2.2 * math.sin(u))
    P.rot(pre + "arm_b2", amp * -3.0 * math.sin(u))
    P.rot(pre + "fist_b", amp * 2.0 * math.sin(u))
    P.rot(pre + "arm_f1", amp * 1.6 * math.sin(u))
    P.rot(pre + "arm_f2", amp * 2.4 * math.sin(u))
    P.rot(pre + "hand_f", amp * -1.8 * math.sin(u))
    P.rot(pre + "tail1", amp * 4.0 * math.sin(u))
    P.rot(pre + "tail2", amp * 3.0 * math.sin(u))
    P.rot(pre + "crest1", amp * 2.0 * math.sin(u))


def idle(ctx):
    """đứng thủ thế: thở, liếc mắt (chớp), ngón vũ khí nhích; đuôi, mào, vải đung đưa trễ pha nhờ lò xo."""
    D = 2.4

    def f(t, P):
        breathe(P, t, D)
        u = 2 * math.pi * t / D
        P.rot("fist_b", 3.0 * math.sin(2 * u))  # siết nắm tay
        plant(P, ctx)
        P.att["head"] = "head_blink" if 1.55 <= t < 1.68 else "head"
    return {"dur": D, "loop": True, "fn": f}


def hit(ctx):
    D = 0.6

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        mx = c([(0, 0), (0.08, -24, "o"), (0.2, -30), (D, 0)])
        P.move("move", mx, 0)
        P.move("shadow", mx, 0)
        P.move("hip", 0, c([(0, 0), (0.1, -7, "o"), (0.3, -3), (D, 0)]))
        b = c([(0, 0), (0.07, 1, "o"), (0.22, 0.6), (D, 0)])
        bend(P, 15 * b)
        P.rot("neck", c([(0, 0), (0.06, 6, "o"), (0.25, 2), (D, 0)]))
        P.rot("head", c([(0, 0), (0.06, 10, "o"), (0.2, 5), (0.4, -2), (D, 0)]))
        P.rot("arm_b1", -20 * b)
        P.rot("arm_b2", -26 * b)
        P.rot("arm_f1", 14 * b)
        P.rot("arm_f2", 18 * b)
        P.rot("hand_f", c([(0, 0), (0.1, 10, "o"), (0.3, -4), (D, 0)]))
        plant(P, ctx, fb=(mx * 0.75, 0), ff=(mx * 0.85, 0))
        P.att["head"] = "head_blink" if 0.02 <= t < 0.3 else "head"
        fx_on(P, "fx_drops", t, 0.02, 0.42, fade=0.28)
        P.move("fx_drops", c([(0, 0), (0.42, 30, "o")]), c([(0, 0), (0.42, 26, "o")]))
        P.scale("fx_drops", c([(0, 0.6), (0.42, 1.15, "o")]))
    return {"dur": D, "fn": f}


def lunge_feet(P, ctx, t, t0, t1, dx_f, dx_b, back_t, D, lift=16):
    """bước lao: chân trước bước tới (nhấc cong), chân sau trượt theo ít hơn, rồi cả hai về."""
    stepf = curve(t, [(0, 0), (t0, -6), (t1, dx_f, "i"), (back_t, dx_f), (D, 0)])
    stepb = curve(t, [(0, 0), (t0 + 0.04, 0), (t1 + 0.05, dx_b), (back_t, dx_b), (D, 0)])
    u = (t - t0) / max(1e-6, t1 - t0)
    up = lift * math.sin(math.pi * u) if 0 < u < 1 else 0
    u2 = (t - back_t) / max(1e-6, D - back_t)
    up += lift * 0.6 * math.sin(math.pi * u2) if 0 < u2 < 1 else 0
    plant(P, ctx, fb=(stepb, 0), ff=(stepf, up))


def leap_feet(P, ctx, t, mx, my, keys_air, keys_land, D):
    """nhảy: chân bám đất -> co theo thân khi bay -> dậm xuống chỗ mới."""
    c = lambda ks: curve(t, ks)  # noqa: E731
    air = c(keys_air)
    for sd in ("b", "f"):
        x, y = ctx.ank[sd]
        gx = c(keys_land[sd])
        bx, by = x + mx + (0.05 * H if sd == "f" else -0.03 * H), y + my + 0.12 * H
        P.feet[sd] = (x + gx + (bx - x - gx) * air, y + (by - y) * air, (-22 if sd == "b" else 18) * air)


def attack(ctx):
    return {"spear": attack_spear, "sword": attack_sword, "glaive": attack_glaive}[WEAPON[ctx.k]](ctx)


def attack_spear(ctx):
    """đâm giáo: rụt tay lấy đà, bước lao đâm thẳng (giáo nằm ngang), tia nước phụt ở mũi, rút về."""
    D, h = 0.95, 0.42
    W0 = ctx.R.weapon_ang

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        mx = c([(0, 0), (0.24, -16), (h, 0.55 * H, "i"), (0.52, 0.53 * H, "o"), (D, 0)])
        P.move("move", mx, 0)
        P.move("shadow", mx, 0)
        P.move("hip", 0, c([(0, 0), (0.22, -12), (h - 0.05, -3), (h, -9, "o"), (0.62, -6), (D, 0)]))
        bend(P, c([(0, 0), (0.22, 7), (h, -10, "o"), (0.62, -6), (D, 0)]))
        P.rot("neck", c([(0, 0), (0.22, 3), (h, -5, "o"), (D, 0)]))
        P.rot("head", c([(0, 0), (0.22, 3), (h, -4, "o"), (0.65, -2), (D, 0)]))
        P.rot("arm_f1", c([(0, 0), (0.22, -30), (h, 36, "o"), (0.62, 28), (D, 0)]))
        P.rot("arm_f2", c([(0, 0), (0.22, 42), (h, -12, "o"), (0.62, -6), (D, 0)]))
        aim(P, ctx.R, c([(0, W0), (0.22, 22), (h, 3, "o"), (0.62, 6), (D, W0)]))
        P.rot("arm_b1", c([(0, 0), (0.22, 14), (h, -32, "o"), (0.65, -18), (D, 0)]))
        P.rot("arm_b2", c([(0, 0), (0.22, -12), (h, -28, "o"), (D, 0)]))
        lunge_feet(P, ctx, t, 0.24, h, 0.6 * H, 0.42 * H, 0.56, D)
        P.att["head"] = "head_roar" if 0.27 <= t < 0.7 else "head"
        fx_on(P, "fx_jet", t, h - 0.04, h + 0.26, fade=0.16)
        P.scale("fx_jet", c([(0, 0.4), (h - 0.04, 0.4), (h + 0.1, 1.1, "o"), (D, 1.15)]),
                c([(0, 0.6), (h + 0.1, 1.0, "o"), (D, 1.0)]))
        fx_on(P, "fx_splash", t, h, h + 0.3, fade=0.2)
        P.scale("fx_splash", c([(0, 0.4), (h, 0.4), (h + 0.22, 1.2, "o"), (D, 1.2)]))
        P.move("fx_splash", 0.08 * H, 0.05 * H)
    return {"dur": D, "fn": f, "hit": h}


def attack_sword(ctx):
    """chém kiếm: giơ kiếm dựng bên phải đầu, bước lao chém chéo xuống, sóng lưỡi liềm, dư lực rồi về."""
    D, h = 1.0, 0.44
    W0 = ctx.R.weapon_ang

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        mx = c([(0, 0), (0.22, -12), (h, 0.52 * H, "i"), (0.56, 0.5 * H, "o"), (D, 0)])
        P.move("move", mx, 0)
        P.move("shadow", mx, 0)
        P.move("hip", 0, c([(0, 0), (0.2, -12), (h, -10, "o"), (0.64, -6), (D, 0)]))
        bend(P, c([(0, 0), (0.2, 6), (h, -9, "o"), (0.62, -5), (D, 0)]))
        P.rot("chest", c([(0, 0), (0.2, -5), (h, 7, "o"), (D, 0)]))
        P.rot("head", c([(0, 0), (0.2, 4), (h, -5, "o"), (D, 0)]))
        P.rot("arm_f1", c([(0, 0), (0.22, 100, "io"), (h - 0.07, 108), (h + 0.02, -26, "o"), (0.62, -16), (D, 0)]))
        P.rot("arm_f2", c([(0, 0), (0.22, 18), (h - 0.07, 22), (h + 0.02, -8, "o"), (D, 0)]))
        aim(P, ctx.R, c([(0, W0), (0.22, 78), (h - 0.07, 86), (h + 0.03, -64, "o"), (0.62, -56), (D, W0)]))
        P.rot("arm_b1", c([(0, 0), (0.22, 18), (h, -34, "o"), (0.66, -16), (D, 0)]))
        P.rot("arm_b2", c([(0, 0), (0.22, -14), (h, -26, "o"), (D, 0)]))
        lunge_feet(P, ctx, t, 0.22, h, 0.56 * H, 0.38 * H, 0.6, D)
        P.att["head"] = "head_roar" if 0.26 <= t < 0.72 else "head"
        fx_on(P, "fx_slash", t, h - 0.04, h + 0.26, fade=0.18)
        P.scale("fx_slash", c([(0, 0.7), (h - 0.04, 0.7), (h + 0.18, 1.2, "o"), (D, 1.2)]))
        P.rot("fx_slash", -15)
        fx_on(P, "fx_splash", t, h, h + 0.3, fade=0.2)
        P.scale("fx_splash", c([(0, 0.4), (h, 0.4), (h + 0.22, 1.25, "o"), (D, 1.25)]))
    return {"dur": D, "fn": f, "hit": h}


def attack_glaive(ctx):
    """bổ đại đao: nhấc đao dựng bên phải đầu, bước tới bổ thẳng xuống đất trước mặt, đất nứt sóng, nước bắn."""
    D, h = 1.1, 0.52
    W0 = ctx.R.weapon_ang

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        mx = c([(0, 0), (0.28, -14), (h, 0.5 * H, "i"), (0.66, 0.48 * H, "o"), (D, 0)])
        P.move("move", mx, 0)
        P.move("shadow", mx, 0)
        P.move("hip", 0, c([(0, 0), (0.26, -14), (h - 0.08, 2), (h, -16, "o"), (0.72, -10), (D, 0)]))
        bend(P, c([(0, 0), (0.26, 9), (h, -12, "o"), (0.72, -6), (D, 0)]))
        P.rot("head", c([(0, 0), (0.26, 5), (h, -6, "o"), (D, 0)]))
        # tay cầm ở giữa ngực: giơ lệch sang phải, đao nghiêng phải (cán không dựng trước mặt)
        P.rot("arm_f1", c([(0, 0), (0.3, 70, "io"), (h - 0.1, 78), (h, -8, "i"), (0.72, -4), (D, 0)]))
        P.rot("arm_f2", c([(0, 0), (0.3, -12), (h, -14, "o"), (D, 0)]))
        aim(P, ctx.R, c([(0, W0), (0.3, 66), (h - 0.1, 72), (h, -32, "i"), (0.72, -28), (D, W0)]))
        P.rot("arm_b1", c([(0, 0), (0.28, 30), (h, -30, "o"), (0.72, -14), (D, 0)]))
        P.rot("arm_b2", c([(0, 0), (0.28, -20), (h, -30, "o"), (D, 0)]))
        lunge_feet(P, ctx, t, 0.28, h, 0.52 * H, 0.36 * H, 0.72, D, lift=12)
        P.att["head"] = "head_roar" if 0.3 <= t < 0.8 else "head"
        fx_on(P, "fx_slash", t, h - 0.05, h + 0.28, fade=0.2)
        P.scale("fx_slash", c([(0, 0.8), (h - 0.05, 0.8), (h + 0.2, 1.45, "o"), (D, 1.45)]))
        P.rot("fx_slash", -40)
        fx_on(P, "fx_ground", t, h, h + 0.45, fade=0.25)
        P.move("fx_ground", 0.62 * H, 0)
        P.scale("fx_ground", c([(0, 0.4), (h, 0.4), (h + 0.35, 1.2, "o"), (D, 1.2)]), c([(0, 0.4), (h, 0.4), (h + 0.35, 1.0, "o"), (D, 1.0)]))
        fx_on(P, "fx_splash", t, h, h + 0.32, fade=0.2)
        P.move("fx_splash", -0.05 * H, -0.3 * H)
        P.scale("fx_splash", c([(0, 0.5), (h, 0.5), (h + 0.24, 1.4, "o"), (D, 1.4)]))
    return {"dur": D, "fn": f, "hit": h}


def cast(ctx):
    """chiêu mana: dựng vũ khí thẳng đứng bên phải đầu, nước tụ ở mũi (bong bóng xoáy, lấp lánh), rồi chĩa thẳng tới;
    trận bắn tia từ mũi ở khung trúng. Không xoay người, không quệt vũ khí qua mặt."""
    D, h = 1.0, 0.56
    W0 = ctx.R.weapon_ang

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        P.move("hip", 0, c([(0, 0), (0.28, -8), (h - 0.05, -10), (h, -4, "o"), (0.82, -3), (D, 0)]))
        bend(P, c([(0, 0), (0.28, 5), (h - 0.05, 7), (h, -8, "o"), (0.82, -5), (D, 0)]))
        P.rot("arm_f1", c([(0, 0), (0.3, 108), (h - 0.05, 113), (h, 52, "o"), (0.82, 48), (D, 0)]))
        P.rot("arm_f2", c([(0, 0), (0.3, 10), (h, -14, "o"), (0.82, -10), (D, 0)]))
        aim(P, ctx.R, c([(0, W0), (0.3, 92), (h - 0.05, 95), (h, 4, "o"), (0.82, 6), (D, W0)]))
        P.rot("arm_b1", c([(0, 0), (0.3, 18), (h, -18, "o"), (D, 0)]))
        P.rot("arm_b2", c([(0, 0), (0.3, -26), (h, -22), (D, 0)]))
        P.rot("neck", c([(0, 0), (0.3, 4), (h, -4, "o"), (D, 0)]))
        P.rot("head", c([(0, 0), (0.3, 5), (h, -5, "o"), (D, 0)]))
        plant(P, ctx, ff=(c([(0, 0), (h - 0.08, 0), (h, 14, "o"), (0.8, 14), (D, 0)]), 0))
        P.att["head"] = "head_roar" if h - 0.08 <= t < 0.82 else "head"
        fx_on(P, "fx_tip", t, 0.14, h + 0.08, rise=0.18, fade=0.08, amax=0.95)
        P.scale("fx_tip", c([(0, 0.3), (0.14, 0.35), (h - 0.02, 1.25), (h + 0.08, 1.6, "o"), (D, 1.6)]))
        P.rot("fx_tip", c([(0, 0), (D, -220, "l")]))
        fx_on(P, "fx_spark", t, 0.24, h + 0.04, rise=0.1, fade=0.1)
        P.scale("fx_spark", c([(0, 0.4), (0.4, 1.1, "o"), (h, 0.7)]))
        P.rot("fx_spark", c([(0, 0), (D, 140, "l")]))
    return {"dur": D, "fn": f, "hit": h}


def skill(ctx):
    return {"spear": skill_spear, "sword": skill_sword, "glaive": skill_glaive}[WEAPON[ctx.k]](ctx)


def skill_fx_charge(P, t, c, t_end=0.66):
    """tụ lực: lốc nước quanh người và vòng sóng dưới chân."""
    fx_on(P, "fx_ring_b", t, 0.0, t_end, rise=0.25, fade=0.18, amax=0.85)
    fx_on(P, "fx_ring_f", t, 0.0, t_end, rise=0.25, fade=0.18, amax=0.5)
    P.rot("fx_ring", c([(0, 0), (t_end, -520, "l")]))
    P.scale("fx_ring", c([(0, 0.5), (0.3, 1.05, "o"), (t_end, 1.25)]))


def skill_fx_impact(P, t, c, h, at=0.5 * H, wave=True):
    """cú đánh xuống đất: vòng sóng, nổ nước, cột nước phụt, sóng thần sau đối thủ."""
    fx_on(P, "fx_ground", t, h, h + 0.5, fade=0.28)
    P.move("fx_ground", at, 0)
    P.scale("fx_ground", c([(0, 0.4), (h, 0.4), (h + 0.4, 1.35, "o"), (h + 1, 1.35)]))
    fx_on(P, "fx_geyser", t, h, h + 0.55, fade=0.25)
    P.scale("fx_geyser", c([(0, 0.6), (h, 0.6), (h + 0.18, 1.15, "o"), (h + 0.45, 1.25), (h + 1, 1.25)]),
            c([(0, 0.15), (h, 0.15), (h + 0.2, 1.0, "o"), (h + 1, 1.05)]))
    P.move("fx_geyser", at - 0.5 * H, 0)
    fx_on(P, "fx_splash", t, h, h + 0.36, fade=0.22)
    P.scale("fx_splash", c([(0, 0.5), (h, 0.5), (h + 0.26, 1.6, "o"), (h + 1, 1.6)]))
    P.move("fx_splash", at - 0.72 * H, -0.32 * H)
    if wave:
        fx_on(P, "fx_wave", t, h + 0.05, h + 0.7, fade=0.28)
        P.scale("fx_wave", c([(0, 0.4), (h + 0.05, 0.4), (h + 0.27, 1.15, "o"), (h + 0.55, 1.25), (h + 1, 1.25)]),
                c([(0, 0.2), (h + 0.05, 0.2), (h + 0.27, 1.15, "o"), (h + 0.55, 1.3), (h + 1, 1.3)]))


def skill_spear(ctx):
    """chiêu cuối giáo: lốc nước tụ lực, bật nhảy vòng cung (không lộn), giương giáo trên cao, lao xuống cắm giáo xuống đất
    trước đối thủ: cột nước phụt, vòng sóng, sóng thần; rút giáo nhảy lùi về."""
    D, h = 1.8, 1.04
    W0 = ctx.R.weapon_ang

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        mx = c([(0, 0), (0.36, -12), (0.66, 0.42 * H, "o"), (0.9, 0.78 * H), (h, 0.95 * H, "i"), (1.26, 0.93 * H),
                (1.42, 0.55 * H, "o"), (1.56, 0.25 * H, "i"), (D, 0)])
        my = c([(0, 0), (0.36, -10), (0.66, 0.5 * H, "o"), (0.9, 0.35 * H, "s"), (h, 0, "i"), (1.26, 0), (1.42, 0.14 * H, "o"),
                (1.56, 0, "i"), (D, 0)])
        P.move("move", mx, my)
        P.move("shadow", mx, -my)
        P.scale("shadow", c([(0, 1), (0.66, 0.6, "o"), (h, 1.0, "i"), (1.42, 0.85), (1.56, 1), (D, 1)]))
        P.move("hip", 0, c([(0, 0), (0.34, -16), (0.44, 4, "o"), (0.9, 0), (h, -20, "o"), (1.3, -8), (1.56, -10), (D, 0)]))
        bend(P, c([(0, 0), (0.34, 8), (0.7, -4), (h - 0.06, 6), (h, -16, "o"), (1.3, -8), (D, 0)]))
        P.rot("neck", c([(0, 0), (0.34, 4), (h, -8, "o"), (D, 0)]))
        P.rot("head", c([(0, 0), (0.34, 5), (0.7, -3), (h, -6, "o"), (D, 0)]))
        P.rot("arm_f1", c([(0, 0), (0.34, 25), (0.7, 135, "io"), (h - 0.1, 150), (h, 12, "i"), (1.3, 6), (D, 0)]))
        P.rot("arm_f2", c([(0, 0), (0.7, 20), (h, -22, "o"), (D, 0)]))
        aim(P, ctx.R, c([(0, W0), (0.34, 70), (0.7, -38), (h - 0.1, -52), (h, -78, "i"), (1.28, -74), (1.44, 30), (D, W0)]))
        P.rot("arm_b1", c([(0, 0), (0.34, -20), (0.7, 40), (h, -36, "o"), (1.3, -14), (D, 0)]))
        P.rot("arm_b2", c([(0, 0), (0.7, -30), (h, -28), (D, 0)]))
        leap_feet(P, ctx, t, mx, my, [(0, 0), (0.4, 0), (0.5, 1, "o"), (0.9, 1), (h - 0.02, 0, "i"), (1.32, 0), (1.42, 1, "o"),
                                     (1.54, 0, "i"), (D, 0)],
                  {"b": [(0, 0), (0.4, 0), (h, 0.9 * H, "io"), (1.32, 0.9 * H), (1.54, 0.3 * H), (D, 0)],
                   "f": [(0, 0), (0.4, 0), (h, 1.02 * H, "io"), (1.32, 1.02 * H), (1.54, 0.38 * H), (D, 0)]}, D)
        P.att["head"] = "head_roar" if 0.3 <= t < 1.34 else "head"
        skill_fx_charge(P, t, c)
        skill_fx_impact(P, t, c, h, at=0.42 * H)
    return {"dur": D, "fn": f, "hit": h}


def skill_sword(ctx):
    """chiêu cuối kiếm: tụ lực, lướt tới thấp người (không lộn), chém xuống rồi hất kiếm chém ngược lên, sóng lưỡi liềm
    lớn, sóng thần sau đối thủ; lùi về."""
    D, h1, h = 1.7, 0.62, 0.92
    W0 = ctx.R.weapon_ang

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        mx = c([(0, 0), (0.34, -14), (0.56, 0.7 * H, "i"), (h1, 0.78 * H, "o"), (h, 0.96 * H, "io"), (1.12, 0.94 * H),
                (1.45, 0.2 * H, "io"), (D, 0)])
        my = c([(0, 0), (0.4, 0), (0.5, 0.08 * H, "o"), (0.58, 0, "i"), (D, 0)])
        P.move("move", mx, my)
        P.move("shadow", mx, -my)
        P.move("hip", 0, c([(0, 0), (0.32, -18), (h1, -22, "o"), (h - 0.08, -10), (h, -6, "o"), (1.15, -12), (D, 0)]))
        bend(P, c([(0, 0), (0.32, 6), (h1, -14, "o"), (h - 0.08, -6), (h, 8, "o"), (1.2, 0), (D, 0)]))
        P.rot("chest", c([(0, 0), (0.32, -6), (h1, 8, "o"), (h, -6, "o"), (D, 0)]))
        P.rot("head", c([(0, 0), (0.32, 4), (h1, -6, "o"), (h, 4, "o"), (D, 0)]))
        P.rot("arm_f1", c([(0, 0), (0.32, 105, "io"), (0.52, 112), (h1, -28, "o"), (h - 0.1, -34), (h, 118, "o"), (1.2, 96), (D, 0)]))
        P.rot("arm_f2", c([(0, 0), (0.32, 18), (h1, -8, "o"), (h, 12, "o"), (D, 0)]))
        aim(P, ctx.R, c([(0, W0), (0.32, 80), (0.52, 88), (h1, -66, "o"), (h - 0.1, -70), (h, 70, "o"), (1.2, 64), (D, W0)]))
        P.rot("arm_b1", c([(0, 0), (0.32, 20), (h1, -36, "o"), (h, -40), (1.2, -16), (D, 0)]))
        P.rot("arm_b2", c([(0, 0), (0.32, -14), (h1, -26), (D, 0)]))
        lunge_feet(P, ctx, t, 0.34, h1, 0.82 * H, 0.62 * H, 1.15, D, lift=18)
        P.att["head"] = "head_roar" if 0.3 <= t < 1.2 else "head"
        skill_fx_charge(P, t, c, t_end=0.5)
        # hai vệt chém: chém xuống (h1) rồi hất ngược lên (h), vệt thứ hai lật ngược, to hơn
        if t < (h1 + h) / 2:
            fx_on(P, "fx_slash", t, h1 - 0.04, h1 + 0.22, fade=0.14)
            P.scale("fx_slash", c([(0, 0.9), (h1 - 0.04, 0.9), (h1 + 0.16, 1.3, "o"), (D, 1.3)]))
            P.rot("fx_slash", -20)
        else:
            fx_on(P, "fx_slash", t, h - 0.04, h + 0.26, fade=0.16)
            P.scale("fx_slash", c([(0, 1.0), (h - 0.04, 1.0), (h + 0.18, 1.55, "o"), (D, 1.55)]),
                    c([(0, -1.0), (h - 0.04, -1.0), (h + 0.18, -1.55, "o"), (D, -1.55)]))
            P.rot("fx_slash", 15)
        skill_fx_impact(P, t, c, h, at=0.55 * H)
    return {"dur": D, "fn": f, "hit": h}


def skill_glaive(ctx):
    """chiêu cuối đại đao: tụ lực, nhảy cao giương đao, bổ xuống đất trước đối thủ (vệt chém lớn, cột nước, sóng thần),
    rồi quét ngang một nhát dư lực; lùi về."""
    D, h = 1.9, 1.06
    W0 = ctx.R.weapon_ang

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        mx = c([(0, 0), (0.38, -14), (0.68, 0.4 * H, "o"), (0.92, 0.76 * H), (h, 0.94 * H, "i"), (1.3, 0.96 * H),
                (1.6, 0.3 * H, "io"), (D, 0)])
        my = c([(0, 0), (0.38, -12), (0.68, 0.46 * H, "o"), (0.92, 0.3 * H, "s"), (h, 0, "i"), (D, 0)])
        P.move("move", mx, my)
        P.move("shadow", mx, -my)
        P.scale("shadow", c([(0, 1), (0.68, 0.62, "o"), (h, 1.0, "i"), (D, 1)]))
        P.move("hip", 0, c([(0, 0), (0.36, -18), (0.46, 4, "o"), (0.92, 0), (h, -24, "o"), (1.36, -10), (D, 0)]))
        bend(P, c([(0, 0), (0.36, 9), (0.72, -6), (h - 0.06, 8), (h, -18, "o"), (1.3, -4), (1.42, 6, "o"), (D, 0)]))
        P.rot("head", c([(0, 0), (0.36, 5), (h, -8, "o"), (D, 0)]))
        # tay cầm ở giữa ngực: giơ lệch sang phải, đao nghiêng phải (cán không dựng trước mặt)
        P.rot("arm_f1", c([(0, 0), (0.36, 25), (0.72, 72, "io"), (h - 0.1, 80), (h, -10, "i"), (1.26, -6), (1.42, 30, "o"),
                           (1.6, 15), (D, 0)]))
        P.rot("arm_f2", c([(0, 0), (0.72, -10), (h, -16, "o"), (1.42, 0), (D, 0)]))
        aim(P, ctx.R, c([(0, W0), (0.36, 66), (0.72, 70), (h - 0.1, 74), (h, -34, "i"), (1.26, -30), (1.42, 12, "o"),
                         (1.6, 30), (D, W0)]))
        P.rot("arm_b1", c([(0, 0), (0.36, -20), (0.72, 40), (h, -36, "o"), (1.3, -14), (D, 0)]))
        P.rot("arm_b2", c([(0, 0), (0.72, -30), (h, -28), (D, 0)]))
        leap_feet(P, ctx, t, mx, my, [(0, 0), (0.42, 0), (0.52, 1, "o"), (0.92, 1), (h - 0.02, 0, "i"), (D, 0)],
                  {"b": [(0, 0), (0.42, 0), (h, 0.88 * H, "io"), (1.36, 0.88 * H), (1.62, 0.25 * H), (D, 0)],
                   "f": [(0, 0), (0.42, 0), (h, 1.0 * H, "io"), (1.36, 1.0 * H), (1.62, 0.32 * H), (D, 0)]}, D)
        P.att["head"] = "head_roar" if 0.32 <= t < 1.45 else "head"
        skill_fx_charge(P, t, c, t_end=0.68)
        fx_on(P, "fx_slash", t, h - 0.05, h + 0.28, fade=0.18)
        P.scale("fx_slash", c([(0, 1.1), (h - 0.05, 1.1), (h + 0.2, 1.8, "o"), (D, 1.8)]))
        P.rot("fx_slash", -40)
        skill_fx_impact(P, t, c, h, at=0.5 * H)
    return {"dur": D, "fn": f, "hit": h}


def clips_of(ctx):
    return {"idle": idle(ctx), "hit": hit(ctx), "attack": attack(ctx), "cast": cast(ctx), "skill": skill(ctx)}


# ---------------------------------------------------------------- tiến hóa
def evolve(ctxA, ctxB, M, idleB0, scaleB):
    """dạng A (xương thường) biến thành dạng B (xương n_): A nện vũ khí, nước dâng lốc quanh người, A tan dần trong nước,
    B hiện ra lớn dần trong cột nước, nước vỡ tung, B gầm rồi về đúng khung đầu clip đứng của B (đổi sticker không giật)."""
    D = 3.0
    slotsA = [s["name"] for s in ctxA.R.slots]
    slotsB = ["n_" + s["name"] for s in ctxB.R.slots]
    endB = {"n_" + b: v for b, v in idleB0.t.items()}

    def f(t, P):
        c = lambda ks: curve(t, ks)  # noqa: E731
        # A: thủ thế, nện vũ khí xuống đất (0,45 s), gồng người khi nước dâng
        P.move("hip", 0, c([(0, 0), (0.3, -10), (0.45, -18, "o"), (1.2, -14), (D, -14)]))
        lean = c([(0, 0), (0.3, 6), (0.45, -8, "o"), (1.1, 4), (D, 4)])
        for b, f_ in (("spine1", 0.3), ("spine2", 0.35), ("chest", 0.35)):
            P.rot(b, f_ * lean)
        P.rot("arm_f1", c([(0, 0), (0.3, 60), (0.45, 10, "o"), (1.2, 30), (D, 30)]))
        P.rot("hand_f", c([(0, 0), (0.3, 20), (0.45, -30, "o"), (D, -30)]))
        P.rot("arm_b1", c([(0, 0), (0.45, -24), (1.2, -40), (D, -40)]))
        P.rot("arm_b2", c([(0, 0), (0.45, -30), (1.2, -50), (D, -50)]))
        P.rot("head", c([(0, 0), (0.3, 4), (0.6, -10, "o"), (1.2, -14), (D, -14)]))
        plant(P, ctxA)
        P.att["head"] = "head_roar" if 0.4 <= t < 1.3 else "head"
        # đổi dạng ngắn (0,3 s) lúc lốc nước phía trước đậm nhất, đỡ cảnh hai dạng trong suốt chồng nhau
        aA = c([(0, 1), (1.05, 1), (1.35, 0, "io"), (D, 0)])
        for s_ in slotsA:
            if s_ in ctxA.R.fx_slots:
                continue
            P.alpha[s_] = aA
        # nước: vòng sóng, lốc quanh người, cột nước, vỡ tung
        P.att["fx_ground"] = "fx_ground" if 0.42 <= t < 2.4 else None
        P.alpha["fx_ground"] = c([(0, 0), (0.42, 0), (0.6, 1), (1.9, 1), (2.4, 0)])
        P.scale("fx_ground", c([(0, 0.3), (0.42, 0.3), (0.9, 1.25, "o"), (2.0, 1.35), (D, 1.35)]))
        for s_ in ("fx_ring_b", "fx_ring_f"):
            P.att[s_] = s_ if 0.55 <= t < 2.0 else None
        P.alpha["fx_ring_b"] = c([(0, 0), (0.55, 0), (0.9, 0.9), (1.65, 0.9), (1.95, 0)])
        P.alpha["fx_ring_f"] = c([(0, 0), (0.55, 0), (0.9, 0.6), (1.05, 0.88), (1.5, 0.88), (1.68, 0.5), (1.95, 0)])
        P.rot("fx_ring", c([(0, 0), (2.0, -1000, "l"), (D, -1000)]))
        P.scale("fx_ring", c([(0, 0.4), (0.55, 0.4), (1.0, 1.05, "o"), (1.6, 1.15), (1.95, 1.5, "o"), (D, 1.5)]),
                c([(0, 0.4), (0.55, 0.4), (1.0, 1.2, "o"), (1.6, 1.3), (1.95, 1.6, "o"), (D, 1.6)]))
        P.att["fx_splash"] = "fx_splash" if 1.6 <= t < 2.25 else None
        P.alpha["fx_splash"] = c([(0, 1), (1.85, 1), (2.25, 0)])
        P.scale("fx_splash", c([(0, 0.5), (1.6, 0.5), (2.0, 2.1, "o"), (D, 2.1)]))
        P.move("fx_splash", -0.72 * H + ctxA.R.bw("spine2")[0], -0.45 * H + ctxA.R.bw("spine2")[1])
        fx_on(P, "fx_drops", t, 1.7, 2.4, fade=0.35)  # giọt nước văng khi cột nước vỡ
        P.scale("fx_drops", c([(0, 0.8), (1.7, 0.8), (2.4, 2.2, "o")]))
        P.move("fx_drops", c([(0, 0), (1.7, 0), (2.4, 0.1 * H, "o")]), c([(0, 0), (1.7, 0), (2.4, 0.3 * H, "o")]))
        # B: hiện dần trong nước, lớn lên từ 0,9, gầm và vươn vũ khí, rồi về dáng đứng đầu clip idle
        aB = c([(0, 0), (1.12, 0), (1.45, 1, "io"), (D, 1)])
        for s_ in slotsB:
            if s_.replace("n_", "", 1) in ctxB.R.fx_slots:
                continue
            P.alpha[s_] = aB
        sc = scaleB * c([(0, 0.86), (1.0, 0.86), (2.0, 1.0, "o"), (D, 1.0)])
        P.scale("evo", sc)
        P.move("evo", 0, c([(0, -10), (1.0, -10), (1.9, 0, "o"), (D, 0)]))
        fl = c([(0, 0), (1.6, 0), (2.05, 1, "o"), (2.45, 1), (2.85, 0, "io"), (D, 0)])
        P.move("n_hip", 0, -10 * fl)
        P.rot("n_chest", -6 * fl)
        P.rot("n_head", 10 * fl)
        P.rot("n_arm_f1", 70 * fl)
        P.rot("n_arm_f2", 20 * fl)
        P.rot("n_hand_f", 25 * fl)
        P.rot("n_arm_b1", -30 * fl)
        P.rot("n_arm_b2", -20 * fl)
        for sd in ("b", "f"):
            x, y = ctxB.ank[sd]
            P.feet["n_" + sd] = (x, y, 0)
        P.att["n_head"] = "n_head_roar" if 1.85 <= t < 2.6 else "n_head"
        P.alpha["shadow"] = aA
        P.alpha["n_shadow"] = aB

    def post(t, P):
        w = L.smooth01((t - (D - 0.35)) / 0.35)
        if w <= 0:
            return
        for b in set(endB) | {b for b in P.t if b.startswith("n_")}:
            tb = endB.get(b, [0, 0, 0, 1, 1])
            ta = P._g(b)
            for q in range(5):
                ta[q] = ta[q] * (1 - w) + tb[q] * w
    return {"dur": D, "fn": f, "post": post}


# ---------------------------------------------------------------- xuất
def portrait(ctx, out_dir, res_dir):
    """chân dung khung 4:5 (chân cách đáy 6%), ghép mảnh tỉ lệ L1 ở dáng gốc, lưu vuông 512, không bóng."""
    parts, pimg, ground, feet_x, top = ctx.parts, ctx.pimg, ctx.ground, ctx.feet_x, ctx.top
    hh = ground - top
    fh = hh / 0.86
    fw = fh * 0.8
    W, Hh = int(round(fw)), int(round(fh))
    canvas = np.zeros((Hh, W, 4), np.float32)
    x0, y0 = feet_x - fw / 2, ground - 0.94 * fh
    for n in DRAW[ctx.k]:
        t = parts[n]
        im = pimg[n].astype(np.float32)
        ox, oy = int(round(t["x0"] - x0)), int(round(t["y0"] - y0))
        h, w = im.shape[:2]
        ax0, ay0, ax1, ay1 = max(0, ox), max(0, oy), min(W, ox + w), min(Hh, oy + h)
        if ax1 <= ax0 or ay1 <= ay0:
            continue
        sub = im[ay0 - oy:ay1 - oy, ax0 - ox:ax1 - ox]
        a = sub[:, :, 3:4] / 255.0
        dst = canvas[ay0:ay1, ax0:ax1]
        out_a = a + dst[:, :, 3:4] * (1 - a)
        dst[:, :, :3] = (sub[:, :, :3] * a + dst[:, :, :3] * dst[:, :, 3:4] * (1 - a)) / np.maximum(out_a, 1e-6)
        dst[:, :, 3:4] = out_a
    im = Image.fromarray(np.clip(np.dstack([canvas[:, :, :3], canvas[:, :, 3:4] * 255]), 0, 255).astype(np.uint8))
    im.save(os.path.join(out_dir, "chan_dung_4x5.png"))
    im.resize((512, 512), Image.LANCZOS).save(os.path.join(res_dir, code(ctx.k) + "_portrait.png"))


def game_info(R, clips, baked):
    hgt = L.idle_height(R, baked["idle"][0])
    hc = [n for n in clips if "hit" in clips[n]]
    ci = round(clips["cast"]["hit"] * L.FPS)
    tip = L.point_world(R, baked["cast"][ci], "tip")
    return {"fps": 25, "height": round(hgt, 2), "hitClips": hc, "hitTimes": [clips[n]["hit"] for n in hc], "lunge": ["skill"],
            "stay": [], "muzzle": [round(float(tip[0]), 2), round(float(tip[1]), 2)], "beam": {1: 0.8, 2: 1.0, 3: 1.25}[0] if False else 1.0,
            "beamStyle": "", "move": "move", "shadow": "shadow"}


def build_form(k, nxt=None, gif=True):
    """dựng, nướng, xuất dạng k; nxt = (ctx, R, idle0) của dạng k+1 để làm clip tiến hóa nối liền."""
    R, ctx = build_rig(k)
    R.chain_tips = {"tail": ctx.info["tail_tip"], "crest": ctx.info["crest_tip"], "cloth": ctx.info["cloth_tip"]}
    if "cape_tip" in ctx.info:
        R.chain_tips["cape"] = ctx.info["cape_tip"]
    clips = clips_of(ctx)
    cfg = springs(R)
    baked = {n: L.bake(R, c, cfg) for n, c in clips.items()}
    hgt = L.idle_height(R, baked["idle"][0])
    out_dir = os.path.join(base(k), "rig")
    res_dir = os.path.join(RES, code(k))
    Rx = R
    if nxt:
        ctxB, RB, idleB0, hB = nxt
        M = L.merge_next(R, RB)
        M.chain_tips = dict(R.chain_tips)
        M.chain_tips.update({"n_" + n: p for n, p in RB.chain_tips.items()})
        M.legs = dict(R.legs)
        M.legs.update({"n_" + sd: tuple("n_" + b for b in leg[:3]) + ("evo",) for sd, leg in RB.legs.items()})
        M.points = dict(R.points)
        M.weapon_ang = R.weapon_ang
        cfgM = dict(cfg)
        cfgM.update(springs(M, prefix="n_"))
        ev = evolve(ctx, ctxB, M, idleB0, hgt / hB)
        # các clip trận chạy trên rig gộp: dạng sau ẩn (độ đậm 0) để file chỉ một rig
        hide = {"n_" + s["name"] for s in RB.slots}
        clipsM = {}
        for n, c in clips.items():
            def fn(t, P, f0=c["fn"]):
                f0(t, P)
                for s_ in hide:
                    P.att[s_] = None
            clipsM[n] = dict(c, fn=fn)
        clipsM["evolve"] = ev
        bakedM = {n: L.bake(M, c, cfgM) for n, c in clipsM.items()}
        Rx, clips, baked = M, clipsM, bakedM
    game = game_info(Rx, clips, baked)
    game["height"] = round(hgt, 2)
    game["beam"] = {1: 0.8, 2: 1.0, 3: 1.25}[k]
    print(f"dạng {k}: {len(Rx.bones)} xương, {len(Rx.slots)} slot, cao {hgt:.0f}, trận {json.dumps(game, ensure_ascii=False)}")
    aw, ah = L.export(Rx, clips, baked, out_dir, res_dir, game, H, gif=gif)
    print(f"  atlas {aw}x{ah}, ra {out_dir}")
    portrait(ctx, out_dir, res_dir)
    import pickle  # bản nướng để soi khung lớn (lệnh show) khỏi nướng lại
    with open(os.path.join(out_dir, "baked.pkl"), "wb") as fh:
        pickle.dump((Rx, {n: c["dur"] for n, c in clips.items()}, baked), fh)
    return ctx, R, baked["idle"][0], hgt


def show(k, clip, times, fh=520, follow=False):
    """khung lớn của clip ở các thời điểm (giây) từ bản nướng, ra rig/xem_<clip>.png."""
    import pickle
    out_dir = os.path.join(base(k), "rig")
    with open(os.path.join(out_dir, "baked.pkl"), "rb") as f_:
        R, durs, baked = pickle.load(f_)
    frames = baked[clip]
    kk = fh / (1.75 * H)
    Wb = int(1.9 * H * kk)
    imgs = []
    for t in times:
        i = min(len(frames) - 1, round(t * L.FPS))
        P = frames[i]
        mx = P.t.get("move", [0, 0, 0, 1, 1])[0] if follow else 0
        box = (Wb, fh, int((0.6 * H - mx) * kk), int(fh - 0.1 * H * kk))
        im = Image.fromarray(L.render(R, P, kk, box))
        ImageDraw.Draw(im).text((6, 6), f"{clip} {t:.2f}s", fill=(43, 33, 24))
        imgs.append(np.array(im))
    p = os.path.join(out_dir, f"xem_{clip}.png")
    Image.fromarray(np.concatenate(imgs, 1)).save(p)
    print(p)


def main(argv):
    step = argv[0]
    if step == "cut":
        k = int(argv[1])
        riglib.cut(code(k))
        fix_grip(k)
        fix_stubs(k)
    elif step == "place":
        place(int(argv[1]), argv[2:] or None)
    elif step == "rig":  # dựng một dạng lẻ (không tiến hóa), soi nhanh
        build_form(int(argv[1]), gif="--gif" in argv)
    elif step == "show":  # show <k> <clip> t1,t2,... [follow]
        show(int(argv[1]), argv[2], [float(x) for x in argv[3].split(",")], follow="follow" in argv)
    elif step == "all":
        n3 = build_form(3)
        n2 = build_form(2, n3)
        build_form(1, n2)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
