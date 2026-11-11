# -*- coding: utf-8 -*-
"""Soi không cần Chrome: bộ vẽ Python cho rig của quai (tính da lưới như runtime: tổng có trọng số ma trận thế giới xương nhân toạ
độ gắn; mặt nạ cắt; độ đậm, hình trong slot).

    ve = soi.Ve(sk, atlas_rgba, place)                 # sau xuat.ghi_spine (vẽ từ atlas bảng 256 màu thật), hoặc Ve(sk) từ ảnh mảnh
    soi.to_khung(ve, frames, clip, "rig/khung_idle.png")   # 12 khung, nền xám 150
    soi.anh_luoi(sk, "rig/luoi.png")                    # lưới + màu trọng số + xương
    soi.anh_can(ve, P, (x, y), 60, "rig/can_mieng.png")  # cận một vùng, phóng 4 lần, có lưới
    soi.lech(ve, Pa, Pb)                                # lệch lớn nhất (px rig) giữa hai tư thế (nối clip)
    soi.chay_chrome(rig_dir, ten, ra_dir, "n=12")       # tờ khung bằng runtime Spine thật (mo_xe/chay.py) qua khoa.py chrome
"""
import colorsys
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

from . import anh
from .khung import mat

HERE = os.path.dirname(os.path.abspath(__file__))
SPINE = os.path.dirname(HERE)


def mau_xuong(i):
    r, g, b = colorsys.hsv_to_rgb((i * 0.618034) % 1.0, 0.85, 0.95)
    return np.array([r * 255, g * 255, b * 255])


class Ve:
    def __init__(self, sk, atlas=None, place=None):
        self.sk = sk
        self.src = {}
        # nguồn đổi sẵn sang RGBa (nhân alpha): Image.transform với RGBA tự đổi CẢ ảnh mỗi lần gọi (chậm)
        if atlas is not None:
            atlas = atlas.convert("RGBA").convert("RGBa")
            for p, (x, y, w, h) in place.items():
                self.src[p] = (atlas, x, y, w, h)
        for p, im in sk.images.items():
            if p not in self.src:
                self.src[p] = (im.convert("RGBA").convert("RGBa"), 0, 0, im.width, im.height)
        self._pre = {}

    def _prep(self, slot, an, spec):
        key = (slot, an)
        if key in self._pre:
            return self._pre[key]
        if spec["type"] == "mesh":
            groups = {}
            for i, row in enumerate(spec["verts"]):
                for b, lx, ly, w in row:
                    groups.setdefault(b, ([], [], [], []))
                    g = groups[b]
                    g[0].append(i)
                    g[1].append(lx)
                    g[2].append(ly)
                    g[3].append(w)
            pre = {"n": len(spec["verts"]), "g": {b: tuple(np.array(v, float if k else int) for k, v in enumerate(g)) for b, g in groups.items()},
                   "uv": np.asarray(spec["uv"], float), "tris": np.asarray(spec["tris"], int)}
        else:
            w, h = spec["width"], spec["height"]
            M = mat(spec["x"], spec["y"], spec.get("rotation", 0.0), spec.get("scaleX", 1.0), spec.get("scaleY", 1.0))
            loc = np.array([[-w / 2, h / 2, 1], [w / 2, h / 2, 1], [w / 2, -h / 2, 1], [-w / 2, -h / 2, 1]], float) @ M.T
            pre = {"loc": loc[:, :2], "bone": spec["bone"], "uv": np.array([[0, 0], [1, 0], [1, 1], [0, 1]], float),
                   "tris": np.array([[0, 1, 2], [2, 3, 0]])}
        self._pre[key] = pre
        return pre

    def skin(self, P=None, W=None):
        """[(slot, hình, V thế giới (N, 2), uv (N, 2), tris, độ đậm, ảnh, chỉ số slot)] theo thứ tự vẽ, và danh sách mặt nạ."""
        sk = self.sk
        W = W or sk.the_gioi(P)
        out, masks = [], []
        for si, s in enumerate(sk.slots):
            nm = s["name"]
            an = P.att.get(nm, s["att"]) if P is not None else s["att"]
            if an is None or an not in sk.atts.get(nm, {}):
                continue
            spec = sk.atts[nm][an]
            if spec["type"] == "clipping":
                v = np.array(spec["verts"], float).reshape(-1, 2)
                Wb = W[s["bone"]]
                masks.append((si, sk.si.get(spec["end"], len(sk.slots) - 1), v @ Wb[:2, :2].T + Wb[:2, 2]))
                continue
            a = P.alpha.get(nm, s["alpha"]) if P is not None else s["alpha"]
            pre = self._prep(nm, an, spec)
            if spec["type"] == "mesh":
                V = np.zeros((pre["n"], 2))
                for b, (idx, lx, ly, w) in pre["g"].items():
                    M = W[b]
                    np.add.at(V, idx, np.stack([(M[0, 0] * lx + M[0, 1] * ly + M[0, 2]) * w, (M[1, 0] * lx + M[1, 1] * ly + M[1, 2]) * w], 1))
            else:
                M = W[pre["bone"]]
                V = pre["loc"] @ M[:2, :2].T + M[:2, 2]
            out.append((nm, an, V, pre["uv"], pre["tris"], float(a), spec["path"], si))
        return out, masks

    def bao(self, P=None, an_mo=0.01):
        """khung bao thế giới (x0, y0, x1, y1) của các hình đang hiện."""
        sk_, _ = self.skin(P)
        Vs = [V for _, _, V, _, _, a, _, _ in sk_ if a > an_mo]
        if not Vs:
            return (-1, -1, 1, 1)
        V = np.vstack(Vs)
        return (float(V[:, 0].min()), float(V[:, 1].min()), float(V[:, 0].max()), float(V[:, 1].max()))

    def ve(self, P, box, scale, bg=None, ss=1, luoi=False, xuong=False, W=None, mau_luoi=(20, 20, 20, 150)):
        """vẽ tư thế P trong khung thế giới box = (x0, y0, x1, y1) với tỉ lệ scale px/đơn vị rig. ss: vẽ lớn ss lần rồi thu (mịn)."""
        sk = self.sk
        W = W or sk.the_gioi(P)
        x0, y0, x1, y1 = box
        k = scale * ss
        Wc, Hc = max(1, int(math.ceil((x1 - x0) * k))), max(1, int(math.ceil((y1 - y0) * k)))
        canvas = Image.new("RGBA", (Wc, Hc), tuple(bg) + (255,) if bg is not None else (0, 0, 0, 0))
        items, masks = self.skin(P, W)
        tf = lambda V: np.stack([(V[:, 0] - x0) * k, (y1 - V[:, 1]) * k], 1)  # noqa: E731
        edges = []
        for nm, an, V, uv, tris, a, path, si in items:
            if a < 0.01 or not len(tris):
                continue
            src, ox, oy, sw, sh = self.src[path]
            D = tf(V)
            S = uv * np.array([sw, sh]) + np.array([ox, oy])
            bx0, by0 = max(0, int(math.floor(D[:, 0].min())) - 1), max(0, int(math.floor(D[:, 1].min())) - 1)
            bx1, by1 = min(Wc, int(math.ceil(D[:, 0].max())) + 2), min(Hc, int(math.ceil(D[:, 1].max())) + 2)
            if bx1 <= bx0 or by1 <= by0:
                continue
            layer = Image.new("RGBa", (bx1 - bx0, by1 - by0), (0, 0, 0, 0))
            off = np.array([bx0, by0], float)
            _tris(layer, src, D - off, S, tris)
            layer = layer.convert("RGBA")
            if a < 0.999:
                al = np.asarray(layer).copy()
                al[..., 3] = (al[..., 3] * a).astype(np.uint8)
                layer = Image.fromarray(al, "RGBA")
            for ms, me, poly in masks:
                if ms < si <= me:
                    mk = Image.new("L", layer.size, 0)
                    ImageDraw.Draw(mk).polygon([tuple(p) for p in (tf(poly) - off).tolist()], fill=255)
                    al = np.asarray(layer).copy()
                    al[..., 3] = (al[..., 3].astype(np.float32) * (np.asarray(mk) / 255.0)).astype(np.uint8)
                    layer = Image.fromarray(al, "RGBA")
            canvas.alpha_composite(layer, (bx0, by0))
            if luoi:
                edges.append((D, tris))
        d = ImageDraw.Draw(canvas)
        if luoi:
            for D, tris in edges:
                for t in tris:
                    p = [tuple(D[i]) for i in t]
                    d.line(p + [p[0]], fill=mau_luoi, width=max(1, ss))
        if xuong:
            for i, b in enumerate(sk.bones):
                M = W[b["name"]]
                L = b["length"] or 12
                p0 = tf(M[:2, 2][None])[0]
                p1 = tf((M @ np.array([L, 0, 1.0]))[:2][None])[0]
                c = tuple(int(v) for v in mau_xuong(i)) + (255,)
                d.line([tuple(p0), tuple(p1)], fill=c, width=2 * ss)
                r = 3 * ss
                d.ellipse([p0[0] - r, p0[1] - r, p0[0] + r, p0[1] + r], outline=(0, 0, 0, 255), fill=c)
        if ss > 1:
            canvas = canvas.resize((max(1, Wc // ss), max(1, Hc // ss)), Image.LANCZOS)
        return canvas


def _tris(layer, src, D, S, tris):
    """chép các tam giác ảnh nguồn (S[tris], px) vào tam giác đích (D[tris], px trong layer): affine tính gộp bằng numpy, mỗi tam
    giác một lần Image.transform (nguồn RGBa) + mặt nạ đa giác."""
    d, s = D[tris], S[tris]                       # (T, 3, 2)
    a00, a01 = d[:, 1, 0] - d[:, 0, 0], d[:, 2, 0] - d[:, 0, 0]
    a10, a11 = d[:, 1, 1] - d[:, 0, 1], d[:, 2, 1] - d[:, 0, 1]
    det = a00 * a11 - a01 * a10
    ok = np.abs(det) > 1e-6
    det = np.where(ok, det, 1.0)
    i00, i01, i10, i11 = a11 / det, -a01 / det, -a10 / det, a00 / det
    b00, b01 = s[:, 1, 0] - s[:, 0, 0], s[:, 2, 0] - s[:, 0, 0]
    b10, b11 = s[:, 1, 1] - s[:, 0, 1], s[:, 2, 1] - s[:, 0, 1]
    m00, m01 = b00 * i00 + b01 * i10, b00 * i01 + b01 * i11
    m10, m11 = b10 * i00 + b11 * i10, b10 * i01 + b11 * i11
    x0 = np.maximum(0, np.floor(d[:, :, 0].min(1))).astype(int)
    y0 = np.maximum(0, np.floor(d[:, :, 1].min(1))).astype(int)
    x1 = np.minimum(layer.width, np.ceil(d[:, :, 0].max(1)) + 1).astype(int)
    y1 = np.minimum(layer.height, np.ceil(d[:, :, 1].max(1)) + 1).astype(int)
    dx, dy = x0 - d[:, 0, 0], y0 - d[:, 0, 1]
    c0 = s[:, 0, 0] + m00 * dx + m01 * dy
    c1 = s[:, 0, 1] + m10 * dx + m11 * dy
    rows = np.stack([m00, m01, c0, m10, m11, c1], 1).tolist()
    dl = d.tolist()
    for k in np.flatnonzero(ok & (x1 > x0) & (y1 > y0)).tolist():
        X0, Y0, w, h = int(x0[k]), int(y0[k]), int(x1[k] - x0[k]), int(y1[k] - y0[k])
        patch = src.transform((w, h), Image.AFFINE, rows[k], resample=Image.BILINEAR)
        mk = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mk).polygon([(px - X0, py - Y0) for px, py in dl[k]], fill=255, outline=255)
        layer.paste(patch, (X0, Y0), mk)


# ---------------------------------------------------------------- tờ khung
def _union(boxes, pad=0.06):
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes)
    y1 = max(b[3] for b in boxes)
    px, py = (x1 - x0) * pad + 4, (y1 - y0) * pad + 4
    return (x0 - px, y0 - py, x1 + px, y1 + py)


def to_khung(ve, frames, clip, ra, n=12, cot=6, fh=300, bg=(150, 150, 150), box=None, fps=30, ss=2, luoi=False):
    """tờ n khung của clip (đều từ 0 tới dur; clip lặp bỏ khung cuối trùng khung 0), nền xám bg. Khung nhìn chung cho cả tờ
    (khung bao mọi khung chọn, thêm box nếu có). Ghi giờ và sự kiện dưới mỗi khung."""
    dur = clip.dur
    ts = np.linspace(0, dur, n + (1 if clip.loop else 0))[:n]
    idx = [min(len(frames) - 1, int(round(t * fps))) for t in ts]
    boxes = [ve.bao(frames[i]) for i in idx] + ([box] if box else [])
    B = _union(boxes)
    bw, bh = B[2] - B[0], B[3] - B[1]
    sc = fh / bh
    tw = int(min(2.2 * fh, max(0.5 * fh, bw * sc)))
    sc = min(sc, tw / bw)
    rows = int(math.ceil(n / cot))
    lab = 34
    sheet = Image.new("RGB", (cot * tw, rows * (fh + lab)), tuple(bg))
    d = ImageDraw.Draw(sheet)
    f = anh.font(13)
    for k, (t, i) in enumerate(zip(ts, idx)):
        img = ve.ve(frames[i], B, sc, bg=bg, ss=ss, luoi=luoi)
        x, y = (k % cot) * tw, (k // cot) * (fh + lab)
        sheet.paste(img.convert("RGB"), (x + (tw - img.width) // 2, y))
        evs = [nm + (f"({st})" if st else "") for te, nm, st in clip.ev if abs(te - t) <= dur / (2 * n) + 1e-6]
        d.text((x + 4, y + fh + 2), f"{clip.ten} {t:.2f}s", fill=(20, 20, 20), font=f)
        if evs:
            d.text((x + 4, y + fh + 17), " ".join(evs), fill=(140, 20, 20), font=f)
        d.line([(x + tw - 1, y), (x + tw - 1, y + fh + lab)], fill=(120, 120, 120))
    os.makedirs(os.path.dirname(os.path.abspath(ra)), exist_ok=True)
    sheet.save(ra)
    return ra


def anh_luoi(sk, ra, ve=None, o=330, cot=4):
    """luoi.png: mỗi lưới một ô (ảnh mảnh, tam giác tô màu trộn theo trọng số, cạnh, đỉnh, số liệu) + dáng gốc có xương."""
    cols = {b["name"]: mau_xuong(i) for i, b in enumerate(sk.bones)}
    tiles = []
    f = anh.font(12)
    for (slot, an), L in sk.luoi.items():
        spec = sk.atts[slot][an]
        im = sk.images[spec["path"]]
        k = min(o / im.width, (o - 40) / im.height, 5.0)
        tw, th = int(im.width * k) + 16, int(im.height * k) + 52
        t = Image.new("RGBA", (max(tw, 220), th), (150, 150, 150, 255))
        big = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))), Image.LANCZOS)
        t.alpha_composite(big, (8, 8))
        ov = Image.new("RGBA", t.size, (0, 0, 0, 0))
        dd = ImageDraw.Draw(ov)
        P = L.pts * k + 8
        vc = np.array([sum((cols[b] * w for b, _, _, w in row), np.zeros(3)) for row in spec["verts"]])
        for tri in L.tris:
            c = vc[tri].mean(0)
            dd.polygon([tuple(P[i]) for i in tri], fill=tuple(int(v) for v in c) + (95,), outline=(25, 25, 25, 170))
        for i, p in enumerate(P):
            r = 1.8
            dd.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=tuple(int(v) for v in vc[i]) + (255,))
        t.alpha_composite(ov)
        st = L.thong_ke()
        bones = sorted({b for row in spec["verts"] for b, _, _, _ in row})
        dw = ImageDraw.Draw(t)
        dw.text((8, th - 42), f"{slot}/{an}: {st['dinh']} đỉnh, {st['tam_giac']} tg, góc min {st['goc_min']:.0f}°, hở {st['ho']}", fill=(0, 0, 0), font=f)
        dw.text((8, th - 26), ("xương: " + " ".join(bones))[:70], fill=(0, 0, 0), font=f)
        x = 8
        for b in bones[:12]:
            dw.rectangle([x, th - 10, x + 14, th - 3], fill=tuple(int(v) for v in cols[b]))
            x += 17
        tiles.append(t)
    ve = ve or Ve(sk)
    B = _union([ve.bao(None)], 0.08)
    sc = min(700 / (B[2] - B[0]), 600 / (B[3] - B[1]))
    setup = ve.ve(None, B, sc, bg=(150, 150, 150), ss=2, xuong=True)
    W_ = max(cot * (o + 20), setup.width + 20)
    rows, x, y, rh = [], 10, setup.height + 20, 0
    places = []
    for t in tiles:
        if x + t.width > W_:
            x, y, rh = 10, y + rh + 10, 0
        places.append((t, x, y))
        x += t.width + 10
        rh = max(rh, t.height)
    sheet = Image.new("RGBA", (W_, y + rh + 10), (120, 124, 132, 255))
    sheet.alpha_composite(setup, (10, 10))
    for t, x, y in places:
        sheet.alpha_composite(t, (x, y))
    sheet.convert("RGB").save(ra)
    return ra


def anh_can(ve, P, tam, r, ra, phong=4.0, luoi=True, bg=(150, 150, 150)):
    """ảnh cận vùng tâm tam (x, y thế giới), bán kính r (đơn vị rig), phóng phong lần, có lưới."""
    cx, cy = tam
    img = ve.ve(P, (cx - r, cy - r, cx + r, cy + r), phong, bg=bg, ss=1, luoi=luoi, mau_luoi=(10, 10, 10, 90))
    img.convert("RGB").save(ra)
    return ra


def ghep_anh(paths, ra, cot=3, nhan=None):
    """ghép nhiều ảnh soi vào một tờ (cận miệng ở vài giờ...)."""
    ims = [Image.open(p).convert("RGB") for p in paths]
    w = max(i.width for i in ims)
    h = max(i.height for i in ims) + 18
    rows = int(math.ceil(len(ims) / cot))
    sheet = Image.new("RGB", (cot * w, rows * h), (120, 124, 132))
    d = ImageDraw.Draw(sheet)
    f = anh.font(13)
    for k, im in enumerate(ims):
        x, y = (k % cot) * w, (k // cot) * h
        sheet.paste(im, (x, y))
        d.text((x + 4, y + im.height + 2), (nhan[k] if nhan else os.path.basename(paths[k])), fill=(255, 255, 255), font=f)
    sheet.save(ra)
    return ra


# ---------------------------------------------------------------- số đo
def chieu_cao(ve, P, bo=()):
    """đỉnh cao nhất (y rig) của các hình đang hiện ở tư thế P (game.height = chiều cao dáng đứng khung 0 idle)."""
    items, _ = ve.skin(P)
    ys = [V[:, 1].max() for nm, _, V, _, _, a, _, _ in items if a > 0.01 and nm not in bo]
    return float(max(ys)) if ys else 1.0


def lech(ve, Pa, Pb):
    """lệch lớn nhất giữa hai tư thế (đơn vị rig) trên các hình hiện ở cả hai; và slot lệch nhất. Hình hiện ở một bên mà không ở
    bên kia (độ đậm khác > 0,2) tính là lệch vô cùng."""
    A, _ = ve.skin(Pa)
    B, _ = ve.skin(Pb)
    da = {(x[0], x[1]): x for x in A}
    best, where = 0.0, ""
    for xb in B:
        key = (xb[0], xb[1])
        xa = da.get(key)
        if xa is None:
            if xb[5] > 0.2:
                return float("inf"), f"{xb[0]} (chỉ hiện ở một bên)"
            continue
        if abs(xa[5] - xb[5]) > 0.2:
            return float("inf"), f"{xb[0]} (độ đậm {xa[5]:.2f} / {xb[5]:.2f})"
        if min(xa[5], xb[5]) < 0.05:
            continue
        dd = float(np.hypot(*(xa[2] - xb[2]).T).max())
        if dd > best:
            best, where = dd, xb[0]
    kb = {(x[0], x[1]) for x in B}
    for xa in A:
        if (xa[0], xa[1]) not in kb and xa[5] > 0.2:
            return float("inf"), f"{xa[0]} (chỉ hiện ở một bên)"
    return best, where


def chan_dung(ve, P, ra, co=512, le=0.06, bo=()):
    """chân dung vuông co px, nền trong suốt, không bóng: vẽ tư thế P (khung 0 idle) lớn rồi cắt vuông ôm cả con. bo: slot không
    vẽ (đồ bay của aura)."""
    if bo:
        P = P.copy()
        for s in bo:
            P.alpha[s] = 0.0
    B = ve.bao(P)
    side = max(B[2] - B[0], B[3] - B[1]) * (1 + 2 * le)
    cx, cy = (B[0] + B[2]) / 2, (B[1] + B[3]) / 2
    box = (cx - side / 2, cy - side / 2, cx + side / 2, cy + side / 2)
    img = ve.ve(P, box, 2 * co / side, ss=1)
    img = img.resize((co, co), Image.LANCZOS)
    img.save(ra)
    return ra


# ---------------------------------------------------------------- runtime Spine thật (Chrome ngầm, qua khoá)
def chay_chrome(rig_dir, ten, ra_dir, tham_so="n=12", che_do="sheet", them=None):
    """chạy mo_xe/chay.py (runtime Spine gốc trong Chrome/Edge ngầm) LUÔN qua quai/khoa.py chrome (1 suất cả máy: máy từng sập
    cứng khi Chrome ngầm vẽ). che_do: sheet | info | keys | mesh | sample. Trả mã thoát."""
    py = sys.executable
    cmd = [py, "-I", os.path.join(HERE, "khoa.py"), "chrome", "--", py, "-I", os.path.join(SPINE, "mo_xe", "chay.py"), che_do,
           os.path.abspath(rig_dir), ten, os.path.abspath(ra_dir)]
    if che_do == "sheet":
        cmd.append(tham_so)
    elif them:
        cmd += list(them)
    print("  chrome:", " ".join(cmd[-6:]))
    return subprocess.call(cmd)
