# -*- coding: utf-8 -*-
"""Phun lửa: đoạn phun lấy từ video gen, cuối đòn cả khối lửa vỡ thành mảnh tàn (như clip firebreath giây 19.3–19.8).

Mảnh = cắt chính khung lửa cuối bằng ô Voronoi kéo dài theo ngang, mép xé bằng nhiễu, có khe nứt.
Mỗi mảnh bung ra, xoay, rơi theo trọng lực, nhỏ dần, tối dần sang đỏ sẫm (phần sáng giữ cam lâu hơn), mờ ở cuối.
Thêm vài đốm than. Không khói.

    py -3 -I vo_manh.py <video.mp4> <tên_fx> <giờ_video_hết_phun> [tốc_độ=2] [số_khung_vỡ=14] [rộng=720]
"""
import math
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cat_gen as cg  # noqa: E402
import gen_khung as gk

FPS = 24
MAROON = np.array([40, 22, 92], np.float32)  # BGR đỏ sẫm #5C1628
ORANGE = [np.array(c, np.float32) for c in ((70, 190, 255), (40, 130, 255), (30, 75, 226))]  # BGR vàng cam, cam, đỏ cam
EMBER = [(80, 190, 255), (60, 140, 255), (150, 230, 255)]  # BGR cam vàng


def breath_frames(path, t_end, speed, out_w):
    c = cv2.VideoCapture(path)
    vf = c.get(cv2.CAP_PROP_FPS)
    n = int(round(t_end * FPS / speed)) + 1
    out = []
    for i in range(n):
        t = i * speed / FPS
        c.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * vf)))
        ok, fr = c.read()
        if not ok:
            break
        k = cg.key_blue(fr)
        k = cg.edge_cut(k, t, None, 0.04)
        sc = out_w / k.shape[1]
        out.append(cv2.resize(k, (out_w, int(round(k.shape[0] * sc))), interpolation=cv2.INTER_AREA))
    return out


def shards_of(img, n_seeds=42, seed=5):
    """Nhãn mảnh cho từng điểm ảnh (-1 = không có / khe nứt)."""
    H, W = img.shape[:2]
    a = img[..., 3].astype(np.float32) / 255
    mask = a > 0.25
    ys, xs = np.where(mask)
    rng = np.random.default_rng(seed)
    pick = rng.choice(len(xs), size=min(n_seeds, len(xs)), replace=False)
    sx, sy = xs[pick].astype(np.float32), ys[pick].astype(np.float32)
    Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
    # mép xé: lệch toạ độ bằng nhiễu trước khi chia ô
    wx = X + 9 * gk.fbm(gk.PN, X / 38, Y / 38, 3)
    wy = Y + 9 * gk.fbm(gk.PN, X / 38 + 40, Y / 38 + 11, 3)
    best = np.full((H, W), 1e18, np.float32)
    lab = np.full((H, W), -1, np.int32)
    for i in range(len(sx)):
        d = ((wx - sx[i]) * 0.42) ** 2 + (wy - sy[i]) ** 2  # ô kéo dài theo ngang (lửa phun ngang)
        m = d < best
        best[m] = d[m]
        lab[m] = i
    lab[~mask] = -1
    # khe nứt giữa các mảnh
    edge = np.zeros((H, W), bool)
    edge[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    edge[1:, :] |= lab[1:, :] != lab[:-1, :]
    edge = cv2.dilate(edge.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    lab[edge] = -1
    return lab, len(sx)


def shatter(last, n_frames, seed=5):
    H, W = last.shape[:2]
    lab, n = shards_of(last, seed=seed)
    rng = np.random.default_rng(seed + 1)
    a_all = last[..., 3] > 60
    ys, xs = np.where(a_all)
    cx, cy = xs.mean(), ys.mean()
    shards = []
    for i in range(n):
        m = lab == i
        if m.sum() < 25:
            continue
        yy, xx = np.where(m)
        x0, x1, y0, y1 = xx.min(), xx.max() + 1, yy.min(), yy.max() + 1
        patch = last[y0:y1, x0:x1].copy()
        patch[..., 3] = np.where(m[y0:y1, x0:x1], patch[..., 3], 0)
        px, py = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = px - cx, py - cy
        L = math.hypot(dx, dy) + 1e-3
        sp = rng.uniform(60, 190)
        vx = dx / L * sp + rng.uniform(10, 80)            # bung ra + trôi theo hướng phun
        vy = dy / L * sp * 0.6 - rng.uniform(40, 150)     # hất lên rồi rơi
        lum = patch[..., :3].astype(np.float32).mean(2)
        # màu cam phẳng theo độ sáng gốc (như mảnh cam trong clip), giữ nguyên alpha
        org = np.zeros(patch.shape[:2] + (3,), np.float32)
        org[:] = ORANGE[2]
        org[lum > 120] = ORANGE[1]
        org[lum > 190] = ORANGE[0]
        shards.append(dict(p=patch, x=px, y=py, vx=vx, vy=vy, rot=rng.uniform(-300, 300),
                           tc=rng.uniform(0.12, 0.7), quick=rng.random() < 0.25,
                           life=rng.uniform(0.75, 1.0), org=org))
    embers = [dict(x=rng.uniform(xs.min(), xs.max()), y=rng.uniform(ys.min(), ys.max()),
                   vx=rng.uniform(-60, 160), vy=rng.uniform(-200, -40), r=rng.uniform(1.6, 3.2),
                   c=EMBER[k % 3], life=rng.uniform(0.5, 1.0)) for k in range(16)]
    T = n_frames / FPS
    G = 700.0
    frames = []
    for f in range(n_frames):
        t = (f + 1) / FPS
        q = t / T
        acc = np.zeros((H, W, 4), np.float32)  # tiền nhân alpha
        for s in shards:
            qa = q / s["life"]
            if qa >= 1:
                continue
            fade = 1 - cg_ss(0.82, 1.0, qa)
            sc = 1 - 0.78 * qa ** 1.3
            if s["quick"]:  # mảnh nhỏ cháy hết sớm: co lại chứ không mờ thành vệt nâu
                sc *= 1 - cg_ss(0.12, 0.5, qa)
            if fade <= 0.01 or sc < 0.06:
                continue
            p = s["p"].astype(np.float32)
            k1 = min(1.0, q / 0.16)                      # 3-4 khung đầu: màu lửa -> cam phẳng
            col = p[..., :3] * (1 - k1) + s["org"] * k1
            k2 = cg_ss(s["tc"], s["tc"] + 0.1, qa)       # rồi cháy thành đỏ sẫm, mỗi mảnh một giờ
            col = col * (1 - k2) + MAROON * k2
            al = p[..., 3:4] / 255 * fade
            ph, pw = p.shape[:2]
            nx = s["x"] + s["vx"] * t
            ny = s["y"] + s["vy"] * t + 0.5 * G * t * t
            M = cv2.getRotationMatrix2D((pw / 2, ph / 2), s["rot"] * t, sc)
            M[0, 2] += nx - pw / 2
            M[1, 2] += ny - ph / 2
            pre = np.dstack([col * al, al])
            acc_s = cv2.warpAffine(pre, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
            acc = acc * (1 - acc_s[..., 3:4]) + acc_s
        for e in embers:
            qe = q / e["life"]
            if qe >= 1:
                continue
            x = e["x"] + e["vx"] * t
            y = e["y"] + e["vy"] * t + 0.25 * G * t * t
            al = 1 - cg_ss(0.6, 1.0, qe)
            r = e["r"] * (1 - 0.5 * qe)
            m = np.zeros((H, W), np.uint8)
            cv2.circle(m, (int(x * 4), int(y * 4)), max(1, int(r * 4)), 255, -1, cv2.LINE_AA, 2)
            mm = m.astype(np.float32)[..., None] / 255 * al
            acc = acc * (1 - mm) + np.dstack([np.array(e["c"], np.float32) * mm, mm])
        a = acc[..., 3:4]
        col = np.where(a > 1e-4, acc[..., :3] / np.maximum(a, 1e-4), 0)
        frames.append(np.clip(np.dstack([col, a * 255]) + 0.5, 0, 255).astype(np.uint8))
    return frames


def cg_ss(a, b, x):
    t = min(max((x - a) / (b - a), 0.0), 1.0)
    return t * t * (3 - 2 * t)


if __name__ == "__main__":
    path, name, t_end = sys.argv[1], sys.argv[2], float(sys.argv[3])
    speed = float(sys.argv[4]) if len(sys.argv) > 4 else 2.0
    nf = int(sys.argv[5]) if len(sys.argv) > 5 else 14
    out_w = int(sys.argv[6]) if len(sys.argv) > 6 else 720
    br = breath_frames(path, t_end, speed, out_w)
    sh = shatter(br[-1], nf)
    cg.save(name, br + sh, cg.find_nozzle(br))
