# Vẽ bộ mảnh tháo rời (exploded view) của khung đứng đầu một tướng aola, làm ảnh ví dụ cho GPT.
# Mảnh nằm gọn trong mảnh lớn hơn (mắt, miệng, hoa văn) đi theo mảnh đó; mảnh gốc đẩy ra xa tâm con theo hệ số K.
import json
import os
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "E:/ProjectAtomik/aola/tools")
import portrait_png as pp  # noqa: E402

R = "E:/ProjectAtomik/aola/reskin/"


def load(name):
    rdir = R + name
    a = json.load(open(rdir + "/export/anim.json", encoding="utf-8"))
    fr = a["clips"]["1_1"]["frames"][0]
    pics = []
    for row in fr:
        p = os.path.normpath(os.path.join(rdir, a["sprites"][int(row[0])]))
        im = Image.open(p).convert("RGBA")
        pics.append((im, [float(v) for v in row[1:7]], float(row[7]), row[8] if len(row) > 8 else None))
    return pics


def bbox(im, m):
    pts = pp.corners(m, im.width, im.height)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def area(b):
    return max(0, b[2] - b[0]) * max(0, b[3] - b[1])


def inside(a, b, tol=0.85):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    return area(a) > 0 and ix * iy / area(a) >= tol


def explode(name, k, out, W=1536, H=1024, drop_first=True):
    pics = load(name)
    if drop_first and pp.is_shadow(pics[0][0]):
        pics = pics[1:]
    boxes = [bbox(im, m) for im, m, _, _ in pics]
    n = len(pics)
    # mặt nạ từng mảnh trong toạ độ khung (thu nhỏ) để xét mảnh nằm gọn trên mảnh khác
    allb0 = [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]
    ms = 300 / max(allb0[2] - allb0[0], allb0[3] - allb0[1])
    MW, MH = int((allb0[2] - allb0[0]) * ms) + 2, int((allb0[3] - allb0[1]) * ms) + 2
    masks = []
    for im, m, _, _ in pics:
        cm = [m[0] * ms, m[1] * ms, m[2] * ms, m[3] * ms, (m[4] - allb0[0]) * ms, (m[5] - allb0[1]) * ms]
        inv = pp.inverse(cm)
        a_ = np.asarray(im.split()[3].transform((MW, MH), Image.AFFINE, inv, resample=Image.BILINEAR)) > 40 if inv else np.zeros((MH, MW), bool)
        masks.append(a_)
    cnt = [mk.sum() for mk in masks]
    parent = list(range(n))
    for i in range(n):
        if cnt[i] == 0:
            continue
        best = None
        for j in range(n):
            if j == i or cnt[j] < cnt[i] * 2.5:
                continue
            if (masks[i] & masks[j]).sum() / cnt[i] >= 0.85 and (best is None or cnt[j] < cnt[best]):
                best = j
        if best is not None:
            parent[i] = best

    def root(i):
        seen = 0
        while parent[i] != i and seen < 20:
            i = parent[i]
            seen += 1
        return i
    roots = [root(i) for i in range(n)]
    allb = [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]
    cx, cy = (allb[0] + allb[2]) / 2, (allb[1] + allb[3]) / 2
    off = {}
    gap = 0.07 * max(allb[2] - allb[0], allb[3] - allb[1])
    for r in set(roots):
        b = boxes[r]
        bx, by = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
        dx, dy = bx - cx, by - cy
        d = max(1e-3, (dx * dx + dy * dy) ** 0.5)
        off[r] = (dx * k + dx / d * gap, dy * k + dy / d * gap)
    # khung sau khi đẩy
    nb = []
    for i, b in enumerate(boxes):
        dx, dy = off[roots[i]]
        nb.append((b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy))
    X0, Y0 = min(b[0] for b in nb), min(b[1] for b in nb)
    X1, Y1 = max(b[2] for b in nb), max(b[3] for b in nb)
    s = min((W * 0.9) / (X1 - X0), (H * 0.9) / (Y1 - Y0))
    ox, oy = W / 2 - (X0 + X1) / 2 * s, H / 2 - (Y0 + Y1) / 2 * s
    canvas = np.ones((H, W, 3), np.float32)
    for i, (im, m, alpha, fx) in enumerate(pics):
        dx, dy = off[roots[i]]
        cm = [m[0] * s, m[1] * s, m[2] * s, m[3] * s, (m[4] + dx) * s + ox, (m[5] + dy) * s + oy]
        inv = pp.inverse(cm)
        if inv is None:
            continue
        layer = np.asarray(im.transform((W, H), Image.AFFINE, inv, resample=Image.BICUBIC), np.float32) / 255
        rgb, a = layer[:, :, :3], layer[:, :, 3:] * alpha
        if isinstance(fx, dict) and fx.get("tint") and len(fx["tint"]) >= 6:
            t = fx["tint"]
            rgb = np.clip(rgb * np.array(t[:3], np.float32) + np.array(t[3:6], np.float32) / 255, 0, 1)
        canvas = rgb * a + canvas * (1 - a)
    Image.fromarray((np.clip(canvas, 0, 1) * 255 + 0.5).astype(np.uint8)).save(out)
    print(name, n, "mảnh,", len(set(roots)), "khối tách")


if __name__ == "__main__":
    k = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
    explode(sys.argv[1], k, sys.argv[3] if len(sys.argv) > 3 else f"ex_{sys.argv[1]}.png")
