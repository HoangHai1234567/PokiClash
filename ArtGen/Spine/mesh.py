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
from PIL import Image, ImageDraw, ImageFont

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


def load_fg(m):
    rgb = np.array(Image.open(m["src"]).convert("RGB"))
    fg = rig.fg_mask(rgb, *m["fg"])
    fg = cv2.erode(fg, np.ones((3, 3), np.uint8)).astype(np.float32)
    fg = (cv2.GaussianBlur(fg, (0, 0), 1.6) > 0.5).astype(np.uint8)
    fg = rig.biggest(fg > 0, 500).astype(np.uint8)
    return rgb, fg


def mesh_mask(fg, step_edge, step_in, min_area=150):
    """lưới tam giác phủ mặt nạ fg (có thể nhiều khối rời): điểm viền mọi khối trước (hull), rồi điểm trong."""
    H, W = fg.shape
    cs, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    hull = []
    for c in sorted(cs, key=cv2.contourArea, reverse=True):
        if cv2.contourArea(c) < min_area:
            continue
        c = c[:, 0, :].astype(np.float64)
        seg = np.sqrt(((np.roll(c, -1, 0) - c) ** 2).sum(1))  # điểm viền cách đều theo chiều dài
        cum = np.concatenate([[0], np.cumsum(seg)])
        L = cum[-1]
        for t in np.linspace(0, L, max(8, int(L / step_edge)), endpoint=False):
            i = np.searchsorted(cum, t, side="right") - 1
            f = (t - cum[i]) / max(seg[i], 1e-6)
            hull.append(c[i] * (1 - f) + c[(i + 1) % len(c)] * f)
    hull = np.array(hull)
    dist = cv2.distanceTransform(fg, cv2.DIST_L2, 5)  # điểm trong: lưới lệch hàng, cách viền >= nửa bước
    s = step_in
    inner = []
    for j, y in enumerate(np.arange(s / 2, H, s * 0.87)):
        for x in np.arange(s / 2 + (s / 2 if j % 2 else 0), W, s):
            if dist[int(y), int(x)] > s * 0.55:
                inner.append((x, y))
    pts = np.concatenate([hull, np.array(inner).reshape(-1, 2)], 0)
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
    return pts, nh, np.array(tris, dtype=np.int64).reshape(-1, 3)


def build_mesh(m):
    rgb, fg = load_fg(m)
    pts, nh, tris = mesh_mask(fg, m["step_edge"], m["step_in"])
    return rgb, fg, pts, nh, tris


def label_map(m, rgb, fg):
    H, W = fg.shape
    dark = rgb.mean(2) < m["dark_thr"]
    cls = {"dark": dark, "light": ~dark}
    lab = np.full((H, W), -1, np.int32)
    names = []  # "xương#ghi chú" = thêm một vùng nữa cho cùng xương (lọc màu khác)
    for b, _, _ in m["labels"]:
        if b.split("#")[0] not in names:
            names.append(b.split("#")[0])
    for b, poly, keep in m["labels"]:
        i = names.index(b.split("#")[0])
        polys = poly if isinstance(poly[0][0], (list, tuple)) else [poly]  # một hay nhiều đa giác
        r = np.zeros(fg.shape, bool)
        for pg in polys:
            r |= rig.poly_mask(rgb.shape, pg)
        r &= (fg > 0) & (lab < 0)
        if isinstance(keep, tuple):  # ("lt", 80): độ sáng trung bình < 80; ("gt", 150): > 150
            r &= (rgb.mean(2) < keep[1]) if keep[0] == "lt" else (rgb.mean(2) > keep[1])
        elif keep:
            r &= cls[keep]
        lab[r] = i
    if m.get("smooth_labels"):  # mỗi pixel theo vùng chiếm đa số trong ô k x k: dải mảnh 1-2 px nhập về vùng bên cạnh
        k = m["smooth_labels"]
        cnt = np.stack([cv2.boxFilter((lab == i).astype(np.float32), -1, (k, k), normalize=False)
                        for i in range(len(names))], 0)
        best = cnt.argmax(0)
        lab = np.where(fg > 0, best, -1).astype(np.int32)
    return names, lab


def geo_dist(region, dom, R):
    """khoảng cách đi trong hình (loang từng bước trong miền dom), xa hơn R thì vô cực."""
    d = np.full(region.shape, np.inf, np.float32)
    cur = region > 0
    d[cur] = 0
    k = np.ones((3, 3), np.uint8)
    for i in range(1, R + 1):
        nb = (cv2.dilate(cur.astype(np.uint8), k) > 0) & dom & ~cur
        if not nb.any():
            break
        d[nb] = i
        cur |= nb
    return d


def weights(m, names, lab, pts, fg=None):
    sig = m["sigma"]
    W_ = np.zeros((len(pts), len(names)))
    dom = cv2.dilate(fg, np.ones((7, 7), np.uint8)) > 0 if fg is not None else None
    R = int(3.2 * max(v for v in sig.values()))
    for i, b in enumerate(names):
        region = (lab == i).astype(np.uint8)
        if m.get("geodesic") and dom is not None:
            d = geo_dist(region, dom, R)
        else:
            d = cv2.distanceTransform(1 - region, cv2.DIST_L2, 5)
        s = sig.get(b, sig["default"])
        xs = np.clip(pts[:, 0].round().astype(int), 0, lab.shape[1] - 1)
        ys = np.clip(pts[:, 1].round().astype(int), 0, lab.shape[0] - 1)
        W_[:, i] = np.exp(-(d[ys, xs] / s) ** 2)
    # 4 xương nặng nhất, bỏ < 2%
    for v in range(len(pts)):
        row = W_[v]
        if row.sum() == 0:  # đỉnh lọt ngoài miền: lấy vùng gần nhất theo đường thẳng
            x, y = int(round(pts[v, 0])), int(round(pts[v, 1]))
            ys_, xs_ = np.nonzero(lab >= 0)
            j = np.argmin((xs_ - x) ** 2 + (ys_ - y) ** 2)
            row[lab[ys_[j], xs_[j]]] = 1
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
    Wt = weights(m, names, lab, pts, fg)
    H, W = fg.shape
    rx, ry = m["root"]
    world = {"root": (rx, ry)}
    for b, parent, j, *_ in m["bones"]:
        world[b] = j

    def sxy(p):
        return p[0] - rx, ry - p[1]

    bones = [{"name": "root"}]
    for b, parent, j, *opt in m["bones"]:
        bx, by = sxy(j)
        px, py = sxy(world[parent])
        bones.append({"name": b, "parent": parent, "x": round(bx - px, 2), "y": round(by - py, 2), "length": 18,
                      **(opt[0] if opt else {})})
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
    for b, parent, j, *_ in m["bones"]:
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


MK = os.path.join(rig.SPINE_AI, "work", "man_kiem")
MESH["man_kiem"] = {  # ảnh người dùng gửi, chỉ để thử: quả mận trùm mũ, hai dao
    "src": os.path.join(MK, "src.png"),
    "out": os.path.join(MK, "rig_mesh"),
    "fg": (232, 20),
    "dark_thr": 90,
    "geodesic": True,  # lưỡi dao sát mép mũ: trọng số đi trong hình, không nhảy qua khe trắng
    "root": (183, 337),
    "bones": [
        ("body", "root", (183, 268)),
        ("head", "body", (183, 192)),
        ("leaf", "head", (192, 46)),
        ("cape_l", "body", (106, 236)),
        ("cape_r", "body", (262, 236)),
        ("arm_l", "body", (112, 212), {"inherit": "noScale"}),  # thân dẹp giãn không làm méo dao
        ("hand_l", "arm_l", (76, 232)),
        ("arm_r", "body", (255, 212), {"inherit": "noScale"}),
        ("hand_r", "arm_r", (292, 232)),
        ("foot_l", "root", (135, 300)),
        ("foot_r", "root", (238, 300)),
    ],
    "labels": [
        ("leaf", [[(80, 10), (180, 10), (180, 50), (130, 68), (84, 72)], [(172, 0), (215, 0), (212, 30), (205, 50), (178, 50)]],
         None),
        ("hand_l", [(0, 60), (72, 60), (72, 195), (90, 198), (92, 285), (0, 285)], None),
        ("hand_r", [(369, 60), (297, 60), (297, 195), (278, 198), (276, 285), (369, 285)], None),
        ("arm_l", [(88, 196), (118, 196), (118, 238), (88, 238)], None),
        ("arm_r", [(250, 196), (282, 196), (282, 238), (250, 238)], None),
        ("cape_l", [(82, 238), (118, 238), (118, 282), (82, 282)], None),
        ("cape_r", [(250, 238), (288, 238), (288, 282), (250, 282)], None),
        ("foot_l", [(85, 274), (183, 274), (183, 342), (85, 342)], None),
        ("foot_r", [(186, 274), (292, 274), (292, 342), (186, 342)], None),
        ("head", [(55, 20), (315, 20), (315, 198), (55, 198)], None),
        ("body", [(0, 0), (369, 0), (369, 342), (0, 342)], None),
    ],
    "sigma": {"default": 9, "head": 9, "leaf": 6, "hand_l": 5, "hand_r": 5, "body": 11},
    "layer": {"foot_l": 1, "foot_r": 1, "body": 2, "cape_l": 2, "cape_r": 2, "head": 3, "leaf": 4,
              "arm_l": 4, "arm_r": 4, "hand_l": 5, "hand_r": 5},
    "step_edge": 5,
    "step_in": 9,
}


def mk_anims():
    tl, tl2, E, EO, EI = rig.tl, rig.tl2, rig.E, rig.EO, rig.EI
    A = {}
    T = 1.6
    # đứng thở: người phập phồng, đầu nhún trễ, lá lắc trễ hơn, dao nhấp nhô, vạt áo đung đưa
    A["idle"] = {"bones": {
        "body": {"scale": tl2([(0, 1, 1), (0.8, 1.02, 0.975), (T, 1, 1)])},
        "head": {"translate": tl2([(0, 0, 0), (0.9, 0, -3), (T, 0, 0)]), "rotate": tl([(0, 0), (0.9, 1.5), (T, 0)])},
        "leaf": {"rotate": tl([(0, 0), (0.45, 5), (1.05, -5), (T, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (0.8, -3), (T, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.8, 3), (T, 0)])},
        "hand_l": {"rotate": tl([(0, 0), (0.95, 5), (T, 0)])},
        "hand_r": {"rotate": tl([(0, 0), (0.95, -5), (T, 0)])},
        "cape_l": {"rotate": tl([(0, 0), (1.0, -4), (T, 0)])},
        "cape_r": {"rotate": tl([(0, 0), (1.0, 4), (T, 0)])},
    }}
    # nhảy: ngồi lấy đà -> bật lên, dang tay -> rơi -> dẹp khi chạm đất -> nảy về
    J = 1.2
    A["jump"] = {"bones": {
        "root": {"translate": tl2([(0, 0, 0), (0.25, 0, 0), (0.5, 0, 85, EO), (0.62, 0, 90), (0.82, 0, 0, EI), (J, 0, 0)])},
        "body": {"scale": tl2([(0, 1, 1), (0.25, 1.1, 0.86, EO), (0.38, 0.92, 1.12), (0.62, 1, 1), (0.82, 1.02, 0.98),
                              (0.88, 1.14, 0.84, EO), (1.0, 0.96, 1.05), (J, 1, 1)])},
        "head": {"translate": tl2([(0, 0, 0), (0.25, 0, -6), (0.45, 0, 5), (0.88, 0, -8, EI), (1.0, 0, 2), (J, 0, 0)])},
        "leaf": {"rotate": tl([(0, 0), (0.3, 10), (0.55, -15), (0.8, 12), (0.95, -18, EO), (1.1, 6), (J, 0)])},
        "arm_l": {"rotate": tl([(0, 0), (0.25, 15), (0.5, -35, EO), (0.7, -30), (0.88, 15, EI), (J, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.25, -15), (0.5, 35, EO), (0.7, 30), (0.88, -15, EI), (J, 0)])},
        "hand_l": {"rotate": tl([(0, 0), (0.5, 20, EO), (0.88, -10, EI), (J, 0)])},
        "hand_r": {"rotate": tl([(0, 0), (0.5, -20, EO), (0.88, 10, EI), (J, 0)])},
        "foot_l": {"rotate": tl([(0, 0), (0.5, -10, EO), (0.82, 0, EI), (J, 0)])},
        "foot_r": {"rotate": tl([(0, 0), (0.5, 10, EO), (0.82, 0, EI), (J, 0)])},
        "cape_l": {"rotate": tl([(0, 0), (0.5, -8), (0.75, 14), (0.92, -6), (J, 0)])},
        "cape_r": {"rotate": tl([(0, 0), (0.5, 8), (0.75, -14), (0.92, 6), (J, 0)])},
    }}
    # chém chéo hai dao: giơ tay, dao ngả ra sau -> quét vào giữa thành chữ X -> dư lực -> về
    S = 0.9
    A["slash"] = {"bones": {
        "arm_l": {"rotate": tl([(0, 0), (0.24, -35, EO), (0.3, -38), (0.38, 30, EI), (0.5, 36, EO), (S, 0)])},
        "hand_l": {"rotate": tl([(0, 0), (0.24, 30, EO), (0.3, 34), (0.36, -118, EI), (0.48, -128, EO), (0.62, -120), (S, 0)])},
        "arm_r": {"rotate": tl([(0, 0), (0.24, 35, EO), (0.3, 38), (0.38, -30, EI), (0.5, -36, EO), (S, 0)])},
        "hand_r": {"rotate": tl([(0, 0), (0.24, -30, EO), (0.3, -34), (0.36, 118, EI), (0.48, 128, EO), (0.62, 120), (S, 0)])},
        "body": {"scale": tl2([(0, 1, 1), (0.24, 0.96, 1.06, EO), (0.3, 0.96, 1.07), (0.38, 1.08, 0.92, EI),
                              (0.5, 1.03, 0.96), (0.65, 0.99, 1.01), (S, 1, 1)]),
                 "translate": tl2([(0, 0, 0), (0.24, 0, 4), (0.38, 0, -6, EI), (0.55, 0, -3), (S, 0, 0)])},
        "head": {"translate": tl2([(0, 0, 0), (0.26, 0, 4), (0.4, 0, -6, EI), (0.56, 0, 2), (S, 0, 0)]),
                 "rotate": tl([(0, 0), (0.26, -2), (0.42, 2), (S, 0)])},
        "leaf": {"rotate": tl([(0, 0), (0.28, -10), (0.45, 16, EO), (0.62, -6), (S, 0)])},
        "cape_l": {"rotate": tl([(0, 0), (0.26, -6), (0.42, 10, EO), (0.6, -3), (S, 0)])},
        "cape_r": {"rotate": tl([(0, 0), (0.26, 6), (0.42, -10, EO), (0.6, 3), (S, 0)])},
    }}
    return A


# ---------------------------------------------------------------- nhiều lớp lưới
# Mỗi lớp (piece) = một slot, một lưới có trọng số riêng, xếp sau -> trước. Lớp nằm dưới được "mọc" thêm một dải dưới
# mép lớp đè lên nó (into, px) và dải đó được vẽ bù từ màu của chính lớp, để khi lớp trên đung đưa không lộ nền trắng.
def disk(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def bg_holes(m, rgb, fg, names, lab):
    """khe trắng nằm lọt giữa các vùng được kê (vd. khe giữa các lọn đuôi): coi là nền, không phải hình."""
    want = [names.index(n) for n in m["bg_holes"]]
    white = (rgb.min(2) >= m.get("hole_white", 246)) & (fg > 0)
    n, cl, st, _ = cv2.connectedComponentsWithStats(white.astype(np.uint8), connectivity=4)
    fg = fg.copy()
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] < 12:
            continue
        comp = cl == i
        ring = (cv2.dilate(comp.astype(np.uint8), disk(3)) > 0) & ~comp & ~white
        if ring.sum() and np.isin(lab[ring], want).mean() > 0.6:
            fg[cv2.dilate(comp.astype(np.uint8), disk(1)) > 0] = 0
    return fg


def main_multi(code):
    m = MESH[code]
    out = m["out"]
    os.makedirs(out, exist_ok=True)
    rgb, fg = load_fg(m)
    names, lab = label_map(m, rgb, fg)
    if m.get("bg_holes"):
        fg = bg_holes(m, rgb, fg, names, lab)
        names, lab = label_map(m, rgb, fg)
    H, W = fg.shape
    ni = {n: i for i, n in enumerate(names)}
    rx, ry = m["root"]
    world = {"root": (rx, ry)}
    for b, parent, j, *_ in m["bones"]:
        world[b] = j

    def sxy(p):
        return p[0] - rx, ry - p[1]

    bones = [{"name": "root"}]
    for b, parent, j, *opt in m["bones"]:
        bx, by = sxy(j)
        px, py = sxy(world[parent])
        bones.append({"name": b, "parent": parent, "x": round(bx - px, 2), "y": round(by - py, 2), "length": 18,
                      **(opt[0] if opt else {})})
    bidx = {b["name"]: i for i, b in enumerate(bones)}
    claimed = {n for pc in m["pieces"] if pc["labels"] != "rest" for n in pc["labels"]}
    pieces, ims = [], {}
    for pc in m["pieces"]:
        lbs = [n for n in names if n not in claimed] if pc["labels"] == "rest" else pc["labels"]
        own = np.isin(lab, [ni[n] for n in lbs]) & (fg > 0)
        ring = np.zeros_like(own)
        if pc.get("into"):
            into = np.isin(lab, [ni[n] for n in pc["into"]])
            ring = (cv2.dilate(own.astype(np.uint8), disk(pc["px"])) > 0) & into & ~own
        dom = own | ring
        dom = cv2.morphologyEx(dom.astype(np.uint8), cv2.MORPH_CLOSE, disk(2)) > 0
        dom = rig.biggest(dom, 120)
        # kết cấu lớp: pixel của lớp giữ nguyên, dải mọc thêm vẽ bù từ màu lớp
        tex = rgb.copy()
        if ring.any():
            work = rgb.copy()
            work[~own] = np.median(rgb[own], 0).astype(np.uint8)
            fill = (dom & ~own).astype(np.uint8) * 255
            tex = cv2.inpaint(work, fill, 7, cv2.INPAINT_TELEA)
            tex = np.where((dom & ~own)[..., None], cv2.GaussianBlur(tex, (0, 0), 1.5), tex)
            tex[own] = rgb[own]
        a = cv2.GaussianBlur(dom.astype(np.float32), (3, 3), 0.7)
        tex4 = np.dstack([tex, np.clip(a * 255, 0, 255).astype(np.uint8)])
        pts, nh, tris = mesh_mask(dom.astype(np.uint8), m["step_edge"], m["step_in"])
        plab = np.where(dom, lab, -1)
        Wt = weights(m, names, plab, pts, dom.astype(np.uint8))
        cen = pts[tris].mean(1)
        cl = plab[np.clip(cen[:, 1].astype(int), 0, H - 1), np.clip(cen[:, 0].astype(int), 0, W - 1)]
        layer = np.array([m["layer"].get(names[c], 2) if c >= 0 else 2 for c in cl])
        tris = tris[np.argsort(layer, kind="stable")]
        ys, xs = np.nonzero(a > 0.02)
        x0, y0, x1, y1 = max(0, xs.min() - 2), max(0, ys.min() - 2), min(W, xs.max() + 3), min(H, ys.max() + 3)
        rname = f"{code}_{pc['name']}"
        ims[rname] = Image.fromarray(tex4[y0:y1, x0:x1])
        verts, uvs = [], []
        for v, p in enumerate(pts):
            sx, sy = sxy(p)
            bs = [(names[i], Wt[v, i]) for i in np.nonzero(Wt[v])[0]]
            verts.append(len(bs))
            for b, w in bs:
                bx, by = sxy(world[b])
                verts += [bidx[b], round(sx - bx, 3), round(sy - by, 3), round(float(w), 4)]
            uvs += [round((p[0] - x0) / (x1 - x0), 6), round((p[1] - y0) / (y1 - y0), 6)]
        att = {"type": "mesh", "path": rname, "uvs": uvs, "triangles": [int(i) for i in tris.flatten()],
               "vertices": verts, "hull": int(nh), "width": int(x1 - x0), "height": int(y1 - y0)}
        pieces.append({"name": pc["name"], "rname": rname, "att": att, "pts": pts, "tris": tris, "Wt": Wt, "tex": tex4})
        print(f"  lớp {pc['name']:7s}: {len(pts)} đỉnh, {len(tris)} tam giác, mọc thêm {int(ring.sum())} px")
    anims = ANIMS[code]()
    raw = json.loads(json.dumps(anims))
    for a_ in anims.values():
        for tl_ in a_.get("bones", {}).values():
            for kind, frames in tl_.items():
                rig._convert_timeline(kind, frames)
    ys, xs = np.nonzero(fg)
    name = code + "_mesh"
    skel = {"skeleton": {"hash": name, "spine": "4.2.0", "x": round(xs.min() - rx), "y": 0,
                         "width": round(xs.max() - xs.min()), "height": round(ry - ys.min()), "images": "./images/"},
            "bones": bones,
            "slots": [{"name": p["name"], "bone": "root", "attachment": p["rname"]} for p in pieces],
            "skins": [{"name": "default", "attachments": {p["name"]: {p["rname"]: p["att"]} for p in pieces}}],
            "animations": anims}
    json.dump(skel, open(os.path.join(out, name + ".json"), "w"))
    aw, ah, place_ = rig.pack(ims, padding=2)
    atlas = Image.new("RGBA", (aw, ah), (0, 0, 0, 0))
    lines = [f"{name}.png", f"size: {aw},{ah}", "format: RGBA8888", "filter: Linear,Linear", "repeat: none"]
    for n, (x, y, w, h) in place_.items():
        atlas.paste(ims[n], (x, y))
        lines += [n, "  rotate: false", f"  xy: {x}, {y}", f"  size: {w}, {h}", f"  orig: {w}, {h}", "  offset: 0, 0",
                  "  index: -1"]
    atlas.save(os.path.join(out, name + ".png"))
    open(os.path.join(out, name + ".atlas"), "w").write("\n".join(lines) + "\n")
    # ảnh soi: từng lớp (dải vẽ bù hiện rõ) + lưới và màu trọng số
    col = np.array([[230, 60, 60], [60, 160, 230], [240, 190, 40], [120, 200, 80], [200, 90, 220], [40, 200, 190],
                    [250, 130, 40], [130, 130, 250], [220, 220, 220], [160, 90, 60], [90, 220, 140], [250, 90, 160]])
    col = np.concatenate([col, col[::-1] // 2 + 100, col // 2 + 60], 0)
    sheets = []
    for p in pieces:
        im = Image.new("RGB", (W, H), (205, 210, 220))
        t = Image.fromarray(p["tex"])
        im.paste(t, (0, 0), t)
        d = ImageDraw.Draw(im)
        vc = (p["Wt"] @ col[:len(names)]).astype(int)
        for tri in p["tris"]:
            d.polygon([tuple(p["pts"][i]) for i in tri], outline=(60, 60, 60))
        for v, q in enumerate(p["pts"]):
            d.ellipse([q[0] - 2, q[1] - 2, q[0] + 2, q[1] + 2], fill=tuple(vc[v]))
        for b, parent, j, *_ in m["bones"]:
            d.ellipse([j[0] - 5, j[1] - 5, j[0] + 5, j[1] + 5], outline=(255, 0, 160), width=2)
        d.text((8, 8), p["name"], fill=(0, 0, 0), font=ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 28))
        sheets.append(np.array(im))
    Image.fromarray(np.concatenate(sheets, 1)).save(os.path.join(out, "luoi.png"))
    rig.page(name, list(anims), out)
    draw = make_draw_multi(pieces, names, world, (rx, ry))
    rig.render(name, skel, raw, None, out, draw, fh=m.get("fh", 300), gif_scale=m.get("gif_scale", 1.2))
    if m.get("detail"):  # cận cảnh tỉ lệ gốc, các pha của animation đầu tiên, từng vùng
        an = list(raw)[0]
        pad = 60
        box = (W + 2 * pad, H + 2 * pad, rx + pad, ry + pad)
        frames = {t: draw(skel, raw[an], t, None, 1.0, box) for t in m["detail"]["times"]}
        rows = []
        F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
        for (x0, y0, x1, y1) in m["detail"]["boxes"]:
            cells = []
            for t, fr in frames.items():
                c = Image.fromarray(fr[y0 + pad:y1 + pad, x0 + pad:x1 + pad].copy())
                ImageDraw.Draw(c).text((6, 4), f"{t:.2f}s", fill=(200, 0, 0), font=F)
                cells.append(np.array(c))
            rows.append(np.concatenate(cells, 1))
        wmax = max(r.shape[1] for r in rows)
        rows = [np.pad(r, ((0, 6), (0, wmax - r.shape[1]), (0, 0)), constant_values=255) for r in rows]
        Image.fromarray(np.concatenate(rows, 0)).save(os.path.join(out, "chi_tiet.png"))
    print(f"{len(bones)} xương, {len(pieces)} lớp, atlas {aw}x{ah}, animation: {', '.join(anims)}")


def make_draw_multi(pieces, names, world, root):
    rx, ry = root
    for p in pieces:
        pts = p["pts"]
        p["bind"] = {b: np.stack([pts[:, 0] - world[b][0], (ry - pts[:, 1]) - (ry - world[b][1]), np.ones(len(pts))], 0)
                     for b in names}
        for b in names:  # toạ độ theo xương: gốc ở khớp, y lên
            p["bind"][b][0] = pts[:, 0] - world[b][0]
            p["bind"][b][1] = world[b][1] - pts[:, 1]

    def draw(skel, anim, t, img, k, box):
        Wb, Hb, ox, oy = box
        canvas = np.full((Hb, Wb, 3), (250, 246, 236), np.float32)
        wm, _ = rig.pose(skel, anim, t)
        for p in pieces:
            pts, tex = p["pts"], p["tex"]
            P = np.zeros((2, len(pts)))
            for i, b in enumerate(names):
                w = p["Wt"][:, i]
                if w.any():
                    P += (wm[b] @ p["bind"][b])[:2] * w
            X, Y = ox + P[0] * k, oy - P[1] * k
            for tri in p["tris"]:
                src = np.float32([pts[i] for i in tri])
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
                c = dst.mean(0)
                grown = c + (dst - c) * (1 + 0.6 / max(1.0, np.linalg.norm(dst - c, axis=1).min()))
                cv2.fillConvexPoly(mk, np.round((grown - [x0, y0]) * 4).astype(np.int32), 1.0, cv2.LINE_AA, 2)
                al = (patch[:, :, 3] / 255.0 * mk)[:, :, None]
                canvas[y0:y1, x0:x1] = canvas[y0:y1, x0:x1] * (1 - al) + patch[:, :, :3] * al
        return canvas.astype(np.uint8)
    return draw


TY = os.path.join(rig.SPINE_AI, "work", "tachyon")
MESH["tachyon"] = {  # ảnh người dùng gửi, chỉ để thử
    "src": os.path.join(TY, "src.png"),
    "out": os.path.join(TY, "rig_mesh"),
    "fg": (238, 18),
    "dark_thr": 120,
    "geodesic": True,
    "smooth_labels": 5,
    "root": (455, 1262),
    "fh": 420,
    "gif_scale": 1.25,
    "detail": {"times": [0.0, 0.75, 2.25], "boxes": [(290, 0, 600, 310), (70, 410, 350, 700), (110, 640, 890, 1060),
                                                    (470, 480, 870, 680)]},
    "bones": [
        ("body", "root", (410, 690)),
        ("head", "body", (420, 282)),
        ("ear_l", "head", (378, 62)),
        ("ear_r", "head", (512, 72)),
        ("ahoge", "head", (462, 52)),
        ("hair_l1", "head", (345, 150)),
        ("hair_l2", "hair_l1", (335, 228)),
        ("hair_r1", "head", (540, 150)),
        ("hair_r2", "hair_r1", (535, 226)),
        ("arm_r", "body", (500, 335), {"inherit": "noScale"}),
        ("cuff_r", "arm_r", (610, 385)),
        ("arm_l", "body", (318, 462), {"inherit": "noScale"}),
        ("sleeve_l2", "arm_l", (215, 560)),
        ("coat_l1", "body", (290, 690)),
        ("coat_l2", "coat_l1", (240, 820)),
        ("coat_r1", "body", (515, 680)),
        ("coat_r2", "coat_r1", (590, 880)),
        ("coat_rf", "coat_r1", (690, 735)),
        ("coat_rf2", "coat_rf", (780, 820)),
        ("tail1", "body", (515, 530)),
        ("tail2", "tail1", (630, 560)),
        ("tail3", "tail2", (735, 575)),
    ],
    "labels": [
        ("ear_l", [(338, 0), (402, 0), (404, 52), (372, 72), (342, 62)], None),
        ("ear_r", [(484, 0), (560, 0), (548, 78), (514, 88), (488, 58)], None),
        ("ahoge", [(425, 5), (505, 5), (505, 50), (470, 56), (428, 50)], None),
        ("hair_l2", [(298, 225), (362, 225), (362, 300), (298, 300)], ("lt", 165)),
        ("hair_l1", [(298, 120), (352, 120), (352, 225), (298, 225)], ("lt", 165)),
        ("hair_r2", [(505, 212), (578, 212), (578, 292), (505, 292)], ("lt", 165)),
        ("hair_r1", [(500, 105), (578, 105), (578, 212), (500, 212)], ("lt", 165)),
        ("head", [(325, 22), (568, 22), (568, 292), (470, 296), (420, 300), (328, 292)], None),
        ("tail1", [(495, 500), (600, 500), (600, 577), (575, 568), (556, 555), (530, 550), (500, 545)], ("lt", 165)),
        ("tail2", [(600, 500), (700, 500), (700, 662), (594, 662), (594, 579), (600, 577)], ("lt", 165)),
        ("tail3", [(700, 515), (845, 515), (845, 645), (700, 645)], ("lt", 165)),
        ("cuff_r", [(605, 230), (755, 230), (755, 480), (605, 480)], None),
        ("arm_r", [(482, 295), (605, 230), (605, 480), (540, 480), (488, 430)], None),
        ("sleeve_l2", [(84, 560), (175, 466), (240, 450), (250, 540), (244, 662), (200, 692), (84, 648)], None),
        ("arm_l", [(175, 468), (323, 426), (323, 500), (247, 540), (240, 452)], None),
        ("root", [[(295, 688), (565, 688), (565, 1100), (295, 1100)]], "dark"),
        ("coat_l2", [(128, 800), (306, 800), (306, 1002), (128, 1002)], "light"),
        ("coat_l1", [(130, 640), (306, 640), (306, 800), (130, 800)], "light"),
        ("coat_r2", [(478, 880), (706, 880), (706, 1048), (478, 1048)], "light"),
        ("coat_rf2", [(770, 680), (882, 680), (882, 968), (770, 968)], "light"),
        ("coat_rf", [(680, 690), (770, 690), (770, 968), (680, 968)], "light"),
        ("coat_r1", [(470, 480), (680, 480), (680, 880), (470, 880)], None),
        ("body", [(0, 0), (879, 0), (879, 1280), (0, 1280)], None),
    ],
    "pieces": [
        {"name": "tail", "labels": ["tail1", "tail2", "tail3"], "into": ["coat_r1", "body"], "px": 22},
        {"name": "legs", "labels": ["root"], "into": ["body", "coat_l1", "coat_l2", "coat_r1", "coat_r2"], "px": 16},
        {"name": "main", "labels": "rest", "into": ["arm_l", "sleeve_l2"], "px": 18},
        {"name": "sleeve", "labels": ["arm_l", "sleeve_l2"]},
    ],
    "sigma": {"default": 12, "head": 10, "hair_l1": 8, "hair_l2": 8, "hair_r1": 8, "hair_r2": 8, "ear_l": 6, "ear_r": 6,
              "ahoge": 6, "root": 4, "body": 14, "coat_l1": 18, "coat_l2": 18, "coat_r1": 18, "coat_r2": 18,
              "coat_rf": 16, "coat_rf2": 16, "tail1": 14, "tail2": 14, "tail3": 14, "sleeve_l2": 14, "arm_l": 12},
    "layer": {"body": 2, "coat_l1": 2, "coat_l2": 2, "coat_r1": 2, "coat_r2": 2, "coat_rf": 2, "coat_rf2": 2,
              "head": 3, "hair_l1": 4, "hair_l2": 4, "hair_r1": 4, "hair_r2": 4, "ear_l": 3, "ear_r": 3, "ahoge": 3,
              "arm_r": 4, "cuff_r": 4},
    "step_edge": 8,
    "step_in": 15,
}
# lớp chân: quần tất (rất tối, sáng TB ~57) + giày
MESH["tachyon"]["labels"][15] = ("root", [[(295, 688), (510, 688), (522, 800), (537, 900), (557, 1000), (572, 1100),
                                           (295, 1100)]], ("lt", 80))
MESH["tachyon"]["labels"].insert(15, ("root#shoes", [[(288, 1072), (372, 1072), (372, 1268), (288, 1268)],
                                                     [(512, 1072), (622, 1072), (622, 1268), (512, 1268)]], None))


def ty_anims():
    """idle 3 s: thở, nghiêng đầu; tóc, tai, ahoge, tay áo, vạt áo, đuôi lay theo gió, trễ pha dần ra ngọn."""
    tl, tl2, E = rig.tl, rig.tl2, rig.E
    T = 3.0

    def wave(amp, phase, n=8):  # dao động vòng lặp khép kín
        return tl([(round(T * i / n, 4), round(amp * math.sin(2 * math.pi * i / n - phase), 2)) for i in range(n + 1)])

    A = {"idle": {"bones": {
        "body": {"rotate": wave(0.8, 0.0),
                 "scale": tl2([(0, 1, 1), (1.5, 1.004, 1.012), (T, 1, 1)])},
        "head": {"rotate": tl([(0, 0), (0.75, -1.8), (2.25, 1.0), (T, 0)]),
                 "translate": tl2([(0, 0, 0), (1.6, 0, -2), (T, 0, 0)])},
        "ear_l": {"rotate": tl([(0, 0), (0.9, 3), (1.9, -2), (2.15, 9, rig.EO), (2.35, -2), (T, 0)])},  # giật tai
        "ear_r": {"rotate": wave(-3, 0.9)},
        "ahoge": {"rotate": wave(8, 1.4)},
        "hair_l1": {"rotate": wave(2.0, 0.7)},
        "hair_l2": {"rotate": wave(5.0, 1.3)},
        "hair_r1": {"rotate": wave(-2.0, 0.9)},
        "hair_r2": {"rotate": wave(-5.0, 1.5)},
        "arm_r": {"rotate": wave(2.2, 0.4)},
        "cuff_r": {"rotate": wave(4.5, 1.1)},
        "arm_l": {"rotate": wave(2.0, 0.5)},
        "sleeve_l2": {"rotate": wave(4.0, 1.2)},
        "coat_l1": {"rotate": wave(1.2, 0.6)},
        "coat_l2": {"rotate": wave(3.0, 1.2)},
        "coat_r1": {"rotate": wave(-1.0, 0.7)},
        "coat_r2": {"rotate": wave(-2.5, 1.3)},
        "coat_rf": {"rotate": wave(3.0, 1.0)},
        "coat_rf2": {"rotate": wave(6.0, 1.7)},
        "tail1": {"rotate": wave(4.0, 0.6)},
        "tail2": {"rotate": wave(7.0, 1.3)},
        "tail3": {"rotate": wave(10.0, 2.0)},
    }}}
    return A


ANIMS = {"snorlax": sn_mesh_anims, "man_kiem": mk_anims, "tachyon": ty_anims}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    code = sys.argv[1] if len(sys.argv) > 1 else "snorlax"
    (main_multi if "pieces" in MESH[code] else main)(code)
