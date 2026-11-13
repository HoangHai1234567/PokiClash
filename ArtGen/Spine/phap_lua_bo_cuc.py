# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của pháp sư lửa (phap_lua, tướng thứ 6 đảo Hỏa): hình bóng từng part của rig monster_3481 ở khung 0 idle_01, tô
phẳng theo màu của THIẾT KẾ MÌNH. Con mắt trong đầu trượng thành CẦU LỬA (vẽ bằng mã: quả cầu ba vùng màu + ba lưỡi lửa bốc lên sau
khung trượng). Mọi mảnh khác giữ đúng chỗ, cỡ, hình bóng, thứ tự chồng của rig; không mang nét, hoa văn, màu của con gốc. Chỉ để GPT
lấy chỗ đặt, cỡ, hình bóng, thứ tự chồng.

Người dùng (2026-11-13): "concept pháp sư lửa giống như ref, con mắt trong quyền trượng đổi thành cầu lửa cháy liên tục".
Ba hướng màu dưới đây là ĐỀ XUẤT của Claude (tránh tông đã dùng ở đảo Hỏa: đá nâu đỏ gạch quy_lava, vỏ chai đen tím mat_lua, giáp cháy
nâu đen cung_lua, đá tro xám golem_lua):
  ao_do     áo choàng đỏ thẫm hoa văn lưỡi lửa cam, tóc tro trắng kem, giáp + trượng đen than (sát con gốc nhất)
  toc_lua   tóc là bờm lửa, áo xám than hoa văn than hồng, khăn vai đỏ thẫm, giáp sắt đen
  khoi      tóc khói xám than, áo cam hổ phách hoa văn vàng, khăn vai nâu đỏ, giáp + trượng đồng thau

    phap_lua_bo_cuc.py [hướng|all]   → inbox/phap_lua_1/mau/bo_cuc_<hướng>.png (+ bo_cuc.json, _luoi_<hướng>.png)
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
import phap_lua as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
S2 = 2
INK = (43, 33, 24)
ATT = "att_idle0.json"
LUA = ((224, 68, 31), (247, 144, 42), (255, 212, 90))          # lửa: ngoài → trong

HUONG = {
    "ao_do": dict(ao=(163, 46, 34), ao2=(232, 120, 42), choang=(60, 53, 59), toc=(233, 225, 210), giap=(74, 66, 76),
                  mat_na=(74, 66, 76), day=(226, 178, 76), ngoc=(255, 212, 90), co_tay=(233, 225, 210), vuot=(74, 66, 76),
                  sao=(74, 66, 76)),
    "toc_lua": dict(ao=(91, 83, 87), ao2=(190, 84, 44), choang=(138, 42, 34), toc="lua", giap=(72, 66, 78),
                    mat_na=(72, 66, 78), day=(232, 223, 204), ngoc=(247, 144, 42), co_tay=(247, 144, 42), vuot=(72, 66, 78),
                    sao=(72, 66, 78)),
    "khoi": dict(ao=(224, 138, 46), ao2=(247, 196, 84), choang=(110, 38, 48), toc=(96, 90, 102), giap=(181, 116, 56),
                 mat_na=(181, 116, 56), day=(60, 52, 58), ngoc=(224, 68, 31), co_tay=(150, 144, 154), vuot=(60, 52, 58),
                 sao=(181, 116, 56)),
}

# vai trò từng slot (khung 0 idle)
VAI = {
    "pifeng_03": "ao", "shenti": "day", "pifeng_02": "choang", "pifeng_01": "choang", "maofa_01": "toc",
    "zhuangshi_02": "sao", "zhuangshi_01": "sao", "tou_05": "mat_na", "tou_04": "mat_na", "tou_03": "ngoc",
    "tou_02": "giap", "tou_01": "giap", "shouzhangR_01": "co_tay", "wuqi": "truong", "shouzhangL_01": "co_tay",
}
NHOM = {
    "ao": ["pifeng_03"], "day": ["shenti"], "choang_trai": ["pifeng_02"], "choang_phai": ["pifeng_01"], "toc": ["maofa_01"],
    "sao_trai": ["zhuangshi_02"], "sao_phai": ["zhuangshi_01"], "mat_na": ["tou_05", "tou_04"], "ngoc": ["tou_03"],
    "sung_trai": ["tou_02"], "sung_phai": ["tou_01"], "truong": ["wuqi"],
    "tay_truong": ["shouzhangR_01", "shouzhiR_01", "shouzhiR_02", "shouzhiR_03", "shouzhiR_04"],
    "tay_vuot": ["shouzhangL_01"] + [f"shouzhiL_{i:02d}" for i in range(1, 11)],
}


def vai_cua(slot):
    if slot in VAI:
        return VAI[slot]
    if slot.startswith("shouzhi"):
        return "vuot"
    return None


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def vien(m, r):
    return m & ~cv2.erode(m.astype(np.uint8), el(r)).astype(bool)


def khung_T():
    _, _, atts = G.nap(ATT)
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts if vai_cua(a["slot"])])
    x0, y0, x1, y1 = P[:, 0].min(), P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    SC = min((W - 420) / (x1 - x0), (H - 190) / (y1 - y0))
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = H - 50 + y0 * SC
    return SC, (lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1))


def lop(a, T):
    src = G.part_goc(a)
    uv, tr = G.luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2))
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, src.convert("RGBa"), V * S2, uv, tr)
    A = np.asarray(lay.convert("RGBA"))
    return A[..., 3], A[..., :3].astype(np.int32)


def bong(al, tron=2.0):
    m = (al > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(2))
    return cv2.GaussianBlur(m * 255, (0, 0), tron) > 127


def luoi_lua(base, d, L, w, seed=0, cong=0.45):
    """một lưỡi lửa: gốc dày ở base, thân uốn chữ S theo hướng d, ngọn nhọn móc lên và về sau (sang trái)."""
    rng = np.random.default_rng(seed)
    up = np.array([-0.55, -1.0])
    up /= np.linalg.norm(up)
    perp = np.array([-d[1], d[0]])
    ts = np.linspace(0, 1, 70)
    mix = np.clip(ts - 0.3, 0, None) / 0.7 * cong
    dirs = d[None] * (1 - mix[:, None]) + up[None] * mix[:, None]
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    sp = base[None] + np.cumsum(dirs * (L / len(ts)), 0)
    sp += perp[None] * (0.07 * L * np.sin(ts * math.pi * 1.7 + rng.uniform(0, 1)))[:, None]
    wd = w * 0.5 * (1 - ts) ** 0.8 * (1 + 0.25 * np.sin(ts * math.pi))
    dx, dy = np.gradient(sp[:, 0]), np.gradient(sp[:, 1])
    nn = np.hypot(dx, dy) + 1e-6
    nx, ny = -dy / nn, dx / nn
    A = np.stack([sp[:, 0] + nx * wd, sp[:, 1] + ny * wd], 1)
    B = np.stack([sp[:, 0] - nx * wd, sp[:, 1] - ny * wd], 1)
    return np.concatenate([A, B[::-1]], 0)


def to_lua(can, m, r1=8, r2=17):
    can[m] = LUA[0]
    can[cv2.erode(m.astype(np.uint8), el(r1 * S2)).astype(bool)] = LUA[1]
    can[cv2.erode(m.astype(np.uint8), el(r2 * S2)).astype(bool)] = LUA[2]
    can[vien(m, 3 * S2)] = INK


def cau_lua(can, cx, cy, R):
    """cầu lửa: quả cầu ba vùng + ba lưỡi lửa bốc lên, ngả về sau (trái)."""
    m = np.zeros(can.shape[:2], np.uint8)
    cv2.circle(m, (int(cx), int(cy)), int(R), 1, -1, cv2.LINE_AA)
    for k, (dx, ang, L, w) in enumerate([(-0.42, -118, 1.75, 0.95), (0.05, -100, 2.35, 1.15), (0.5, -84, 1.6, 0.85)]):
        a = math.radians(ang)
        base = np.array([cx + dx * R, cy - 0.35 * R])
        P = luoi_lua(base, np.array([math.cos(a), math.sin(a)]), L * R, w * R, seed=11 + k, cong=0.5)
        cv2.fillPoly(m, [P.astype(np.int32)], 1)
    m = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 2 * S2) > 0.5
    can[m] = LUA[0]
    can[cv2.erode(m.astype(np.uint8), el(0.2 * R)).astype(bool)] = LUA[1]
    yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
    ang = np.arctan2(yy - cy, xx - cx)
    dd = np.hypot(xx - cx, yy - cy) * (1 + 0.08 * np.sin(ang * 6))
    can[m & (dd < R * 0.58)] = LUA[2]
    can[vien(m, 3 * S2)] = INK
    ys, xs = np.nonzero(m)
    return [xs.min() / S2, ys.min() / S2, xs.max() / S2, ys.max() / S2]


def ve(huong):
    C = HUONG[huong]
    SC, T = khung_T()
    G._C.pop("att", None)
    _, _, atts = G.nap(ATT)
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop, info = {}, {"slot": {}}
    for i, a in enumerate(atts):
        v = vai_cua(a["slot"])
        if not v:
            continue
        al, rgb = lop(a, T)
        m = bong(al, 1.4 if v in ("vuot", "ngoc", "sao", "mat_na", "day") else 2.4)
        if not m.any():
            continue
        if v == "truong":
            sang = (al > 110) & (rgb.sum(-1) > 480)                       # quả cầu mắt (trắng / tím nhạt) trong ảnh trượng
            n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.morphologyEx(sang.astype(np.uint8), cv2.MORPH_CLOSE, el(6 * S2)))
            k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
            (cx, cy), R = cv2.minEnclosingCircle(np.argwhere(lab == k)[:, ::-1].astype(np.float32))
            R *= 0.97
            hb = cau_lua(can, cx, cy, R)
            hop["cau_lua"] = hb
            hop["cau_tam"] = [cx / S2, cy / S2, R / S2]
            cau = np.zeros(m.shape, np.uint8)
            cv2.circle(cau, (int(cx), int(cy)), int(R * 0.98), 1, -1)
            toi = (al > 110) & (rgb.sum(-1) < 330)                         # khung trượng (sẫm) đè lên quả cầu
            toi = cv2.morphologyEx(toi.astype(np.uint8), cv2.MORPH_OPEN, el(2 * S2))
            toi = cv2.GaussianBlur(toi * 255, (0, 0), 2.0) > 127
            m = np.where(cau.astype(bool), toi, m)
            n2, lab2, st2, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8))
            m = lab2 == (1 + int(np.argmax(st2[1:, cv2.CC_STAT_AREA])))
        ys, xs = np.nonzero(m)
        b = [xs.min() / S2, ys.min() / S2, xs.max() / S2, ys.max() / S2]
        info["slot"][a["slot"]] = [round(x) for x in b]
        for ten, sl in NHOM.items():
            if a["slot"] in sl:
                h = hop.get(ten)
                hop[ten] = b if h is None else [min(h[0], b[0]), min(h[1], b[1]), max(h[2], b[2]), max(h[3], b[3])]
        if v == "truong":
            can[m] = C["giap"]
            can[vien(m, 3 * S2)] = INK
        elif v == "toc" and C["toc"] == "lua":
            to_lua(can, m, 11, 26)
        elif v == "ao":
            can[m] = C["ao"]
            # hoa văn của MÌNH: vùng trong sáng hơn, ranh uốn như lưỡi lửa (không theo hoa văn con gốc)
            inn = cv2.erode(m.astype(np.uint8), el(30 * S2)).astype(np.uint8)
            yy, xx = np.mgrid[0:m.shape[0], 0:m.shape[1]]
            cxm, cym = xs.mean(), ys.mean()
            ang = np.arctan2(yy - cym, xx - cxm)
            rr = np.hypot(xx - cxm, yy - cym)
            rmax = (xs.max() - xs.min() + ys.max() - ys.min()) / 4
            song = rr < rmax * (0.62 + 0.16 * np.sin(ang * 9 + 0.6))
            can[inn.astype(bool) & song] = C["ao2"]
            can[vien(m, 3 * S2)] = INK
        elif v == "co_tay" and huong == "toc_lua":
            to_lua(can, m, 6, 13)
        else:
            mau = C[v]
            can[m] = mau
            can[vien(m, 3 * S2)] = INK
    im = Image.fromarray(can, "RGB").resize((W, H), Image.LANCZOS)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, f"bo_cuc_{huong}.png")
    im.save(p)
    out = {k: [round(x) for x in v] for k, v in hop.items()}
    out.update(info)
    allb = np.array(list(info["slot"].values()) + [out["cau_lua"]])
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
