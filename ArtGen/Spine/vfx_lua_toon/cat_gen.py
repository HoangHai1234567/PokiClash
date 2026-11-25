# -*- coding: utf-8 -*-
"""Cắt hình gen Magnific thành khung cho build_atom.py.

    py -3 -I cat_gen.py luoi <tờ.png> <tên_fx> [cột hàng]       # tờ GPT nền trong, lưới cố định (mặc định 4 x 6)
    py -3 -I cat_gen.py video <clip.mp4> <tên_fx> <t0> <t1> [rộng]  # video nền xanh lam phẳng, tách nền, 24 khung/giây

Ra: frames/<tên_fx>/<tên_fx>_NN.png (mọi khung cùng một hộp để điểm neo đứng yên) + mục trong frames/manifest.json.
Điểm neo = nòng lửa: chấm sáng nhất ở mép trái của các khung đầu.
"""
import json
import os
import sys

import cv2
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "frames")
FPS = 24


def save(name, frames, anchor, loop=False):
    """frames: list BGRA cùng cỡ. Cắt hộp gộp, lưu, ghi manifest."""
    al = np.max(np.stack([f[..., 3] for f in frames]), 0)
    ys, xs = np.where(al > 8)
    pad = 6
    x0, x1 = max(0, xs.min() - pad), min(al.shape[1], xs.max() + pad + 1)
    y0, y1 = max(0, ys.min() - pad), min(al.shape[0], ys.max() + pad + 1)
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):
        if f.endswith(".png"):
            os.remove(os.path.join(d, f))
    for i, f in enumerate(frames):
        cv2.imwrite(os.path.join(d, f"{name}_{i:02d}.png"), f[y0:y1, x0:x1])
    mp = os.path.join(OUT, "manifest.json")
    man = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {}
    man[name] = dict(count=len(frames), w=int(x1 - x0), h=int(y1 - y0), fps=FPS, loop=loop,
                     anchor=[int(anchor[0] - x0), int(anchor[1] - y0)])
    json.dump(man, open(mp, "w", encoding="utf-8"), indent=1)
    print(name, len(frames), "khung", x1 - x0, "x", y1 - y0, "neo", man[name]["anchor"])


def find_nozzle(frames, k=4):
    """Chấm sáng nhất (gần trắng) ở 1/5 trái, lấy trung bình vài khung đầu có lửa."""
    pts = []
    for f in frames[:12]:
        if f[..., 3].max() < 50:
            continue
        w = f.shape[1]
        sub = f[:, : w // 5].astype(np.float32)
        white = (sub[..., :3].min(2) > 215) & (sub[..., 3] > 200)  # chấm nòng trắng nóng
        if white.sum() < 4:
            continue
        ys, xs = np.where(white)
        x = xs.min() + 4  # cụm trắng nằm trái nhất
        near = np.abs(xs - x) < 10
        pts.append((x, int(np.median(ys[near]))))
        if len(pts) >= k:
            break
    if not pts:
        return (8, frames[0].shape[0] // 2)
    return tuple(np.median(np.array(pts), 0).astype(int))


def luoi(path, name, cols=4, rows=6, out_w=640):
    im = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    H, W = im.shape[:2]
    cw, ch = W / cols, H / rows
    frames = []
    for r in range(rows):
        for c in range(cols):
            cell = im[int(round(r * ch)):int(round((r + 1) * ch)), int(round(c * cw)):int(round((c + 1) * cw))]
            frames.append(cell)
    h = min(f.shape[0] for f in frames)
    w = min(f.shape[1] for f in frames)
    frames = [f[:h, :w] for f in frames]
    sc = out_w / w
    frames = [cv2.resize(f, (out_w, int(round(h * sc))), interpolation=cv2.INTER_AREA) for f in frames]
    save(name, frames, find_nozzle(frames))


def key_blue(bgr):
    """Nền xanh lam phẳng -> alpha; gỡ màu xanh lẫn ở mép (unmix theo màu nền)."""
    f = bgr.astype(np.float32)
    b, g, r = f[..., 0], f[..., 1], f[..., 2]
    blue = b - np.maximum(r, g)
    a = np.clip(1 - (blue - 30) / (150 - 30), 0, 1)
    a = cv2.GaussianBlur(a, (0, 0), 0.6)
    # màu nền = trung vị các điểm chắc chắn là nền
    m = blue > 170
    bg = np.median(f[m], 0) if m.sum() > 100 else np.array([255, 48, 0], np.float32)
    aa = np.maximum(a, 1e-3)[..., None]
    col = (f - (1 - aa) * bg) / aa
    col = np.clip(col, 0, 255)
    out = np.dstack([col, a * 255]).astype(np.uint8)
    out[a < 0.02] = 0
    return out


def edge_cut(k, t, cut=None, edge=0.06, seed=3):
    """Mờ dần sát mép khung (khói trôi ra ngoài không lộ đường cắt) và cho luồng đứt từ nòng:
    cut = (giờ bắt đầu, giờ xong, tới bao xa theo bề ngang) tính theo giờ video."""
    H, W = k.shape[:2]
    a = k[..., 3].astype(np.float32) / 255
    e = edge * min(W, H)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.minimum(np.minimum(yy, H - 1 - yy), W - 1 - xx)  # mép trên, dưới, phải (mép trái là nòng)
    a *= np.clip(d / e, 0, 1)
    if cut and t > cut[0]:
        q = min(1.0, (t - cut[0]) / (cut[1] - cut[0]))
        q = q * q * (3 - 2 * q)
        xc = q * cut[2] * W
        rng = np.random.default_rng(seed)
        ph = rng.uniform(0, 6.28, 3)
        rag = (np.sin(yy[:, :1] / H * 9 + ph[0]) * 0.5 + np.sin(yy[:, :1] / H * 23 + ph[1]) * 0.3 +
               np.sin(yy[:, :1] / H * 51 + ph[2]) * 0.2) * 0.035 * W
        w = 0.03 * W
        a *= np.clip((xx - (xc + rag) + w) / (2 * w), 0, 1)
    k[..., 3] = (a * 255).astype(np.uint8)
    return k


def video(path, name, t0, t1, out_w=640, speed=1.0, fade_tail=0, cut=None, edge=0.0):
    c = cv2.VideoCapture(path)
    vf = c.get(cv2.CAP_PROP_FPS)
    n = int(round((t1 - t0) * FPS / speed))
    frames = []
    for i in range(n):
        t = t0 + i * speed / FPS
        c.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * vf)))
        ok, fr = c.read()
        if not ok:
            break
        k = key_blue(fr)
        if cut or edge:
            k = edge_cut(k, t, cut, edge)
        sc = out_w / k.shape[1]
        frames.append(cv2.resize(k, (out_w, int(round(k.shape[0] * sc))), interpolation=cv2.INTER_AREA))
    for j in range(fade_tail):  # giọt sót cuối mờ dần
        f = frames[len(frames) - fade_tail + j]
        f[..., 3] = (f[..., 3].astype(np.float32) * (1 - (j + 1) / (fade_tail + 1))).astype(np.uint8)
    save(name, frames, find_nozzle(frames))


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "luoi":
        cols = int(sys.argv[4]) if len(sys.argv) > 4 else 4
        rows = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        luoi(sys.argv[2], sys.argv[3], cols, rows)
    elif mode == "video":
        w = int(sys.argv[6]) if len(sys.argv) > 6 else 640
        sp = float(sys.argv[7]) if len(sys.argv) > 7 else 1.0
        ft = int(sys.argv[8]) if len(sys.argv) > 8 else 0
        cut = tuple(float(v) for v in sys.argv[9].split(",")) if len(sys.argv) > 9 else None
        edge = float(sys.argv[10]) if len(sys.argv) > 10 else 0.0
        video(sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5]), w, sp, ft, cut, edge)
