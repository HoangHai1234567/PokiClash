# -*- coding: utf-8 -*-
"""Rig Spine 4.2 bằng MỘT lưới có trọng số cho cả con (không cắt mảnh): khớp uốn mềm, không hở.

    <python venv repo>/python -I ArtGen/Spine/mesh.py snorlax

Lưới: điểm dọc đường viền (thứ tự = hull) + lưới điểm bên trong, tam giác Delaunay, bỏ tam giác ra ngoài hình.
Trọng số: bản đồ vùng (đa giác ghi trong MESH) -> mỗi xương w = exp(-(khoảng cách tới vùng / sigma)^2), giữ 4 xương
nặng nhất, chuẩn hoá. Thứ tự vẽ tam giác theo lớp của vùng (tay vẽ sau cùng để đè lên bụng).
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rig  # noqa: E402

sn = rig.SPEC["snorlax"]["one"]
MESH = {
    "snorlax": {
        "src": rig.SPEC["snorlax"]["src"],
        "out": os.path.join(rig.SPEC["snorlax"]["base"], "rig_mesh"),
        "fg": (232, 20),
        "dark_thr": 120,
        "root": (258, 362),
        # (xương, cha, khớp theo toạ độ ảnh)
        "bones": [
            ("body", "root", (258, 336)),
            ("belly", "body", (256, 318)),
            ("head", "body", (258, 128)),
            ("ear_l", "head", (200, 50)),
            ("ear_r", "head", (314, 48)),
            ("arm_l", "body", (182, 158)),
            ("hand_l", "arm_l", (116, 152)),
            ("arm_r", "body", (334, 158)),
            ("hand_r", "arm_r", (400, 152)),
            ("foot_l", "root", (178, 348)),
            ("foot_r", "root", (340, 348)),
        ],
        # vùng của từng xương, theo thứ tự ưu tiên (vùng trước giành pixel trước)
        "labels": [
            ("ear_l", [(182, 12), (218, 12), (214, 42), (186, 50)], None),
            ("ear_r", [(290, 12), (342, 12), (334, 56), (300, 40)], None),
            ("head", sn["head"]["poly"], None),
            ("hand_l", [(20, 80), (112, 80), (112, 230), (20, 230)], None),
            ("hand_r", [(404, 80), (500, 80), (500, 230), (404, 230)], None),
            ("arm_l", sn["arm_l"]["poly"], None),
            ("arm_r", sn["arm_r"]["poly"], None),
            ("foot_l", [(118, 330), (234, 330), (234, 372), (118, 372)], "light"),
            ("foot_r", [(283, 330), (402, 330), (402, 372), (283, 372)], "light"),
            ("belly", [(150, 140), (366, 140), (366, 312), (150, 312)], "light"),
            ("body", [(0, 0), (520, 0), (520, 390), (0, 390)], None),
        ],
        "sigma": {"default": 13, "belly": 22, "head": 10},
        "layer": {"ear_l": 0, "ear_r": 0, "foot_l": 1, "foot_r": 1, "body": 2, "belly": 3, "head": 4,
                  "arm_l": 5, "hand_l": 5, "arm_r": 5, "hand_r": 5},
        "step_edge": 7,
        "step_in": 13,
    },
}


def build_mesh(m):
    rgb = np.array(Image.open(m["src"]).convert("RGB"))
    H, W = rgb.shape[:2]
    fg = rig.fg_mask(rgb, *m["fg"])
    fg = cv2.erode(fg, np.ones((3, 3), np.uint8)).astype(np.float32)
    fg = (cv2.GaussianBlur(fg, (0, 0), 1.6) > 0.5).astype(np.uint8)
    fg = rig.biggest(fg > 0, 500).astype(np.uint8)
    cs, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)[:, 0, :].astype(np.float64)
    # điểm viền cách đều theo chiều dài
    seg = np.sqrt(((np.roll(c, -1, 0) - c) ** 2).sum(1))
    cum = np.concatenate([[0], np.cumsum(seg)])
    L = cum[-1]
    n = int(L / m["step_edge"])
    hull = []
    for t in np.linspace(0, L, n, endpoint=False):
        i = np.searchsorted(cum, t, side="right") - 1
        f = (t - cum[i]) / max(seg[i], 1e-6)
        hull.append(c[i] * (1 - f) + c[(i + 1) % len(c)] * f)
    hull = np.array(hull)
    # điểm trong: lưới lệch hàng, cách viền >= nửa bước
    dist = cv2.distanceTransform(fg, cv2.DIST_L2, 5)
    s = m["step_in"]
    inner = []
    for j, y in enumerate(np.arange(s / 2, H, s * 0.87)):
        for x in np.arange(s / 2 + (s / 2 if j % 2 else 0), W, s):
            if dist[int(y), int(x)] > s * 0.55:
                inner.append((x, y))
    pts = np.concatenate([hull, np.array(inner)], 0)
    pts = np.round(pts * 4) / 4  # số đúng trên float32 để tra lại chỉ số từ Subdiv2D
    _, uniq = np.unique(pts, axis=0, return_index=True)
    keepi = np.sort(uniq)
    nh = int((keepi < len(hull)).sum())
    pts = pts[keepi]
    sub = cv2.Subdiv2D((-10, -10, W + 20, H + 20))
    for p in pts:
        sub.insert((float(p[0]), float(p[1])))
    key = {(round(p[0], 2), round(p[1], 2)): i for i, p in enumerate(pts)}
    inside = cv2.dilate(fg, np.ones((3, 3), np.uint8))

    def ins(p):
        x, y = int(round(p[0])), int(round(p[1]))
        return 0 <= x < W and 0 <= y < H and inside[y, x] > 0

    tris = []
    for t in sub.getTriangleList():
        ps = [(round(t[0], 2), round(t[1], 2)), (round(t[2], 2), round(t[3], 2)), (round(t[4], 2), round(t[5], 2))]
        if not all(p in key for p in ps):
            continue
        idx = [key[p] for p in ps]
        a, b, cc = pts[idx[0]], pts[idx[1]], pts[idx[2]]
        probes = [(a + b + cc) / 3, (a + b) / 2, (b + cc) / 2, (cc + a) / 2]
        if all(ins(p) for p in probes):
            tris.append(idx)
    return rgb, fg, pts, nh, np.array(tris, dtype=np.int64)


def label_map(m, rgb, fg):
    H, W = fg.shape
    dark = rgb.mean(2) < m["dark_thr"]
    cls = {"dark": dark, "light": ~dark}
    lab = np.full((H, W), -1, np.int32)
    names = [b for b, _, _ in m["labels"]]
    for i, (b, poly, keep) in enumerate(m["labels"]):
        r = rig.poly_mask(rgb.shape, poly) & (fg > 0) & (lab < 0)
        if keep:
            r &= cls[keep]
        lab[r] = i
    return names, lab


def weights(m, names, lab, pts):
    sig = m["sigma"]
    W_ = np.zeros((len(pts), len(names)))
    for i, b in enumerate(names):
        region = (lab == i).astype(np.uint8)
        d = cv2.distanceTransform(1 - region, cv2.DIST_L2, 5)
        s = sig.get(b, sig["default"])
        xs = np.clip(pts[:, 0].round().astype(int), 0, lab.shape[1] - 1)
        ys = np.clip(pts[:, 1].round().astype(int), 0, lab.shape[0] - 1)
        W_[:, i] = np.exp(-(d[ys, xs] / s) ** 2)
    # 4 xương nặng nhất, bỏ < 2%
    for v in range(len(pts)):
        row = W_[v]
        keep = np.argsort(-row)[:4]
        mask = np.zeros_like(row, bool)
        mask[keep] = True
        row[~mask] = 0
        row[row < 0.02 * row.max()] = 0
        W_[v] = row / row.sum()
    return W_


def main(code):
    m = MESH[code]
    out = m["out"]
    os.makedirs(out, exist_ok=True)
    rgb, fg, pts, nhull, tris = build_mesh(m)
    names, lab = label_map(m, rgb, fg)
    Wt = weights(m, names, lab, pts)
    H, W = fg.shape
    rx, ry = m["root"]
    world = {"root": (rx, ry)}
    for b, parent, j in m["bones"]:
        world[b] = j

    def sxy(p):
        return p[0] - rx, ry - p[1]

    bones = [{"name": "root"}]
    for b, parent, j in m["bones"]:
        bx, by = sxy(j)
        px, py = sxy(world[parent])
        bones.append({"name": b, "parent": parent, "x": round(bx - px, 2), "y": round(by - py, 2), "length": 18})
    bidx = {b["name"]: i for i, b in enumerate(bones)}
    # tam giác: sắp theo lớp của vùng ở trọng tâm (tay vẽ sau cùng)
    cen = pts[tris].mean(1)
    cl = lab[np.clip(cen[:, 1].astype(int), 0, H - 1), np.clip(cen[:, 0].astype(int), 0, W - 1)]
    layer = np.array([m["layer"].get(names[c], 2) if c >= 0 else 2 for c in cl])
    tris = tris[np.argsort(layer, kind="stable")]
    # đỉnh có trọng số: [số xương, (chỉ số xương, x, y theo xương, trọng số)...]
    verts = []
    for v, p in enumerate(pts):
        sx, sy = sxy(p)
        bs = [(names[i], Wt[v, i]) for i in np.nonzero(Wt[v])[0]]
        verts.append(len(bs))
        for b, w in bs:
            bx, by = sxy(world[b])
            verts += [bidx[b], round(sx - bx, 3), round(sy - by, 3), round(float(w), 4)]
    uvs = []
    for p in pts:
        uvs += [round(p[0] / W, 6), round(p[1] / H, 6)]
    skin_name = code + "_skin"
    att = {"type": "mesh", "path": skin_name, "uvs": uvs, "triangles": [int(i) for i in tris.flatten()],
           "vertices": verts, "hull": int(nhull), "width": W, "height": H}
    anims = ANIMS[code]()
    raw = json.loads(json.dumps(anims))
    for a in anims.values():
        for tl in a.get("bones", {}).values():
            for kind, frames in tl.items():
                rig._convert_timeline(kind, frames)
    xs, ys = pts[:, 0], pts[:, 1]
    skel = {"skeleton": {"hash": code + "_mesh", "spine": "4.2.0", "x": round(xs.min() - rx), "y": 0,
                         "width": round(xs.max() - xs.min()), "height": round(ry - ys.min()), "images": "./images/"},
            "bones": bones, "slots": [{"name": "skin", "bone": "root", "attachment": skin_name}],
            "skins": [{"name": "default", "attachments": {"skin": {skin_name: att}}}], "animations": anims}
    name = code + "_mesh"
    json.dump(skel, open(os.path.join(out, name + ".json"), "w"))
    # kết cấu: ảnh gốc, nền trong suốt
    a = cv2.GaussianBlur(fg.astype(np.float32), (3, 3), 0.7)
    tex = np.dstack([rgb, np.clip(a * 255, 0, 255).astype(np.uint8)])
    Image.fromarray(tex).save(os.path.join(out, name + ".png"))
    open(os.path.join(out, name + ".atlas"), "w").write("\n".join([
        f"{name}.png", f"size: {W},{H}", "format: RGBA8888", "filter: Linear,Linear", "repeat: none",
        skin_name, "  rotate: false", "  xy: 0, 0", f"  size: {W}, {H}", f"  orig: {W}, {H}", "  offset: 0, 0",
        "  index: -1"]) + "\n")
    # ảnh soi: lưới + vùng trọng số
    dbg = Image.fromarray(rgb).resize((W * 2, H * 2), Image.LANCZOS).convert("RGB")
    col = np.array([[230, 60, 60], [60, 160, 230], [240, 190, 40], [120, 200, 80], [200, 90, 220], [40, 200, 190],
                    [250, 130, 40], [130, 130, 250], [220, 220, 220], [160, 90, 60], [90, 220, 140], [250, 90, 160]])
    vc = (Wt @ col[:len(names)]).astype(int)
    d = ImageDraw.Draw(dbg)
    for t in tris:
        p = [(pts[i][0] * 2, pts[i][1] * 2) for i in t]
        d.polygon(p, outline=(40, 40, 40))
    for v, p in enumerate(pts):
        d.ellipse([p[0] * 2 - 3, p[1] * 2 - 3, p[0] * 2 + 3, p[1] * 2 + 3], fill=tuple(vc[v]))
    for b, parent, j in m["bones"]:
        d.ellipse([j[0] * 2 - 6, j[1] * 2 - 6, j[0] * 2 + 6, j[1] * 2 + 6], outline=(255, 0, 160), width=3)
        d.text((j[0] * 2 + 8, j[1] * 2 - 6), b, fill=(255, 0, 160))
    dbg.save(os.path.join(out, "luoi.png"))
    rig.page(name, list(anims), out)
    draw = make_draw(pts, tris, Wt, names, world, (rx, ry), tex)
    rig.render(name, skel, raw, None, out, draw)
    print(f"{len(pts)} đỉnh ({nhull} viền), {len(tris)} tam giác, {len(bones)} xương, animation: {', '.join(anims)}")


def make_draw(pts, tris, Wt, names, world, root, tex):
    """bộ dựng khung cho lưới: da = tổng có trọng số (ma trận xương x vị trí gắn), vẽ từng tam giác."""
    rx, ry = root
    bind = {}
    for i, b in enumerate(names):
        bx, by = world[b][0] - rx, ry - world[b][1]
        bind[b] = np.stack([pts[:, 0] - rx - bx, ry - pts[:, 1] - by, np.ones(len(pts))], 0)  # 3 x N theo xương
    H, W = tex.shape[:2]

    def draw(skel, anim, t, img, k, box):
        Wb, Hb, ox, oy = box
        canvas = np.full((Hb, Wb, 3), (250, 246, 236), np.float32)
        wm, _ = rig.pose(skel, anim, t)
        P = np.zeros((2, len(pts)))
        for i, b in enumerate(names):
            w = Wt[:, i]
            if not w.any():
                continue
            P += (wm[b] @ bind[b])[:2] * w
        X = ox + P[0] * k
        Y = oy - P[1] * k
        for tri in tris:
            src = np.float32([[pts[i][0], pts[i][1]] for i in tri])
            dst = np.float32([[X[i], Y[i]] for i in tri])
            x0, y0 = np.floor(dst.min(0)).astype(int) - 1
            x1, y1 = np.ceil(dst.max(0)).astype(int) + 2
            x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, Wb), min(y1, Hb)
            if x1 <= x0 or y1 <= y0:
                continue
            M = cv2.getAffineTransform(src, dst - np.float32([x0, y0]))
            patch = cv2.warpAffine(tex, M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR,
                                   borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0)).astype(np.float32)
            mk = np.zeros((y1 - y0, x1 - x0), np.float32)
            # nới tam giác 0.6 px để không hở đường nối giữa các tam giác
            c = dst.mean(0)
            grown = c + (dst - c) * (1 + 0.6 / max(1.0, np.linalg.norm(dst - c, axis=1).min()))
            cv2.fillConvexPoly(mk, np.round((grown - [x0, y0]) * 4).astype(np.int32), 1.0, cv2.LINE_AA, 2)
            al = (patch[:, :, 3] / 255.0 * mk)[:, :, None]
            sub = canvas[y0:y1, x0:x1]
            canvas[y0:y1, x0:x1] = sub * (1 - al) + patch[:, :, :3] * al
        return canvas.astype(np.uint8)
    return draw


def sn_mesh_anims():
    A = rig.sn_anims()
    # tay cong: khuỷu gập theo vai, trễ nhịp một chút
    A["idle"]["bones"]["hand_l"] = {"rotate": rig.tl([(0, 0), (1.3, -5), (2.4, 0)])}
    A["idle"]["bones"]["hand_r"] = {"rotate": rig.tl([(0, 0), (1.3, 5), (2.4, 0)])}
    EO, EI = rig.EO, rig.EI
    A["attack"]["bones"]["hand_l"] = {"rotate": rig.tl([(0, 0), (0.3, -35, EO), (0.38, -40), (0.5, 30, EI), (0.64, 15),
                                                        (0.9, 0)])}
    A["attack"]["bones"]["hand_r"] = {"rotate": rig.tl([(0, 0), (0.3, 35, EO), (0.38, 40), (0.5, -30, EI), (0.64, -15),
                                                        (0.9, 0)])}
    A["skill"]["bones"]["hand_l"] = {"rotate": rig.tl([(0, 0), (0.3, 15), (0.62, -22, EO), (0.8, -25), (1.0, 30, EI),
                                                       (1.25, 5), (1.6, 0)])}
    A["skill"]["bones"]["hand_r"] = {"rotate": rig.tl([(0, 0), (0.3, -15), (0.62, 22, EO), (0.8, 25), (1.0, -30, EI),
                                                       (1.25, -5), (1.6, 0)])}
    # vai giơ vừa phải (lưới kéo da nên giơ quá cao tay sẽ gập đè lên đầu)
    A["skill"]["bones"]["arm_l"] = {"rotate": rig.tl([(0, 0), (0.3, 20), (0.6, -48, EO), (0.8, -52), (0.98, 25, EI),
                                                      (1.2, 10), (1.6, 0)])}
    A["skill"]["bones"]["arm_r"] = {"rotate": rig.tl([(0, 0), (0.3, -20), (0.6, 48, EO), (0.8, 52), (0.98, -25, EI),
                                                      (1.2, -10), (1.6, 0)])}
    A["hit"]["bones"]["hand_l"] = {"rotate": rig.tl([(0, 0), (0.12, -20, EO), (0.45, 0)])}
    A["hit"]["bones"]["hand_r"] = {"rotate": rig.tl([(0, 0), (0.12, 18, EO), (0.45, 0)])}
    A["walk"]["bones"]["hand_l"] = {"rotate": rig.tl([(0, 0), (0.3, -8), (0.55, 0), (0.8, 6), (1.0, 0)])}
    A["walk"]["bones"]["hand_r"] = {"rotate": rig.tl([(0, 0), (0.3, -6), (0.55, 0), (0.8, 8), (1.0, 0)])}
    return A


ANIMS = {"snorlax": sn_mesh_anims}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1] if len(sys.argv) > 1 else "snorlax")
