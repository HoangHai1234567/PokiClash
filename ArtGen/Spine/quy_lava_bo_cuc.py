# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của tiểu quỷ lava (quy_lava, tướng đầu tiên đảo Hỏa): khối từng part của rig monster_3336 ở khung 0 idle_01, tô phẳng
theo màu của THIẾT KẾ MÌNH. Tóc của con gốc (chùm gai vàng) thay bằng NGỌN LỬA vẽ bằng mã (người dùng 2026-11-13: "phần tóc lửa tôi
muốn bạn cải thiện thêm cho giống ngọn lửa thật hơn"): mấy lưỡi lửa gốc dày uốn chữ S, ngọn móc ngả ra sau, ba lớp màu (đỏ cam ngoài,
cam giữa, vàng lõi ở gốc). Chỉ để GPT lấy chỗ đặt, cỡ, thứ tự chồng; không mang nét, hoa văn, màu của con gốc.

Ba hướng màu ĐỀ XUẤT của Claude (2026-11-13), chờ người dùng chọn:
  than_tim  đá than tím (sát con gốc): thân tím than, đá sẫm, vết nứt dung nham đỏ cam
  da_nung   đá đỏ nung: thân nâu đỏ bazan, đá đen nâu, vết nứt cam vàng
  tro_nui   tro núi lửa: thân xám tro sáng, đá than, vết nứt cam

    quy_lava_bo_cuc.py [hướng|all]   → inbox/quy_lava_1/mau/bo_cuc_<hướng>.png (+ bo_cuc.json khung từng nhóm, _luoi_<hướng>.png)
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
import quy_lava as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
S2 = 2
INK = (43, 33, 24)
ATT = "att_idle0.json"

HUONG = {
    "than_tim": dict(than=(92, 80, 108), da=(56, 50, 62), sung=(56, 50, 62), khien=(70, 62, 76), nut=(236, 86, 48),
                     luoi=(238, 92, 56), luoi_vien=(255, 196, 92), mat=(255, 214, 96),
                     lua=((222, 62, 36), (244, 136, 36), (255, 214, 82))),
    "da_nung": dict(than=(124, 66, 56), da=(58, 40, 40), sung=(58, 40, 40), khien=(74, 50, 46), nut=(255, 160, 52),
                    luoi=(250, 132, 44), luoi_vien=(255, 214, 96), mat=(255, 222, 110),
                    lua=((222, 62, 36), (244, 136, 36), (255, 214, 82))),
    "tro_nui": dict(than=(150, 144, 140), da=(64, 60, 64), sung=(64, 60, 64), khien=(92, 86, 88), nut=(246, 112, 40),
                    luoi=(246, 112, 40), luoi_vien=(255, 200, 90), mat=(255, 210, 90),
                    lua=((222, 62, 36), (244, 136, 36), (255, 214, 82))),
}

# part của con gốc (tên slot) → vai trò trong thiết kế mình
VAI = {
    "xem_25": "than", "xem_23": "than", "xem_18": "than", "xem_16": "than", "xem_15": "than", "xem_11": "than",  # tay xa, chân, thân, đầu
    "xem_24": "khien", "xem_22": "nut",                                   # tấm khiên đá (tay xa) + vệt dung nham trên khiên
    "xem_17": "toc",                                                       # tóc → ngọn lửa (vẽ bằng mã)
    "xem_14": "da", "xem_13": "da", "xem_12": "da", "xem_9": "da", "xem_8": "da", "xem_6": "da",  # các khối đá dưới chân
    "xem_1": "sung", "xem_0": "sung",                                     # hai sừng
    "xem_4": "mat", "xem_3": "mat", "xem_2": "mieng",
    "xem_27": "da", "xem_28": "da", "xem_29": "da",                       # ba ngón đá của nắm tay xa (nắm cán khiên)
    "xem_10": "kiem",                                                      # lưỡi dung nham (tay gần)
    "xem_7": "da", "xem_5": "da",                                          # cánh tay đá gần + mảnh vai
}
NHOM = {  # khung nhóm ghi ra json để viết prompt
    "dau": ["xem_11"], "than": ["xem_16"], "tay_xa": ["xem_25", "xem_23"], "khien": ["xem_24"], "nam_xa": ["xem_27", "xem_28", "xem_29"],
    "sung_gan": ["xem_1"], "sung_xa": ["xem_0"], "mat_gan": ["xem_3"], "mat_xa": ["xem_4"], "mieng": ["xem_2"],
    "kiem": ["xem_10"], "tay_gan": ["xem_7"], "vai_gan": ["xem_5"],
    "chan": ["xem_18", "xem_15", "xem_14", "xem_13", "xem_12", "xem_9", "xem_8", "xem_6"], "toc_goc": ["xem_17"],
}
# vết nứt dung nham (toạ độ chuẩn hoá trong khung của mảnh, 0..1 từ trên-trái)
NUT = {
    "xem_7": [[(0.62, 0.15), (0.50, 0.42), (0.30, 0.62)], [(0.50, 0.42), (0.70, 0.66)], [(0.30, 0.62), (0.22, 0.86)]],
    "xem_1": [[(0.45, 0.10), (0.55, 0.45), (0.42, 0.80)]],
    "xem_0": [[(0.70, 0.12), (0.52, 0.48), (0.30, 0.78)]],
    "xem_16": [[(0.10, 0.62), (0.26, 0.70), (0.30, 0.88)], [(0.26, 0.70), (0.40, 0.66)]],
    "xem_24": [[(0.50, 0.08), (0.44, 0.40), (0.58, 0.62), (0.50, 0.92)], [(0.44, 0.40), (0.28, 0.52)]],
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
    # chừa phía trên cho ngọn lửa cao hơn tóc gốc
    SC = min((W - 260) / (x1 - x0), (H - 300) / (y1 - y0))
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = H - 70 + y0 * SC
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


def luoi_lua(base_l, base_r, cao, n=5, seed=3):
    """các lưỡi lửa mọc từ đoạn gốc (base_l → base_r, toạ độ canvas S2), vươn lên và ngả ra sau (sang TRÁI: con nhìn phải).
    Trả danh sách đa giác (mỗi lưỡi một đa giác) theo thứ tự vẽ sau → trước."""
    rng = np.random.default_rng(seed)
    bl, br = np.array(base_l, float), np.array(base_r, float)
    dai = np.linalg.norm(br - bl)
    out = []
    # chiều cao từng lưỡi: lưỡi giữa-sau cao nhất, hai đầu thấp
    hs = [0.58, 0.92, 1.0, 0.78, 0.52][:n]
    ws = [0.46, 0.52, 0.56, 0.48, 0.38][:n]
    for i in range(n):
        u = (i + 0.5) / n
        g = bl + (br - bl) * u                              # gốc lưỡi
        h = cao * hs[i]
        w = dai * ws[i]
        lean = -0.42 * h                                    # ngọn ngả về sau (trái)
        ts = np.linspace(0, 1, 40)
        # sống lưỡi: chữ S (cong ra trước ở giữa, quặp về sau ở ngọn)
        sx = g[0] + lean * ts ** 1.7 + 0.13 * h * np.sin(ts * math.pi) * (1 if i % 2 == 0 else 0.7)
        sy = g[1] - h * ts
        # bề ngang thon dần, ngọn móc
        wd = w * 0.5 * (1 - ts) ** 1.15 * (1 + 0.18 * np.sin(ts * math.pi * 2 + i))
        # pháp tuyến
        dx, dy = np.gradient(sx), np.gradient(sy)
        nn = np.hypot(dx, dy) + 1e-6
        nx, ny = -dy / nn, dx / nn
        L = np.stack([sx + nx * wd, sy + ny * wd], 1)
        R = np.stack([sx - nx * wd, sy - ny * wd], 1)
        # móc ở ngọn: điểm ngọn quặp thêm về sau và hơi xuống
        tip = np.array([sx[-1] - 0.20 * h, sy[-1] + 0.09 * h])
        poly = np.concatenate([L, tip[None], R[::-1]], 0)
        out.append(poly)
    return out


def ve(huong):
    C = HUONG[huong]
    SC, T = khung_T()
    G._C.pop("att", None)
    _, _, atts = G.nap(ATT)
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop = {}
    toc_m = None
    for a in atts:
        v = VAI.get(a["slot"])
        if not v:
            continue
        m = bong(a, T, 1.8 if v in ("nut", "mieng", "mat") else 3.0)
        if not m.any():
            continue
        ys, xs = np.nonzero(m)
        b = [xs.min() / S2, ys.min() / S2, xs.max() / S2, ys.max() / S2]
        for ten, sl in NHOM.items():
            if a["slot"] in sl:
                h = hop.get(ten)
                hop[ten] = b if h is None else [min(h[0], b[0]), min(h[1], b[1]), max(h[2], b[2]), max(h[3], b[3])]
        if v == "toc":
            toc_m = m
            ve_lua(can, m, C, hop)
            continue
        if v == "mieng":
            can[m] = INK
            continue
        if v == "kiem":
            # nửa sau (trên-trái, chỗ nắm) là cán đá sẫm, nửa trước (dưới-phải) là lưỡi dung nham có viền vàng
            pts = np.stack([xs, ys], 1).astype(float)
            c = pts.mean(0)
            U, Sv, Vt = np.linalg.svd(pts - c, full_matrices=False)
            ax = Vt[0] if Vt[0][0] > 0 else -Vt[0]
            t = (pts - c) @ ax
            t = (t - t.min()) / (t.max() - t.min())
            can[m] = C["luoi"]
            sel = t < 0.42
            mm = np.zeros_like(m)
            mm[ys[sel], xs[sel]] = True
            can[mm] = C["da"]
            # sống lưỡi màu sáng
            core = cv2.erode(m.astype(np.uint8), el(21 * S2)).astype(bool) & ~mm
            can[core] = C["luoi_vien"]
            can[vien(m, 3 * S2)] = INK
            can[vien(mm, 2 * S2) & cv2.erode(m.astype(np.uint8), el(3 * S2)).astype(bool)] = INK
            hop["kiem_goc"] = [round(float(pts[np.argmin(t)][0] / S2)), round(float(pts[np.argmin(t)][1] / S2))]
            hop["kiem_mui"] = [round(float(pts[np.argmax(t)][0] / S2)), round(float(pts[np.argmax(t)][1] / S2))]
            continue
        can[m] = C[v]
        if v != "nut":
            can[vien(m, (2 if v == "mat" else 3) * S2)] = INK
        for ln in NUT.get(a["slot"], []):
            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max(), ys.max()
            P = np.array([(x0 + (x1 - x0) * u, y0 + (y1 - y0) * w) for u, w in ln], np.int32)
            cv2.polylines(can, [P], False, INK, 7 * S2, cv2.LINE_AA)
            cv2.polylines(can, [P], False, C["nut"], 3 * S2, cv2.LINE_AA)
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


def ve_lua(can, m, C, hop):
    """ngọn lửa thay cho tóc gốc: gốc là mép dưới của vùng tóc (nằm trên đỉnh đầu), cao ~1,25 lần tóc gốc."""
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    # đoạn gốc: hơi dưới mép dưới vùng tóc (để gốc lửa chui vào đỉnh đầu)
    bl = (x0 + (x1 - x0) * 0.10, y1 - (y1 - y0) * 0.18)
    br = (x0 + (x1 - x0) * 0.92, y1 - (y1 - y0) * 0.05)
    cao = (y1 - y0) * 1.25
    polys = luoi_lua(bl, br, cao)
    ngoai = np.zeros(m.shape, np.uint8)
    for P in polys:
        cv2.fillPoly(ngoai, [P.astype(np.int32)], 1)
    # gốc liền một khối: bầu tròn phủ đoạn gốc
    cx, cy = (bl[0] + br[0]) / 2, (bl[1] + br[1]) / 2
    cv2.ellipse(ngoai, (int(cx), int(cy)), (int((br[0] - bl[0]) * 0.56), int(cao * 0.22)), math.degrees(math.atan2(br[1] - bl[1], br[0] - bl[0])),
                0, 360, 1, -1)
    ngoai = cv2.GaussianBlur(ngoai.astype(np.float32), (0, 0), 3 * S2) > 0.5
    # lớp giữa và lõi: co về phía gốc (thu nhỏ quanh điểm gốc rồi giao với khối ngoài đã gọt)
    def co(k, dx=0):
        M = cv2.getRotationMatrix2D((float(cx), float(cy + cao * 0.05)), 0, k)
        M[0, 2] += dx
        return cv2.warpAffine(ngoai.astype(np.uint8), M, (m.shape[1], m.shape[0])).astype(bool) & cv2.erode(
            ngoai.astype(np.uint8), el(10 * S2)).astype(bool)
    giua = co(0.74, 8 * S2)
    loi = co(0.46, 14 * S2)
    can[ngoai] = C["lua"][0]
    can[giua] = C["lua"][1]
    can[loi] = C["lua"][2]
    can[vien(ngoai, 3 * S2)] = INK
    ys2, xs2 = np.nonzero(ngoai)
    hop["lua"] = [xs2.min() / S2, ys2.min() / S2, xs2.max() / S2, ys2.max() / S2]
    hop["lua_goc"] = [bl[0] / S2, bl[1] / S2, br[0] / S2, br[1] / S2]


if __name__ == "__main__":
    hs = sys.argv[1] if len(sys.argv) > 1 else "all"
    for h in (HUONG if hs == "all" else [hs]):
        ve(h)
