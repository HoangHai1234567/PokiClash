# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của golem lõi lửa (golem_lua, tướng thứ 4 đảo Hỏa): khối từng part của rig monster_3422 ở khung 0 idle_01, tô
phẳng theo màu của THIẾT KẾ MÌNH. Mọi GAI ĐỎ của con gốc thành LƯỠI LỬA phụt ra từ lỗ trên người (vẽ bằng mã theo đúng trục của gai:
gốc ở chân gai, ngọn theo hướng mũi gai, dài hơn gai); khối cầu đỏ giữa ngực thành LÕI LỬA (vòng màu đồng tâm), hai khớp gối đỏ thành
khớp dung nham, lòng miệng thành họng lửa. Các tấm đá (đầu, mày, lưng, vai, thân, hông, chân, hai bàn tay) giữ đúng chỗ, cỡ, thứ tự
chồng của rig; không mang nét, hoa văn, màu của con gốc. Chỉ để GPT lấy chỗ đặt, cỡ, thứ tự chồng.

Người dùng (2026-11-13): "concept như trong hình, kiểu golem đi bằng 2 chân có lõi lửa, lửa thoát ra từ các lỗ trên người (gai đỏ đổi
thành lửa)". Ba hướng chất liệu dưới đây là ĐỀ XUẤT của Claude (tránh tông đã dùng ở đảo Hỏa: đá nâu đỏ gạch của quy_lava, đá vỏ chai đen
tím của mat_lua, giáp cháy đen của cung_lua):
  da_tro   đá tro núi lửa xám kem, mảng phụ than chì
  sat_lo   sắt lò rèn xám xanh, mảng phụ đồng thau
  da_cat   đá sa thạch vàng cát, mảng phụ nâu than

    golem_lua_bo_cuc.py [hướng|all]   → inbox/golem_lua_1/mau/bo_cuc_<hướng>.png (+ bo_cuc.json, _luoi_<hướng>.png)
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import golem_lua as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
S2 = 2
INK = (43, 33, 24)
ATT = "att_idle0.json"

LUA = ((224, 68, 31), (247, 144, 42), (255, 212, 90))          # lửa: ngoài → trong
HUONG = {
    "da_tro": dict(da=(178, 167, 154), phu=(63, 59, 70), vuot=(46, 42, 48), ranh=(146, 136, 124)),
    "sat_lo": dict(da=(92, 97, 108), phu=(181, 116, 56), vuot=(44, 45, 51), ranh=(70, 74, 84), dinh=True),
    "da_cat": dict(da=(201, 174, 132), phu=(74, 58, 54), vuot=(46, 38, 34), ranh=(168, 142, 104)),
}

# vai trò từng slot (khung 0 idle). "lua": gai → lưỡi lửa; "x+lua": mảnh ghép có gai đỏ trên đó (phần gai → lửa, phần còn lại x).
VAI = {
    "P_yuanzhui2": "lua", "P_tuiiL2": "khop", "P_tuiiL3": "da", "P_tuiiL1": "da",
    "P_kua4": "da", "P_kua3": "da+lua", "P_kua2": "da", "P_kua1": "da",
    "P_tuiiR3": "da", "P_tuiiR2": "khop", "P_tuiiR1": "da",
    "P_shouL3": "phu", "P_shouL4": "da", "P_shouzhiL5": "vuot", "P_shouzhiL6": "vuot", "P_shouzhiL4": "vuot",
    "P_yuanzhui1": "lua", "P_tiekuai4": "phu", "P_xiongjia6": "da",
    "P_xiongqiang3": "loi", "P_qiu2": "tam", "P_xiongqiang4": "da", "P_tiekuai3": "phu", "P_xiongjia5": "da",
    "P_kouqiang3": "mieng", "P_tou3": "da", "P_jiao3": "lua", "P_zuiiba3": "phu", "P_jianci13": "lua",
    "P_toujia11": "da", "P_toujia10": "da", "P_dise": "phu", "P_jianci17": "lo", "P_jianci16": "lua", "P_jianci15": "phu",
    "P_jianci14": "lua", "P_toujia9": "da", "P_toujia8": "da", "P_yanjing3": "mat", "P_toujia6": "da",
    "P_jianci11": "lo", "P_jianci9": "lua", "P_jianci10": "phu", "P_jiapian2": "da",
    "P_shouR1": "phu+lua", "P_shouR2": "da", "P_shouzhiR3": "vuot", "P_shouzhiR2": "vuot", "P_shouzhiR1": "vuot",
}
# độ dài lưỡi lửa so với gai, độ rộng gốc so với gai (theo slot)
LUA_DAI = {"P_jianci9": 1.55, "P_jianci16": 1.75, "P_jiao3": 1.35, "P_jianci13": 1.7, "P_jianci14": 1.7,
           "P_yuanzhui1": 1.6, "P_yuanzhui2": 1.5, "P_kua3": 1.4, "P_shouR1": 1.7}
# gai dò ngược chiều (chân gai có đế tròn rộng hơn mũi không rõ) → lật hướng
LAT = {"P_shouR1"}
# nhóm để ghi toạ độ trong prompt
NHOM = {
    "loi": ["P_xiongqiang3", "P_qiu2"], "vo_nguc": ["P_xiongqiang4"],
    "dau": ["P_tou3"], "ham": ["P_zuiiba3"], "mieng": ["P_kouqiang3"], "mat": ["P_yanjing3"],
    "may": ["P_toujia8"], "may2": ["P_jiapian2"], "dinh_dau": ["P_toujia9"], "lung": ["P_toujia10"],
    "vai_gan": ["P_toujia6"], "vai_gan_sau": ["P_toujia11"], "vong_vai": ["P_jianci10", "P_jianci11"],
    "nguc_trai": ["P_xiongjia5"], "nguc_phai": ["P_xiongjia6"],
    "tay_gan": ["P_shouR1", "P_shouR2", "P_shouzhiR1", "P_shouzhiR2", "P_shouzhiR3"],
    "tay_xa": ["P_shouL3", "P_shouL4", "P_shouzhiL4", "P_shouzhiL5", "P_shouzhiL6"],
    "chan_gan": ["P_tuiiR1", "P_tuiiR2", "P_tuiiR3"], "chan_xa": ["P_tuiiL1", "P_tuiiL2", "P_tuiiL3"],
    "hong": ["P_kua1", "P_kua2", "P_kua3", "P_kua4"],
}
# rãnh khắc đơn giản (toạ độ chuẩn hoá trong khung của mảnh) — chi tiết của MÌNH, mật độ như con gốc (vài tấm có một rãnh)
RANH = {
    "P_toujia8": [[(0.30, 0.22), (0.62, 0.30), (0.52, 0.62)]],
    "P_jiapian2": [[(0.18, 0.30), (0.55, 0.55), (0.80, 0.62)]],
    "P_shouR2": [[(0.30, 0.30), (0.55, 0.42), (0.62, 0.62)]],
    "P_shouL4": [[(0.35, 0.35), (0.58, 0.50)]],
    "P_toujia10": [[(0.25, 0.62), (0.55, 0.70)]],
}


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def vien(m, r):
    return m & ~cv2.erode(m.astype(np.uint8), el(r)).astype(bool)


def khung_T():
    _, _, atts = G.nap(ATT)
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts if a["slot"] in VAI])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    SC = min((W - 420) / (x1 - x0), (H - 300) / (y1 - y0))
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = H - 80 + y0 * SC
    return SC, (lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1))


def lop(a, T):
    """ảnh gốc của part dán lên canvas (S2): trả (alpha, rgb) — chỉ dùng để tách vùng gai đỏ trong mảnh ghép."""
    src = G.part_goc(a)
    uv, tr = G.luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2))
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, src.convert("RGBa"), V * S2, uv, tr)
    A = np.asarray(lay.convert("RGBA"))
    return A[..., 3], A[..., :3].astype(np.int32)


def bong(al, tron=3.0):
    m = (al > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(3))
    return cv2.GaussianBlur(m * 255, (0, 0), tron) > 127


def do_gai(m):
    """gai (hình nón): tâm chân gai, hướng chân → mũi, dài, rộng chân."""
    ys, xs = np.nonzero(m)
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0)
    u, s, vt = np.linalg.svd(P - c, full_matrices=False)
    d = vt[0]
    t = (P - c) @ d
    n = (P - c) @ np.array([-d[1], d[0]])
    lo, hi = t.min(), t.max()
    L = hi - lo
    w_lo = np.ptp(n[t < lo + 0.22 * L]) if (t < lo + 0.22 * L).sum() > 3 else 0
    w_hi = np.ptp(n[t > hi - 0.22 * L]) if (t > hi - 0.22 * L).sum() > 3 else 0
    if w_lo < w_hi:                       # chân gai là đầu RỘNG
        d, t = -d, -t
        lo, hi = -hi, -lo
    base = c + d * lo
    return base, d, L, max(w_lo, w_hi)


def luoi_lua(base, d, L, w, seed=0):
    """lưỡi lửa: gốc dày tròn ở chân gai, thân uốn chữ S theo hướng gai, ngọn nhọn hơi móc lên và về sau (sang trái: con nhìn phải),
    thêm một lưỡi phụ nhỏ ở một bên. Trả danh sách đa giác."""
    rng = np.random.default_rng(seed)
    up = np.array([-0.55, -1.0])
    up /= np.linalg.norm(up)
    perp = np.array([-d[1], d[0]])
    ts = np.linspace(0, 1, 70)
    mix = np.clip(ts - 0.35, 0, None) / 0.65 * 0.45
    dirs = d[None] * (1 - mix[:, None]) + up[None] * mix[:, None]
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    sp = base[None] + np.cumsum(dirs * (L / len(ts)), 0) - d[None] * w * 0.25
    sp += perp[None] * (0.08 * L * np.sin(ts * math.pi * 1.7 + rng.uniform(0, 1)))[:, None]
    wd = w * 0.62 * (1 - ts) ** 0.85 * (1 + 0.28 * np.sin(ts * math.pi))
    dx, dy = np.gradient(sp[:, 0]), np.gradient(sp[:, 1])
    nn = np.hypot(dx, dy) + 1e-6
    nx, ny = -dy / nn, dx / nn
    A = np.stack([sp[:, 0] + nx * wd, sp[:, 1] + ny * wd], 1)
    B = np.stack([sp[:, 0] - nx * wd, sp[:, 1] - ny * wd], 1)
    polys = [np.concatenate([A, B[::-1]], 0)]
    # lưỡi phụ: mọc ở 35–45% thân, ngả ra một bên, dài 0,38
    k = int(len(ts) * rng.uniform(0.32, 0.42))
    sgn = 1 if rng.uniform() < 0.5 else -1
    b2 = sp[k] + np.array([nx[k], ny[k]]) * wd[k] * 0.55 * sgn
    d2 = dirs[k] * 0.7 + np.array([nx[k], ny[k]]) * 0.7 * sgn
    d2 /= np.linalg.norm(d2)
    L2 = L * 0.38
    t2 = np.linspace(0, 1, 30)
    m2 = t2 * 0.5
    dd2 = d2[None] * (1 - m2[:, None]) + up[None] * m2[:, None]
    dd2 /= np.linalg.norm(dd2, axis=1, keepdims=True)
    s2 = b2[None] + np.cumsum(dd2 * (L2 / len(t2)), 0)
    w2 = wd[k] * 0.55 * (1 - t2) ** 0.9
    gx, gy = np.gradient(s2[:, 0]), np.gradient(s2[:, 1])
    g2 = np.hypot(gx, gy) + 1e-6
    A2 = np.stack([s2[:, 0] - gy / g2 * w2, s2[:, 1] + gx / g2 * w2], 1)
    B2 = np.stack([s2[:, 0] + gy / g2 * w2, s2[:, 1] - gx / g2 * w2], 1)
    polys.append(np.concatenate([A2, B2[::-1]], 0))
    return polys


def to_lua(can, m):
    can[m] = LUA[0]
    giua = cv2.erode(m.astype(np.uint8), el(9 * S2)).astype(bool)
    loi = cv2.erode(m.astype(np.uint8), el(19 * S2)).astype(bool)
    can[giua] = LUA[1]
    can[loi] = LUA[2]
    can[vien(m, 3 * S2)] = INK


def ve(huong):
    C = HUONG[huong]
    SC, T = khung_T()
    G._C.pop("att", None)
    _, _, atts = G.nap(ATT)
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop, info = {}, {"lua": {}}
    for i, a in enumerate(atts):
        v = VAI.get(a["slot"])
        if not v:
            continue
        al, rgb = lop(a, T)
        m = bong(al, 1.6 if v in ("mat", "tam", "khop") else 4.0)
        if not m.any():
            continue
        ys, xs = np.nonzero(m)
        b = [xs.min() / S2, ys.min() / S2, xs.max() / S2, ys.max() / S2]
        info.setdefault("slot", {})[a["slot"]] = [round(x) for x in b]
        for ten, sl in NHOM.items():
            if a["slot"] in sl:
                h = hop.get(ten)
                hop[ten] = b if h is None else [min(h[0], b[0]), min(h[1], b[1]), max(h[2], b[2]), max(h[3], b[3])]
        nen, co_lua = v.split("+")[0], v.endswith("lua")
        mg = None
        if co_lua:
            if v == "lua":
                mg = m
            else:   # vùng gai đỏ trong mảnh ghép
                red = (al > 110) & (rgb[..., 0] > 140) & (rgb[..., 0] - rgb[..., 1] > 70) & (rgb[..., 0] - rgb[..., 2] > 60)
                n, lab, st, _ = cv2.connectedComponentsWithStats(red.astype(np.uint8))
                if n > 1:
                    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
                    mg = cv2.dilate((lab == k).astype(np.uint8), el(2 * S2)).astype(bool)
            if mg is not None and nen != "lua":
                m = m & ~mg
        if nen in ("da", "phu"):
            mau = C[nen]
            can[m] = mau
            if C.get("dinh") and nen == "da" and m.sum() > 9000 * S2 * S2:
                inn = cv2.erode(m.astype(np.uint8), el(18 * S2)).astype(bool)
                iy, ix = np.nonzero(inn)
                for k in range(0, len(ix), max(1, len(ix) // 3))[:3]:
                    cv2.circle(can, (int(ix[k]), int(iy[k])), 5 * S2, C["phu"], -1)
                    cv2.circle(can, (int(ix[k]), int(iy[k])), 5 * S2, INK, 2 * S2)
            can[vien(m, 3 * S2)] = INK
            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max(), ys.max()
            for ln in RANH.get(a["slot"], []):
                P = np.array([(x0 + (x1 - x0) * u, y0 + (y1 - y0) * w) for u, w in ln], np.int32)
                cv2.polylines(can, [P], False, C["ranh"] if nen == "da" else INK, 6 * S2, cv2.LINE_AA)
                cv2.polylines(can, [P], False, INK, 2 * S2, cv2.LINE_AA)
        elif nen == "vuot":
            can[m] = C["vuot"]
            can[vien(m, 3 * S2)] = INK
        elif nen == "lo":
            can[m] = (36, 26, 24)
            inn = cv2.erode(m.astype(np.uint8), el(6 * S2)).astype(bool)
            can[inn] = LUA[1]
            can[vien(m, 3 * S2)] = INK
        elif nen in ("khop", "tam"):
            can[m] = LUA[0] if nen == "khop" else LUA[1]
            inn = cv2.erode(m.astype(np.uint8), el((6 if nen == "khop" else 7) * S2)).astype(bool)
            can[inn] = LUA[1] if nen == "khop" else LUA[2]
            can[vien(m, 3 * S2)] = INK
        elif nen == "loi":
            cx, cy = xs.mean(), ys.mean()
            R = (xs.max() - xs.min() + ys.max() - ys.min()) / 4
            yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
            # vòng lửa đồng tâm lệch về tâm cầu nhỏ (P_qiu2), ranh uốn như lưỡi lửa
            q = [x for x in atts if x["slot"] == "P_qiu2"][0]
            qx, qy = T(np.array(q["xy"], float).reshape(-1, 2)).mean(0) * S2
            ang = np.arctan2(yy - qy, xx - qx)
            dd = np.hypot(xx - qx, yy - qy) * (1 + 0.07 * np.sin(ang * 7))
            can[m] = LUA[0]
            can[m & (dd < R * 1.05)] = LUA[1]
            can[m & (dd < R * 0.55)] = LUA[2]
            can[vien(m, 3 * S2)] = INK
            hop["loi_tam"] = [round(qx / S2), round(qy / S2), round(R / S2)]
        elif nen == "mieng":
            can[m] = LUA[0]
            inn = cv2.erode(m.astype(np.uint8), el(10 * S2)).astype(bool)
            can[inn] = LUA[1]
            can[vien(m, 3 * S2)] = INK
        elif nen == "mat":
            ex, ey = xs.mean(), ys.mean()
            er = (xs.max() - xs.min() + ys.max() - ys.min()) / 4 * 1.1
            cv2.circle(can, (int(ex), int(ey)), int(er), C["phu"] if huong != "sat_lo" else (40, 36, 40), -1, cv2.LINE_AA)
            cv2.circle(can, (int(ex), int(ey)), int(er), INK, 3 * S2, cv2.LINE_AA)
            cv2.circle(can, (int(ex), int(ey)), int(er * 0.62), LUA[2], -1, cv2.LINE_AA)
            cv2.circle(can, (int(ex), int(ey)), int(er * 0.62), INK, 2 * S2, cv2.LINE_AA)
            hop["mat_tam"] = [round(ex / S2), round(ey / S2), round(er / S2)]
        if mg is not None and mg.any():
            base, d, L, w = do_gai(mg)
            if a["slot"] in LAT:
                base, d = base + d * L, -d
            k = LUA_DAI.get(a["slot"], 1.5)
            ml = np.zeros(m.shape, np.uint8)
            for P in luoi_lua(base, d, L * k, w * 1.05, seed=i):
                cv2.fillPoly(ml, [P.astype(np.int32)], 1)
            ml = cv2.GaussianBlur(ml.astype(np.float32), (0, 0), 2 * S2) > 0.5
            to_lua(can, ml)
            ys2, xs2 = np.nonzero(ml)
            tip = base + d * L * k
            info["lua"][a["slot"]] = dict(goc=[round(base[0] / S2), round(base[1] / S2)], ngon=[round(tip[0] / S2), round(tip[1] / S2)],
                                          hop=[round(xs2.min() / S2), round(ys2.min() / S2), round(xs2.max() / S2), round(ys2.max() / S2)])
    im = Image.fromarray(can, "RGB").resize((W, H), Image.LANCZOS)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, f"bo_cuc_{huong}.png")
    im.save(p)
    out = {k: [round(x) for x in v] for k, v in hop.items()}
    out.update(info)
    allb = np.array([v for v in info["slot"].values()] + [v["hop"] for v in info["lua"].values()])
    out["_khung"] = [int(allb[:, 0].min()), int(allb[:, 1].min()), int(allb[:, 2].max()), int(allb[:, 3].max())]
    out["_sc"] = round(SC, 4)
    json.dump(out, open(os.path.join(G.MAU, "bo_cuc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(p, "tỉ lệ", round(SC, 3), "khung", out["_khung"])
    g = im.copy()
    d = ImageDraw.Draw(g)
    F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    for x in range(0, W, 50):
        d.line([(x, 0), (x, H)], fill=(0, 0, 0) if x % 100 == 0 else (170, 170, 170), width=1)
        if x % 100 == 0:
            d.text((x + 2, 2), str(x), fill=(200, 0, 0), font=F)
    for y in range(0, H, 50):
        d.line([(0, y), (W, y)], fill=(0, 0, 0) if y % 100 == 0 else (170, 170, 170), width=1)
        if y % 100 == 0:
            d.text((2, y + 2), str(y), fill=(200, 0, 0), font=F)
    g.save(os.path.join(G.MAU, f"_luoi_{huong}.png"))


if __name__ == "__main__":
    hs = sys.argv[1] if len(sys.argv) > 1 else "all"
    for h in (HUONG if hs == "all" else [hs]):
        ve(h)
