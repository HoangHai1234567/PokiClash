# -*- coding: utf-8 -*-
"""Sơ đồ bố cục rồng vây (mã làm việc rong_vay, tướng thứ 8 đảo Thủy, 2026-11-11) để đính vào prompt concept.

Con gốc của rig: monster_3458 (game tham khảo, đã mổ ở <SXS>/scan/monster_3458). Sơ đồ CHỈ lấy cách dựng của rig: chỗ đặt, cỡ và
thứ tự chồng của từng mảnh (hình bóng mảnh đã làm trơn, bỏ mọi nét vẽ, hoa văn, màu của con gốc), rồi tô phẳng theo thiết kế của
mình: thân chàm tím, bụng kem có vạch, vây và màng cánh lam xám trầm có tia vây chàm sẫm, sừng màu cát, giáp vỏ sò trên lưng, đốm kem trên
cánh, mắt hổ phách. GPT lấy bố cục và tỉ lệ, không lấy nét.

    py -3 -I ArtGen/Spine/rong_vay_bo_cuc.py   →  inbox/rong_vay_1/mau/bo_cuc.png (1536 × 1024, nền trắng) + bo_cuc_so.png (có số mảnh)
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
sys.path.insert(0, HERE)
from quai.soi import _tris  # noqa: E402
import to_manh  # noqa: E402

CODE = "rong_vay"
MON = "monster_3458"


def sxs():
    c = [os.environ.get("SXS"), r"D:\Ripper\SwordxStaff", r"E:\Ripper\SwordxStaff", r"C:\Ripper\SwordxStaff"]
    for p in c:
        if p and os.path.isdir(p):
            return p
    raise SystemExit("không thấy thư mục SwordxStaff (đặt biến môi trường SXS)")


Z = 2                      # vẽ gấp đôi rồi thu
W, H = 1536, 1024
SC = 0.80                  # đơn vị rig → pixel khung
INK = (43, 33, 24)
PAL = dict(body=(52, 64, 143), belly=(243, 230, 196), fin=(106, 155, 168), ray=(36, 44, 104), horn=(38, 37, 44),
           beak=(38, 37, 44), shell=(250, 240, 214), spot=(250, 240, 214), brow=(36, 44, 104), eye=(242, 179, 61),
           rib=(201, 154, 85))      # 2026-11-11: người dùng chê lam ngọc + cam loè loẹt → vây lam xám trầm, tia và sống cánh chàm sẫm

KIND = {"P_shenti01": "body", "P_shenti02": "body", "P_shenti03": "body", "P_shenti04": "body", "P_shenti05": "body",
        "P_shenti06": "body", "P_shenti07": "body", "P_tou": "head", "P_zuiba01": "beak", "P_zuiba02": "beak",
        "P_erduo": "brow", "P_yuqi03": "horn", "P_yuqi04": "horn", "P_chibangR06": "web", "P_chibangL06": "web",
        "P_chibangR08": "spar", "P_chibangL05": "spar", "P_chibangR08_2": "spar", "P_chibangR08_3": "spar",
        "P_yanjing01": "eye"}
OPEN = {"body": 3, "head": 3, "beak": 0, "brow": 0, "horn": 4, "web": 13, "spar": 2, "fin": 4}     # bán kính làm trơn (px khung)


def dung(only=None, luu=True):
    """only: chỉ dựng các slot này (mỗi mảnh vẽ đủ cả phần khuất) cho tờ hướng dẫn gen mảnh. Trả (ảnh 1536 × 1024, mặt nạ từng
    slot ở cỡ khung, thứ tự vẽ từng slot)."""
    root = sxs()
    rig = os.path.join(root, "web", "assets", "Monster", MON)
    D = json.load(open(os.path.join(root, "scan", MON, "att_goc.json"), encoding="utf-8"))
    atlas, imgs = to_manh.nap(rig, MON)
    atts = sorted([a for a in D["atts"] if a["cur"] and a.get("region") in imgs], key=lambda a: a["order"])
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    s = SC * Z
    ox = (W * Z - (x1 - x0) * s) / 2 - x0 * s
    oy = (H * Z + (y1 - y0) * s) / 2 + y0 * s

    def T(p):
        p = np.asarray(p, float)
        return np.stack([p[..., 0] * s + ox, oy - p[..., 1] * s], -1)

    bones = D["bones"]
    bi = {b["name"]: b for b in bones}

    def seg(b):
        return T((b["x"], b["y"])), T((b["x"] + b["a"] * b["len"], b["y"] + b["c"] * b["len"]))

    def ras(a):
        im = imgs[a["region"]]
        V = T(np.array(a["xy"], float).reshape(-1, 2))
        UV = np.array(a["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
        tr = np.array(a["tris"]).reshape(-1, 3)
        lay = Image.new("RGBa", (W * Z, H * Z), (0, 0, 0, 0))
        _tris(lay, im.convert("RGBa"), V, UV, tr)
        return np.asarray(lay.convert("RGBA"))

    def el(r):
        r = max(1, int(round(r * Z)))
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))

    def smooth(m, r):
        m = (m > 0).astype(np.uint8) * 255
        if r > 0:
            m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(r))
            m = cv2.morphologyEx(m, cv2.MORPH_OPEN, el(r))
        m = cv2.GaussianBlur(m, (0, 0), 2.0 * Z)
        return m > 127

    def biggest(m):
        n, lab, st, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
        if n <= 2:
            return m
        k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        return lab == k

    # đường sống thân: đầu → cổ → giữa thân → vòng cuộn → đuôi (xương của rig), để kẻ vạch bụng vuông góc với thân
    chain = ["Q_shenti5", "Q_shenti4", "Q_shenti3", "Q_shenti2", "Q_shenti", "H_shenti", "H_shenti2", "H_shenti3", "H_shenti4",
             "H_shenti5", "H_shenti6", "H_shenti7", "H_shenti8", "weiba", "weiba2", "weiba3", "weiba4", "weiba5"]
    pts = [seg(bi["Q_shenti5"])[1]] + [seg(bi[n])[0] for n in chain]
    pts.append(seg(bi["weiba5"])[1])
    pts = np.array(pts)

    def catmull(p, n=24):
        q = np.concatenate([p[:1], p, p[-1:]])
        out = []
        for i in range(1, len(q) - 2):
            p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
            for t in np.linspace(0, 1, n, endpoint=False):
                out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                                  + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
        return np.array(out)

    spine = catmull(pts)
    dl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(spine, axis=0), axis=1))]
    step = 30 * Z
    marks = []
    for dd in np.arange(step, dl[-1], step):
        i = min(int(np.searchsorted(dl, dd)), len(spine) - 2)
        t = spine[i + 1] - spine[i - 1 if i else 0]
        t = t / (np.linalg.norm(t) + 1e-6)
        marks.append((spine[i], np.array([-t[1], t[0]]), dd / dl[-1]))

    canvas = np.full((H * Z, W * Z, 3), 255, np.uint8)
    num = []
    info = {}
    for a in atts:
        kind = KIND.get(a["slot"], "fin")
        if only is not None and a["slot"] not in only and not (kind == "eye" and "P_tou" in only):
            continue
        if kind == "eye":
            px = ras(a)
            ys, xs = np.nonzero(px[..., 3] > 40)
            info["eye"] = (float(xs.mean()), float(ys.mean()))
            continue
        px = ras(a)
        m = biggest(smooth(px[..., 3] > 60, OPEN[kind]))
        if m.sum() < 30:
            continue
        col = {"body": "body", "head": "body", "beak": "beak", "brow": "brow", "horn": "horn", "web": "fin", "spar": "ray",
               "fin": "fin"}[kind]
        layer = np.zeros((H * Z, W * Z, 3), np.uint8)
        layer[:] = PAL[col]
        lines = Image.new("L", (W * Z, H * Z), 0)
        dr = ImageDraw.Draw(lines)
        if kind == "body":
            hsv = cv2.cvtColor(px[..., :3], cv2.COLOR_RGB2HSV)
            pale = (hsv[..., 2] > 150) & (hsv[..., 1] < 95) & (px[..., 3] > 60)
            pale = cv2.medianBlur(pale.astype(np.uint8) * 255, 2 * (4 * Z) + 1)
            pale = smooth(pale > 127, 9) & m
            layer[pale] = PAL["belly"]
            # ranh lưng / bụng
            edge = cv2.morphologyEx(pale.astype(np.uint8), cv2.MORPH_GRADIENT, el(1.2)) > 0
            # vạch bụng vuông góc với sống thân
            vl = Image.new("L", (W * Z, H * Z), 0)
            dv = ImageDraw.Draw(vl)
            near = cv2.dilate(m.astype(np.uint8), el(10)).astype(bool)
            front = a["slot"] in ("P_shenti01", "P_shenti02")
            for c, nrm, u in marks:
                if front != (u < 0.3):               # ngực, cổ chỉ lấy mốc của nửa trước (đuôi vòng ra sau cổ, kẻo vạch đan chéo)
                    continue
                cx, cy = int(c[0]), int(c[1])
                if not (0 <= cx < W * Z and 0 <= cy < H * Z and near[cy, cx]):
                    continue
                dv.line([tuple(c - nrm * 95 * Z), tuple(c + nrm * 95 * Z)], fill=255, width=int(2.2 * Z))
            vl = (np.asarray(vl) > 0) & pale
            layer[edge & m] = INK
            layer[vl] = INK
            if a["slot"] == "P_shenti03":            # chỗ đặt giáp lưng: vùng ngả lục của mảnh lưng → giáp vỏ sò của mình
                r, g, b = [px[..., i].astype(int) for i in range(3)]
                sad = (g > b - 2) & (g > r + 12) & (px[..., 3] > 60)
                print("giáp lưng: px ngả lục", int(sad.sum()))
                sad = biggest(smooth(cv2.medianBlur(sad.astype(np.uint8) * 255, 2 * (3 * Z) + 1) > 127, 6)) & m
                if sad.sum() > 200:
                    info["saddle"] = sad
        if kind in ("fin", "web"):                   # tia vây: theo các xương của mảnh
            used = set()
            for w in a.get("w", []):
                for k, wt in w:
                    if wt > 0.05:
                        used.add(k)
            for k in used:
                b = bones[k]
                nm = b["name"]
                if nm.startswith(("Q_", "H_", "weiba", "zhixin", "xy", "all", "root", "tou")) or b["len"] < 5:
                    continue
                p, q = seg(b)
                dr.line([tuple(p), tuple(q)], fill=255, width=int((5 if kind == "web" else 4) * Z))
            if kind == "web":
                mids = [bi[n] for n in (("R_chibang15", "R_chibang16", "R_chibang17") if a["slot"].endswith("R06")
                                        else ("L_chibang4", "L_chibang5", "L_chibang6"))]
                root = seg(mids[0])[0]
                tip = seg(mids[-1])[1]
                v = tip - root
                for ang in (-30, -20, -10, 10, 20, 30):
                    t = np.radians(ang)
                    u = np.array([v[0] * np.cos(t) - v[1] * np.sin(t), v[0] * np.sin(t) + v[1] * np.cos(t)]) * 1.15
                    dr.line([tuple(root), tuple(root + u)], fill=255, width=int(4 * Z))
            ray = (np.asarray(lines) > 0) & m
            layer[ray] = PAL["ray"]
            if kind == "web":
                info.setdefault("webs", []).append((a["slot"], m, used))
        ink = m & ~cv2.erode(m.astype(np.uint8), el(2.6)).astype(bool)
        layer[ink] = INK
        canvas[m] = layer[m]
        ys, xs = np.nonzero(m)
        num.append((a["order"], a["slot"][2:], float(xs.mean()), float(ys.mean())))
        info[a["slot"]] = m

    im = Image.fromarray(canvas)
    d = ImageDraw.Draw(im)

    # giáp vỏ sò trên lưng: ba vỏ sò điệp xếp chồng dọc theo vùng giáp
    if "saddle" in info:
        sad = info["saddle"]
        ys, xs = np.nonzero(sad)
        c = np.array([xs.mean(), ys.mean()])
        cov = np.cov(np.stack([xs, ys]))
        ev, evec = np.linalg.eigh(cov)
        ax = evec[:, 1] * np.sign(evec[0, 1] or 1)
        L = 2.0 * np.sqrt(ev[1])
        Wd = 2.0 * np.sqrt(ev[0])
        up = np.array([ax[1], -ax[0]])
        if up[1] > 0:
            up = -up
        for k, f in enumerate((-0.62, 0.0, 0.62)):
            base = c + ax * L * f - up * Wd * 0.55
            R = max(L * 0.42, Wd * 1.05)
            fan = [tuple(base)]
            a0 = np.arctan2(up[1], up[0])
            for t in np.linspace(-1.15, 1.15, 13):
                fan.append(tuple(base + R * np.array([np.cos(a0 + t), np.sin(a0 + t)]) * (1 + 0.05 * np.cos(t * 12))))
            d.polygon(fan, fill=PAL["shell"], outline=INK, width=int(2.6 * Z))
            for t in np.linspace(-0.8, 0.8, 5):
                d.line([tuple(base + R * 0.2 * np.array([np.cos(a0 + t), np.sin(a0 + t)])),
                        tuple(base + R * 0.93 * np.array([np.cos(a0 + t), np.sin(a0 + t)]))], fill=PAL["rib"], width=int(2.4 * Z))

    # đốm kem trên màng cánh: ba đốm nhỏ dần dọc tia giữa
    for slot, m, used in info.get("webs", []):
        names = sorted([bones[k]["name"] for k in used if bones[k]["name"].split("chibang")[-1].isdigit()],
                       key=lambda n: int(n.split("chibang")[-1]))
        mid = [n for n in names if n in ("R_chibang16", "R_chibang17", "L_chibang5", "L_chibang6")]
        for j, n in enumerate(mid):
            p, q = seg(bi[n])
            for f, r in ((0.45, 15 - 3 * j),):
                c = p + (q - p) * f + np.array([0, 0])
                nrm = np.array([-(q - p)[1], (q - p)[0]]) / (np.linalg.norm(q - p) + 1e-6)
                c = c + nrm * 26 * Z * (1 if slot.endswith("R06") else -1)
                if m[int(c[1]), int(c[0])]:
                    d.ellipse([c[0] - r * Z, c[1] - r * Z, c[0] + r * Z, c[1] + r * Z], fill=PAL["spot"], outline=INK, width=int(2 * Z))

    # mắt: to, hổ phách, con ngươi dọc, một chấm sáng
    if "eye" in info:
        ex, ey = info["eye"]
        rx, ry = 21 * Z, 13 * Z
        d.ellipse([ex - rx, ey - ry, ex + rx, ey + ry], fill=PAL["eye"], outline=INK, width=int(2.6 * Z))
        d.ellipse([ex - 4 * Z, ey - ry + 2 * Z, ex + 4 * Z, ey + ry - 2 * Z], fill=INK)
        d.ellipse([ex + 5 * Z, ey - 8 * Z, ex + 10 * Z, ey - 3 * Z], fill=(255, 255, 255))

    small = im.resize((W, H), Image.LANCZOS)
    masks = {k: cv2.resize(v.astype(np.uint8) * 255, (W, H), interpolation=cv2.INTER_AREA) > 127
             for k, v in info.items() if k.startswith("P_")}
    order = {"P_" + n: o for o, n, _, _ in num}
    if luu:
        out = os.path.join(HERE, "inbox", f"{CODE}_1", "mau")
        os.makedirs(out, exist_ok=True)
        small.save(os.path.join(out, "bo_cuc.png"))
        so = small.copy()
        ds = ImageDraw.Draw(so)
        F = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)
        for o, n, x, y in num:
            ds.text((x / Z - 14, y / Z - 6), f"{o}:{n}", fill=(255, 255, 255), font=F, stroke_width=2, stroke_fill=(0, 0, 0))
        so.save(os.path.join(out, "bo_cuc_so.png"))
        print(os.path.join(out, "bo_cuc.png"))
    return small, masks, order


if __name__ == "__main__":
    dung()
