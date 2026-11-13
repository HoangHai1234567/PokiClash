# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của mắt lửa bọc giáp (mat_lua, tướng thứ 2 đảo Hỏa): khối từng part của rig monster_3342 ở khung 0 idle_01, tô
phẳng theo màu của THIẾT KẾ MÌNH. Quả cầu giữa (shenti_01) thành NHÃN CẦU LỬA: một quả cầu lửa ba lớp màu, tròng vàng trắng quanh con
ngươi dọc (yanjing_01), lưỡi lửa liếm ra ở các khe giữa các tấm giáp (lớp lửa thêm, nằm sau quả cầu). Các tấm giáp lơ lửng (đầu, vai,
dưới thân) và hai nắm tay giữ đúng chỗ, cỡ, thứ tự chồng của rig. Chỉ để GPT lấy chỗ đặt, cỡ, thứ tự chồng; không mang nét, màu của
con gốc.

Người dùng (2026-11-13): "concept flaming fire eyeball có tay chân và bọc giáp". Ba hướng giáp dưới đây là ĐỀ XUẤT của Claude:
  da_den    giáp đá vỏ chai (obsidian) đen tím, vết nứt dung nham mảnh; cầu lửa đỏ cam
  sat_ren   giáp sắt rèn xám than có đinh tán, mép nung cam; cầu lửa cam vàng
  tro_nui   giáp đá bọt xám tro sáng, vết nứt cam; cầu lửa đỏ cam (tương phản mạnh)

    mat_lua_bo_cuc.py [hướng|all]   → inbox/mat_lua_1/mau/bo_cuc_<hướng>.png (+ bo_cuc.json khung từng nhóm, _luoi_<hướng>.png)
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
import mat_lua as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
S2 = 2
INK = (43, 33, 24)
ATT = "att_idle0.json"

LUA_DO = ((220, 58, 34), (244, 128, 34), (255, 206, 80))      # ngoài → trong
LUA_VANG = ((236, 92, 30), (252, 160, 40), (255, 222, 110))
HUONG = {
    "da_den": dict(giap=(52, 46, 60), giap2=(40, 35, 46), nut=(238, 90, 46), lua=LUA_DO, trong=(255, 236, 160), nguoi=(150, 24, 30),
                   tay=(232, 84, 44)),
    "sat_ren": dict(giap=(84, 86, 92), giap2=(62, 64, 70), nut=(250, 140, 46), lua=LUA_VANG, trong=(255, 244, 190), nguoi=(46, 30, 30),
                    tay=(246, 128, 40), dinh=True),
    "tro_nui": dict(giap=(150, 144, 140), giap2=(118, 112, 110), nut=(246, 104, 38), lua=LUA_DO, trong=(255, 234, 150), nguoi=(140, 22, 28),
                    tay=(232, 84, 44)),
}

VAI = {
    "shenti_01": "cau", "yanjing_01": "mat",
    "tou_01": "giap", "tou_02": "giap", "tou_03": "giap",
    "jian_02": "giap", "jian_03": "giap",
    "shitou_01": "giap", "shitou_03": "giap", "shitou_04": "giap",
    "shou_01": "nam", "shou_02": "nam",
    "shoubi_01": "tay", "shoubi_02": "tay",
}
NHOM = {
    "cau": ["shenti_01"], "mat": ["yanjing_01"],
    "mu": ["tou_01"], "giap_nho_mat": ["tou_02"], "giap_nho_phai": ["tou_03"],
    "vai_gan": ["jian_03"], "vai_xa": ["jian_02"],
    "giap_duoi_trai": ["shitou_01"], "giap_duoi_giua": ["shitou_04"], "giap_duoi_phai": ["shitou_03"],
    "nam_gan": ["shou_01"], "nam_xa": ["shou_02"], "tay_gan": ["shoubi_01"], "tay_xa": ["shoubi_02"],
}
# vết nứt / đường mép trên giáp (toạ độ chuẩn hoá trong khung của mảnh)
NUT = {
    "tou_01": [[(0.15, 0.30), (0.40, 0.42), (0.55, 0.36)], [(0.40, 0.42), (0.48, 0.62)]],
    "jian_03": [[(0.40, 0.15), (0.48, 0.45), (0.38, 0.70)]],
    "jian_02": [[(0.55, 0.15), (0.45, 0.50)]],
    "shou_01": [[(0.30, 0.30), (0.50, 0.50), (0.42, 0.78)], [(0.50, 0.50), (0.72, 0.58)]],
    "shou_02": [[(0.40, 0.30), (0.55, 0.60)]],
    "shitou_04": [[(0.20, 0.40), (0.45, 0.55), (0.70, 0.45)]],
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
    SC = min((W - 300) / (x1 - x0), (H - 300) / (y1 - y0))
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = H - 90 + y0 * SC
    return SC, (lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1))


def bong(a, T, tron=3.0):
    src = G.part_goc(a)
    al = np.asarray(src)[..., 3]
    one = Image.fromarray(np.dstack([np.full(al.shape + (3,), 255, np.uint8), np.where(al > 90, 255, 0).astype(np.uint8)]), "RGBA")
    uv, tr = G.luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2))
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, one.convert("RGBa"), V * S2, uv, tr)
    m = (np.asarray(lay)[..., 3] > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(3))
    return cv2.GaussianBlur(m * 255, (0, 0), tron) > 127


def luoi_lua(cx, cy, R, goc, dai, rong, cong=1.0):
    """một lưỡi lửa mọc từ quả cầu tâm (cx, cy) bán kính R theo hướng `goc` (độ, 0 = phải, 90 = lên): gốc dày tròn, uốn chữ S,
    ngọn nhọn quặp lên và về sau (sang trái: con nhìn phải), mép có một hai vết khuyết chữ C."""
    a = math.radians(goc)
    d = np.array([math.cos(a), -math.sin(a)])
    g = np.array([cx, cy]) + d * R * 0.70
    ts = np.linspace(0, 1, 60)
    L = dai * R
    up = np.array([-0.45, -1.0])
    up /= np.linalg.norm(up)
    sp = np.array([g + (d * (1 - t ** 1.3) + up * t ** 1.3) * L * t for t in ts])
    perp = np.array([-d[1], d[0]])
    sp += perp[None] * (0.12 * L * np.sin(ts * math.pi * 1.6) * cong)[:, None]
    wd = rong * R * 0.5 * (1 - ts) ** 0.9 * (1 + 0.25 * np.sin(ts * math.pi))
    dx, dy = np.gradient(sp[:, 0]), np.gradient(sp[:, 1])
    nn = np.hypot(dx, dy) + 1e-6
    nx, ny = -dy / nn, dx / nn
    A = np.stack([sp[:, 0] + nx * wd, sp[:, 1] + ny * wd], 1)
    B = np.stack([sp[:, 0] - nx * wd, sp[:, 1] - ny * wd], 1)
    tip = sp[-1] + up * L * 0.10 + np.array([-0.16 * L, 0.02 * L])
    return np.concatenate([A, tip[None], B[::-1]], 0)


# lưỡi lửa liếm ra từ các khe giáp: (góc, dài theo R, rộng theo R)
LUOI = [(176, 0.80, 0.66, 1), (146, 1.25, 0.82, -1), (116, 1.45, 0.86, 1), (88, 1.20, 0.74, -1), (58, 0.85, 0.60, 1), (30, 0.50, 0.46, -1), (206, 0.48, 0.50, 1)]


def ve(huong):
    C = HUONG[huong]
    SC, T = khung_T()
    G._C.pop("att", None)
    _, _, atts = G.nap(ATT)
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop = {}
    masks = {}
    for a in atts:
        if a["slot"] in VAI:
            masks[a["slot"]] = bong(a, T, 1.8 if VAI[a["slot"]] == "mat" else 6.0)
    # quả cầu: tâm, bán kính
    mc = masks["shenti_01"]
    ys, xs = np.nonzero(mc)
    cx, cy = xs.mean(), ys.mean()
    R = (xs.max() - xs.min() + ys.max() - ys.min()) / 4
    # lớp lửa sau cùng
    lua = np.zeros(mc.shape, np.uint8)
    for g_, d_, r_, c_ in LUOI:
        cv2.fillPoly(lua, [luoi_lua(cx, cy, R, g_, d_, r_, c_).astype(np.int32)], 1)
    cv2.circle(lua, (int(cx), int(cy)), int(R * 1.12), 1, -1)   # gốc lửa liền một khối quanh quả cầu
    lua = (cv2.GaussianBlur(lua.astype(np.float32), (0, 0), 3 * S2) > 0.5) & ~cv2.erode(mc.astype(np.uint8), el(6 * S2)).astype(bool)
    giua = cv2.erode(lua.astype(np.uint8), el(22 * S2)).astype(bool)
    loi = cv2.erode(lua.astype(np.uint8), el(44 * S2)).astype(bool)
    can[lua] = C["lua"][0]
    can[giua] = C["lua"][1]
    can[loi] = C["lua"][2]
    can[vien(lua, 3 * S2)] = INK
    ys2, xs2 = np.nonzero(lua)
    hop["lua"] = [xs2.min() / S2, ys2.min() / S2, xs2.max() / S2, ys2.max() / S2]
    for a in atts:
        v = VAI.get(a["slot"])
        if not v:
            continue
        m = masks[a["slot"]]
        if not m.any():
            continue
        ys, xs = np.nonzero(m)
        b = [xs.min() / S2, ys.min() / S2, xs.max() / S2, ys.max() / S2]
        for ten, sl in NHOM.items():
            if a["slot"] in sl:
                h = hop.get(ten)
                hop[ten] = b if h is None else [min(h[0], b[0]), min(h[1], b[1]), max(h[2], b[2]), max(h[3], b[3])]
        if v == "cau":
            # cầu lửa: ba vòng đồng tâm lệch về phía mắt (phải)
            mx, my = masks["yanjing_01"].nonzero()[1].mean(), masks["yanjing_01"].nonzero()[0].mean()
            yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
            dd = np.hypot(xx - mx, yy - my)
            can[m] = C["lua"][0]
            can[m & (dd < R * 1.05)] = C["lua"][1]
            can[m & (dd < R * 0.62)] = C["lua"][2]
            can[vien(m, 3 * S2)] = INK
            hop["cau_tam"] = [round(cx / S2), round(cy / S2), round(R / S2)]
            continue
        if v == "mat":
            ex, ey = xs.mean(), ys.mean()
            er = (xs.max() - xs.min() + ys.max() - ys.min()) / 4 * 1.15
            cv2.circle(can, (int(ex), int(ey)), int(er), C["trong"], -1, cv2.LINE_AA)
            cv2.circle(can, (int(ex), int(ey)), int(er), INK, 3 * S2, cv2.LINE_AA)
            # con ngươi dọc (khe)
            cv2.ellipse(can, (int(ex), int(ey)), (int(er * 0.26), int(er * 0.78)), 0, 0, 360, C["nguoi"], -1, cv2.LINE_AA)
            cv2.ellipse(can, (int(ex), int(ey)), (int(er * 0.26), int(er * 0.78)), 0, 0, 360, INK, 2 * S2, cv2.LINE_AA)
            hop["mat"] = [round((ex - er) / S2), round((ey - er) / S2), round((ex + er) / S2), round((ey + er) / S2)]
            continue
        if v == "tay":
            can[m] = C["tay"]
            can[vien(m, 3 * S2)] = INK
            continue
        can[m] = C["giap"]
        can[vien(m, 3 * S2)] = INK
        # mặt vát: dải sẫm dọc mép dưới-phải (chỉ là đường mép tấm giáp, phẳng)
        x0, y0, x1, y1 = xs.min(), ys.min(), xs.max(), ys.max()
        for ln in NUT.get(a["slot"], []):
            P = np.array([(x0 + (x1 - x0) * u, y0 + (y1 - y0) * w) for u, w in ln], np.int32)
            if C.get("dinh"):
                cv2.polylines(can, [P], False, INK, 3 * S2, cv2.LINE_AA)
            else:
                cv2.polylines(can, [P], False, INK, 7 * S2, cv2.LINE_AA)
                cv2.polylines(can, [P], False, C["nut"], 3 * S2, cv2.LINE_AA)
        if C.get("dinh"):
            # mép nung cam dọc viền trong + đinh tán
            band = vien(m, 9 * S2) & ~vien(m, 4 * S2)
            can[band] = C["nut"]
            inn = cv2.erode(m.astype(np.uint8), el(16 * S2)).astype(bool)
            iy, ix = np.nonzero(inn)
            if len(ix):
                for k in range(0, len(ix), max(1, len(ix) // 4)):
                    cv2.circle(can, (int(ix[k]), int(iy[k])), 5 * S2, C["giap2"], -1)
                    cv2.circle(can, (int(ix[k]), int(iy[k])), 5 * S2, INK, 2 * S2)
    im = Image.fromarray(can, "RGB").resize((W, H), Image.LANCZOS)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, f"bo_cuc_{huong}.png")
    im.save(p)
    hop = {k: [round(x) for x in v] for k, v in hop.items()}
    hop["_sc"] = round(SC, 4)
    json.dump(hop, open(os.path.join(G.MAU, "bo_cuc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(p, "tỉ lệ", round(SC, 3))
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
