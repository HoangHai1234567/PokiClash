# Nhập bộ mảnh môi trường Nhà (GD_Claude/22_Critters_Home.md mốc A5) và tính chỗ đặt trên bản đồ.
# - Cắt kit_vach_1.png (4 mảnh vách) và kit_bien_1.png (6 đồ ven biển), làm sạch alpha (quầng mờ GPT để lại), cắt sát hình.
# - Vách: đo lại trên ảnh (không tin khung): mặt vách = điểm cam đậm; mép cắt trái, phải; chân vách khớp đường dốc 0,5 → điểm neo
#   là chân vách ở đầu hở (mảnh 1, 2, 3: đầu trái; mảnh 4: đầu phải), dài đoạn vách (px ngang).
# - Chỗ đặt (px bản đồ, gốc trên trái, y xuống; cùng phép tính HomeSceneMenu: s = grid * 96 / diamondW):
#   vách cạnh trên phải (gy = 0) và trên trái (gx = 0, bản lật ngang) ở các ô rừng không phải đồi (balance.json home.lots kind "hill");
#   hai đầu nối thẳng vào khối đồi vẽ sẵn; mũi trái (gy = grid) dùng mảnh 3 lật ngang (vách đổ xuống đá, bụi).
#   Đồ ven biển rải trên dải cát ngoài hai cạnh dưới, chỉ chỗ ảnh nền là cát, tránh bến (mũi dưới) và cửa suối.
# Ra: Assets/03 Art/Home/home_k_vach_<1..4>.png, home_k_bien_<1..6>.png, Assets/03 Art/Home/home_kit.json; soi: kit/preview_kit.png.
# Chạy: py -3 -I ArtGen/Home/kit/import_kit.py
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ART = os.path.join(ROOT, "Assets", "03 Art", "Home")
CW, CH = 96.0, 48.0
GEOM = json.load(open(os.path.join(HERE, "refs", "kit_geom.json")))
H = GEOM["H"]
PROP_SCALE = {1: 0.52, 2: 0.5, 3: 0.42, 4: 0.55, 5: 0.5, 6: 0.5}   # dải cát hẹp (khoảng 100 px bản đồ)
OVERLAP = 24  # px ngang hai đoạn vách chồng nhau để giấu mối nối
CUT = 7       # px xoá ở đầu hở: GPT viền mực cả mép cắt, để lại thì mỗi mối nối hiện một nét dọc
# nhuộm mặt vách cho khớp vách khối đồi vẽ sẵn trên ảnh nền (đo: đồi trung vị 225,137,70; vách gen 251,156,93)
FACE_TINT = np.array([225 / 251, 137 / 156, 70 / 93])


def tint_face(a):
    a = a.copy()
    R, G, B = [a[..., i].astype(int) for i in range(3)]
    orange = (a[..., 3] > 0) & (R > G) & (G > B) & (R - B > 60) & (G > 60)
    rgb = a[..., :3].astype(float)
    rgb[orange] *= FACE_TINT
    a[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return a


def cut_open(a, xl, xr, left, right):
    a = a.copy()
    if left:
        a[:, :int(round(xl + CUT)), 3] = 0
    if right:
        a[:, int(round(xr - CUT)):, 3] = 0
    return a


def clean(a):
    a = a.copy()
    al = a[..., 3].astype(int)
    al[al < 64] = 0
    al[al >= 200] = 255
    a[..., 3] = al.astype(np.uint8)
    a[al == 0, :3] = 0
    return a


def trim(a):
    ys, xs = np.where(a[..., 3] > 0)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    return a[y0:y1, x0:x1], (x0, y0)


def face_mask(a):
    R, G, B, A = [a[..., i].astype(int) for i in range(4)]
    return (A > 200) & (R > 200) & (G > 95) & (G < 190) & (B < 140) & (R - B > 90)


def measure_wall(a, open_side):
    m = face_mask(a)
    ys, xs = np.where(m)
    xl, xr = np.percentile(xs, 0.3), np.percentile(xs, 99.7)
    cols = np.arange(int(xl) + 4, int(xr) - 4)
    bottoms = []
    for x in cols:
        yy = np.where(m[:, x])[0]
        if len(yy):
            bottoms.append(yy.max() - 0.5 * x)
    b = float(np.median(bottoms))
    ax = xl if open_side == "left" else xr
    return dict(anchor=(float(ax), float(0.5 * ax + b)), length=float(xr - xl))


def base_info():
    meta = json.load(open(os.path.join(ART, "home_art.json"), encoding="utf-8"))["home_base"]
    s = meta["grid"] * CW / meta["diamondW"]
    top = (meta["top"][0] * s, meta["top"][1] * s)
    return meta, s, top


def cell_top(top, gx, gy):
    return (top[0] + (gx - gy) * CW / 2, top[1] + (gx + gy) * CH / 2)


def main():
    meta, s, top = base_info()
    grid = meta["grid"]
    bal = json.load(open(os.path.join(ROOT, "Assets", "02 Data", "Json", "balance.json"), encoding="utf-8"))["home"]
    L = bal["lot"]
    hills = {(l["i"], l["j"]) for l in bal["lots"] if l.get("kind") == "hill"}
    out = {"H": H, "pieces": {}, "vach": [], "cat": []}

    # --- vách ---
    sheet = clean(np.asarray(Image.open(os.path.join(HERE, "kit_vach_1.png")).convert("RGBA")))
    walls = {}
    for k in range(4):
        cx, cy = (k % 2) * 768, (k // 2) * 512
        crop, off = trim(sheet[cy:cy + 512, cx:cx + 768])
        mw = measure_wall(crop, "right" if k == 3 else "left")
        mm = measure_wall(crop, "right")  # mép phải của mặt vách
        xl, xr = mw["anchor"][0] if k != 3 else mm["anchor"][0] - mm["length"], mm["anchor"][0]
        crop = cut_open(tint_face(crop), xl, xr, left=(k != 3), right=(k in (0, 1, 3)))
        name = "home_k_vach_%d" % (k + 1)
        Image.fromarray(crop).save(os.path.join(ART, name + ".png"))
        h, w = crop.shape[:2]
        ax, ay = mw["anchor"]
        walls[k + 1] = dict(name=name, w=w, h=h, ax=ax, ay=ay, length=mw["length"])
        out["pieces"][name] = {"pivot": [ax / w, 1 - ay / h], "w": w, "h": h}
        print(name, "cỡ", w, "x", h, "neo", round(ax, 1), round(ay, 1), "dài", round(mw["length"], 1), "px")

    def run(edge, a_cells, b_cells, cap_end):
        """Đặt vách dọc cạnh: edge 'R' = cạnh trên phải (gy = 0, '\\'), 'L' = cạnh trên trái (gx = 0, '/', lật). Từ ô a tới b."""
        segs = [walls[1], walls[2]]
        cap = walls[3] if cap_end else None
        a_cells -= CUT / (CW / 2)  # đầu hở bị xoá CUT px: lùi ra cho khít khối đồi
        end = b_cells - (cap["length"] / (CW / 2) if cap else -CUT / (CW / 2))
        span = end - a_cells
        seg_c = min(sg["length"] for sg in segs) / (CW / 2)
        n = max(1, math.ceil((span - seg_c) / (seg_c - OVERLAP / (CW / 2))) + 1) if span > seg_c else 1
        step = (span - seg_c) / (n - 1) if n > 1 else 0
        places = []
        for i in range(n):
            st = a_cells + i * step
            places.append((segs[i % 2], st))
        if cap:
            places.append((cap, end - OVERLAP / (CW / 2) / 2))
        for pc, st in places:
            p = cell_top(top, st, 0) if edge == "R" else cell_top(top, 0, st)
            out["vach"].append({"id": pc["name"], "x": round(p[0], 1), "y": round(p[1], 1), "flip": edge == "L"})

    # các đoạn liền nhau không phải ô đồi trên mỗi cạnh
    def free_runs(side):
        runs, cur = [], None
        for t in range(grid // L):
            lot = (t, 0) if side == "R" else (0, t)
            if lot in hills:
                if cur: runs.append(cur); cur = None
            else:
                cur = [t * L, (t + 1) * L] if not cur else [cur[0], (t + 1) * L]
        if cur: runs.append(cur)
        return runs

    for side in ("R", "L"):
        for a, b in free_runs(side):
            run(side, a, b, cap_end=(side == "L" and b == grid))
    out["vach"].sort(key=lambda e: e["y"])  # xa trước gần sau

    # --- đồ ven biển ---
    sheet = clean(np.asarray(Image.open(os.path.join(HERE, "kit_bien_1.png")).convert("RGBA")))
    props = {}
    for k in range(6):
        cx, cy = (k % 3) * 512, (k // 3) * 512
        crop, off = trim(sheet[cy:cy + 512, cx:cx + 512])
        name = "home_k_bien_%d" % (k + 1)
        Image.fromarray(crop).save(os.path.join(ART, name + ".png"))
        h, w = crop.shape[:2]
        flat = k + 1 in (3, 5)  # đồ nằm dẹt: điểm đặt ở giữa hình
        ay = h * (0.55 if flat else 0.9)
        props[k + 1] = dict(name=name, w=w, h=h)
        out["pieces"][name] = {"pivot": [0.5, 1 - ay / h], "w": w, "h": h}

    base = np.asarray(Image.open(os.path.join(ART, "home_base.png")).convert("RGB")).astype(int)
    BH, BW = base.shape[:2]

    def sandy(mx, my):
        bx, by = int(mx / s), int(my / s)
        if not (4 <= bx < BW - 4 and 4 <= by < BH - 4):
            return False
        patch = base[by - 3:by + 4, bx - 3:bx + 4].reshape(-1, 3)
        R, G, B = patch[:, 0], patch[:, 1], patch[:, 2]
        return float(((R > 225) & (G > 195) & (B < 190) & (R >= G)).mean()) > 0.7

    rnd = random.Random(20261120)
    mix = [1, 2, 3, 6, 2, 5, 6, 3, 1, 6, 2, 4, 6, 3, 5, 2, 6, 1, 3, 6, 4, 2, 6, 5]
    mi = 0
    stream_x = [f["gx"] for f in bal["features"] if f["kind"] == "stream"]
    for edge in ("LB", "BR"):
        t = 2.0
        while t < grid - 2:
            t += rnd.uniform(2.2, 4.2)
            if t > grid - 7:  # bến tàu ở mũi dưới
                break
            if edge == "LB" and any(abs(t - sx) < 4 for sx in stream_x):
                continue
            k = rnd.uniform(0.9, 1.35)
            gx, gy = (t, grid + k) if edge == "LB" else (grid + k, t)
            p = cell_top(top, gx, gy)
            if not sandy(*p):
                continue
            pid = mix[mi % len(mix)]
            mi += 1
            out["cat"].append({"id": props[pid]["name"], "x": round(p[0], 1), "y": round(p[1], 1), "flip": rnd.random() < 0.5,
                               "scale": round(PROP_SCALE[pid] * rnd.uniform(0.9, 1.1), 3)})
    out["cat"].sort(key=lambda e: e["y"])
    json.dump(out, open(os.path.join(ART, "home_kit.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("vách", len(out["vach"]), "mảnh; đồ ven biển", len(out["cat"]), "món")
    preview(out, s)


def preview(out, s):
    """Ghép thử lên ảnh nền phóng cỡ bản đồ (thu 0,5) để soi chỗ đặt."""
    base = Image.open(os.path.join(ART, "home_base.png")).convert("RGBA")
    k = 0.5
    W, Hh = int(base.width * s * k), int(base.height * s * k)
    can = base.resize((W, Hh), Image.LANCZOS)
    cache = {}
    for layer in ("cat", "vach"):
        for e in out[layer]:
            pc = out["pieces"][e["id"]]
            if e["id"] not in cache:
                cache[e["id"]] = Image.open(os.path.join(ART, e["id"] + ".png")).convert("RGBA")
            im = cache[e["id"]]
            sc = e.get("scale", 1.0) * k
            w, h = max(1, int(im.width * sc)), max(1, int(im.height * sc))
            im2 = im.resize((w, h), Image.LANCZOS)
            px, py = pc["pivot"][0], pc["pivot"][1]
            if e["flip"]:
                im2 = im2.transpose(Image.FLIP_LEFT_RIGHT)
                px = 1 - px
            x = int(e["x"] * k - px * w)
            y = int(e["y"] * k - (1 - py) * h)
            can.alpha_composite(im2, (x, y)) if x >= 0 and y >= 0 else can.paste(im2, (x, y), im2)
    can.convert("RGB").save(os.path.join(HERE, "preview_kit.png"))
    print("soi", os.path.join(HERE, "preview_kit.png"))


if __name__ == "__main__":
    main()
