# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của rùa golem lửa (rua_lua, tướng thứ 5 đảo Hỏa): khối từng part của rig monster_3425 ở khung 0 idle_01, tô phẳng
theo màu của THIẾT KẾ MÌNH. Pha lê đỏ TRÊN LƯNG của con gốc thành GAI LỬA (lưỡi lửa nhọn vẽ bằng mã theo đúng trục từng pha lê: gốc
ở chân pha lê, ngọn theo hướng mũi); pha lê nhỏ ở chân giữ là pha lê, đổi sang màu dung nham; mắt đỏ thành mắt lửa. Mai, cột đá trên
mai, bốn chân, đuôi, mặt sọ đá, hàm, hai sừng giữ đúng chỗ, cỡ, thứ tự chồng của rig; không mang nét, hoa văn, màu của con gốc.
Chỉ để GPT lấy chỗ đặt, cỡ, thứ tự chồng.

Người dùng (2026-11-13): "concept rùa golem lửa, đổi pha lê đỏ trên lưng thành gai lửa, lửa cũng phải có animation đung đưa nhẹ".
Ba hướng màu dưới đây là ĐỀ XUẤT của Claude (tránh tông đã dùng ở đảo Hỏa: nâu đỏ gạch của quy_lava, vỏ chai đen tím của mat_lua,
giáp cháy đen của cung_lua, đá tro xám kem của golem_lua):
  bazan    đá bazan xám lam, cột đá chàm than, sọ và sừng màu ngà
  dat_son  đá sa thạch vàng son, cột đá và sừng nâu sẫm, sọ kem
  ca_phe   đá nâu cà phê sẫm, cột đá nâu đen, sọ và sừng màu ngà

    rua_lua_bo_cuc.py [hướng|all]   → inbox/rua_lua_1/mau/bo_cuc_<hướng>.png (+ bo_cuc.json, _luoi_<hướng>.png)
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
import rua_lua as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
S2 = 2
INK = (43, 33, 24)
ATT = "att_idle0.json"

LUA = ((224, 68, 31), (247, 144, 42), (255, 212, 90))          # lửa: ngoài → trong
HUONG = {
    "bazan": dict(da=(95, 108, 125), mai=(78, 90, 108), cot=(53, 59, 72), bung=(135, 147, 161), so=(230, 218, 192),
                  sung=(240, 232, 212), gai=(240, 232, 212), ranh=(60, 70, 86)),
    "dat_son": dict(da=(201, 160, 92), mai=(186, 142, 74), cot=(91, 67, 52), bung=(224, 196, 140), so=(240, 228, 198),
                    sung=(91, 67, 52), gai=(240, 228, 198), ranh=(150, 112, 56)),
    "ca_phe": dict(da=(104, 80, 64), mai=(92, 70, 56), cot=(56, 44, 40), bung=(154, 123, 94), so=(232, 220, 192),
                   sung=(240, 232, 212), gai=(240, 232, 212), ranh=(68, 52, 42)),
}
PHA_LE = (242, 138, 46)

# vai trò từng slot (khung 0 idle). "x+ple": mảnh có pha lê đỏ nhỏ (phần đỏ → pha lê dung nham); "x+gai": đuôi có gai sáng.
VAI = {
    "p_kuangshi07": "lua", "p_kuangshi06": "lua", "p_datui05": "da", "p_xiaotui03": "da", "p_weiba": "da+gai",
    "p_kuangshi05": "cot", "p_xiaotuineice": "da", "p_datui02": "da", "p_xiaotui02": "da+ple", "p_datui04": "da",
    "p_xiaotui04": "da", "p_xiongqiang": "bung", "p_guike02": "bung", "p_datui01": "da", "p_ke": "mai",
    "p_jiao01_2": "sung", "p_kuangshi04": "ple", "p_kuangshi03": "cum", "p_kuangshi02": "lua", "p_kuangshi01": "cot",
    "p_xiaba01": "so", "p_lian": "so", "p_xiaba": "so", "p_yanjing": "mat", "p_jiao01": "sung", "p_xiaotui01": "da+ple",
}
# cụm pha lê lớn trên đỉnh mai (p_kuangshi03): từng pha lê = (tên, gốc, mũi) theo toạ độ chuẩn hoá trong ẢNH PART (213 × 173)
CUM = [("lua_trai", (0.30, 0.87), (0.02, 0.57), 0.30),
       ("lua_giua_trai", (0.53, 0.72), (0.35, 0.48), 0.30),
       ("lua_cao", (0.66, 0.72), (0.59, 0.02), 0.36),
       ("lua_phai", (0.885, 0.76), (0.91, 0.41), 0.17)]
LUA_DAI = {"p_kuangshi07": 1.25, "p_kuangshi06": 1.3, "p_kuangshi02": 1.3, "lua_trai": 1.12, "lua_giua_trai": 1.15,
           "lua_cao": 1.10, "lua_phai": 1.2}
LAT = set()
NHOM = {
    "mai": ["p_ke"], "vanh_mai": ["p_guike02"], "bung": ["p_xiongqiang"],
    "cot_gan": ["p_kuangshi01"], "cot_xa": ["p_kuangshi05"],
    "mat_so": ["p_lian"], "ham": ["p_xiaba"], "ham_sau": ["p_xiaba01"], "mat": ["p_yanjing"],
    "sung_gan": ["p_jiao01"], "sung_xa": ["p_jiao01_2"],
    "chan_truoc_gan": ["p_datui01", "p_xiaotui01", "p_kuangshi04"], "chan_truoc_xa": ["p_datui02", "p_xiaotui02", "p_xiaotuineice"],
    "chan_sau_gan": ["p_datui04", "p_xiaotui04"], "chan_sau_xa": ["p_datui05", "p_xiaotui03"],
    "duoi": ["p_weiba"],
}
# rãnh khắc đơn giản (toạ độ chuẩn hoá trong khung của mảnh): chi tiết của MÌNH, mật độ thấp (mai là các tấm đá ghép)
RANH = {
    "p_ke": [[(0.30, 0.12), (0.40, 0.42), (0.20, 0.62)], [(0.40, 0.42), (0.66, 0.36), (0.80, 0.10)], [(0.66, 0.36), (0.74, 0.62)]],
    "p_xiaotui01": [[(0.30, 0.62), (0.52, 0.74), (0.60, 0.95)]],
    "p_xiaotui04": [[(0.35, 0.45), (0.55, 0.62)]],
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
    SC = min((W - 300) / (x1 - x0), (H - 250) / (y1 - y0))
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = H - 90 + y0 * SC
    return SC, (lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1))


def lop(a, T):
    """ảnh gốc của part dán lên canvas (S2): trả (alpha, rgb): chỉ dùng để tách vùng pha lê đỏ / gai sáng trong mảnh ghép."""
    src = G.part_goc(a)
    uv, tr = G.luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2))
    lay = Image.new("RGBa", (W * S2, H * S2), (0, 0, 0, 0))
    _tris(lay, src.convert("RGBa"), V * S2, uv, tr)
    A = np.asarray(lay.convert("RGBA"))
    return A[..., 3], A[..., :3].astype(np.int32)


def affine(a, T):
    """phép affine: toạ độ điểm ảnh trong ảnh part → canvas (S2), bình phương tối thiểu trên đỉnh lưới."""
    uv, _ = G.luoi(a)
    V = T(np.array(a["xy"], float).reshape(-1, 2)) * S2
    A = np.concatenate([uv, np.ones((len(uv), 1))], 1)
    M, *_ = np.linalg.lstsq(A, V, rcond=None)
    return lambda p: np.concatenate([np.atleast_2d(np.asarray(p, float)), np.ones((len(np.atleast_2d(p)), 1))], 1) @ M


def bong(al, tron=3.0):
    m = (al > 110).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(3))
    return cv2.GaussianBlur(m * 255, (0, 0), tron) > 127


def do_gai(m):
    """pha lê (hình nón): tâm chân, hướng chân → mũi, dài, rộng chân."""
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
    if w_lo < w_hi:
        d, t = -d, -t
        lo, hi = -hi, -lo
    if d[1] > 0.3:                         # gai lửa trên lưng luôn chĩa lên
        d, lo, hi = -d, -hi, -lo
    base = c + d * lo
    return base, d, L, max(w_lo, w_hi)


def gai_lua(base, d, L, w, seed=0):
    """GAI LỬA: lưỡi lửa dáng gai: gốc dày, thân thon dần rất ít uốn, ngọn nhọn hơi móc về sau (sang trái: con nhìn phải), một lưỡi
    phụ nhỏ ở sườn. Trả danh sách đa giác."""
    rng = np.random.default_rng(seed)
    up = np.array([-0.45, -1.0])
    up /= np.linalg.norm(up)
    perp = np.array([-d[1], d[0]])
    ts = np.linspace(0, 1, 70)
    mix = np.clip(ts - 0.5, 0, None) / 0.5 * 0.30
    dirs = d[None] * (1 - mix[:, None]) + up[None] * mix[:, None]
    dirs /= np.linalg.norm(dirs, axis=1, keepdims=True)
    sp = base[None] + np.cumsum(dirs * (L / len(ts)), 0) - d[None] * w * 0.12
    sp += perp[None] * (0.045 * L * np.sin(ts * math.pi * 1.5 + rng.uniform(0, 1)))[:, None]
    wd = w * 0.52 * (1 - ts) ** 0.8 * (1 + 0.22 * np.sin(ts * math.pi))
    dx, dy = np.gradient(sp[:, 0]), np.gradient(sp[:, 1])
    nn = np.hypot(dx, dy) + 1e-6
    nx, ny = -dy / nn, dx / nn
    A = np.stack([sp[:, 0] + nx * wd, sp[:, 1] + ny * wd], 1)
    B = np.stack([sp[:, 0] - nx * wd, sp[:, 1] - ny * wd], 1)
    polys = [np.concatenate([A, B[::-1]], 0)]
    if L > 150:
        k = int(len(ts) * rng.uniform(0.25, 0.36))
        sgn = 1 if rng.uniform() < 0.5 else -1
        b2 = sp[k] + np.array([nx[k], ny[k]]) * wd[k] * 0.5 * sgn
        d2 = dirs[k] * 0.78 + np.array([nx[k], ny[k]]) * 0.62 * sgn
        d2 /= np.linalg.norm(d2)
        L2 = L * 0.30
        t2 = np.linspace(0, 1, 30)
        s2 = b2[None] + np.cumsum(np.repeat(d2[None], len(t2), 0) * (L2 / len(t2)), 0)
        w2 = wd[k] * 0.5 * (1 - t2) ** 0.9
        A2 = np.stack([s2[:, 0] - d2[1] * w2, s2[:, 1] + d2[0] * w2], 1)
        B2 = np.stack([s2[:, 0] + d2[1] * w2, s2[:, 1] - d2[0] * w2], 1)
        polys.append(np.concatenate([A2, B2[::-1]], 0))
    return polys


def to_lua(can, m):
    can[m] = LUA[0]
    giua = cv2.erode(m.astype(np.uint8), el(11 * S2)).astype(bool)
    loi = cv2.erode(m.astype(np.uint8), el(24 * S2)).astype(bool)
    can[giua] = LUA[1]
    can[loi] = LUA[2]
    can[vien(m, 3 * S2)] = INK


def ve_lua(can, info, ten, base, d, L, w, seed):
    k = LUA_DAI.get(ten, 1.2)
    ml = np.zeros(can.shape[:2], np.uint8)
    for P in gai_lua(base, d, L * k, w, seed=seed):
        cv2.fillPoly(ml, [P.astype(np.int32)], 1)
    ml = cv2.GaussianBlur(ml.astype(np.float32), (0, 0), 2 * S2) > 0.5
    to_lua(can, ml)
    ys2, xs2 = np.nonzero(ml)
    tip = base + d * L * k
    info["lua"][ten] = dict(goc=[round(base[0] / S2), round(base[1] / S2)], ngon=[round(tip[0] / S2), round(tip[1] / S2)],
                            hop=[round(xs2.min() / S2), round(ys2.min() / S2), round(xs2.max() / S2), round(ys2.max() / S2)])


def ve(huong):
    C = HUONG[huong]
    SC, T = khung_T()
    G._C.pop("att", None)
    _, _, atts = G.nap(ATT)
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop, info = {}, {"lua": {}, "ple": []}
    for i, a in enumerate(atts):
        v = VAI.get(a["slot"])
        if not v:
            continue
        al, rgb = lop(a, T)
        m = bong(al, 1.6 if v in ("mat", "ple") else 3.5)
        if not m.any():
            continue
        ys, xs = np.nonzero(m)
        b = [xs.min() / S2, ys.min() / S2, xs.max() / S2, ys.max() / S2]
        info.setdefault("slot", {})[a["slot"]] = [round(x) for x in b]
        for ten, sl in NHOM.items():
            if a["slot"] in sl:
                h = hop.get(ten)
                hop[ten] = b if h is None else [min(h[0], b[0]), min(h[1], b[1]), max(h[2], b[2]), max(h[3], b[3])]
        nen = v.split("+")[0]
        red = (al > 110) & (rgb[..., 0] > 140) & (rgb[..., 0] - rgb[..., 1] > 70) & (rgb[..., 0] - rgb[..., 2] > 60)
        if nen in ("da", "mai", "cot", "bung", "so", "sung"):
            can[m] = C[nen]
            can[vien(m, 3 * S2)] = INK
            x0, y0, x1, y1 = xs.min(), ys.min(), xs.max(), ys.max()
            for ln in RANH.get(a["slot"], []):
                P = np.array([(x0 + (x1 - x0) * u, y0 + (y1 - y0) * w) for u, w in ln], np.int32)
                cv2.polylines(can, [P], False, INK, 2 * S2, cv2.LINE_AA)
            if v.endswith("+ple"):
                mp = cv2.dilate(cv2.morphologyEx(red.astype(np.uint8), cv2.MORPH_OPEN, el(2)), el(2 * S2)).astype(bool)
                mp = cv2.GaussianBlur(mp.astype(np.uint8) * 255, (0, 0), 1.5 * S2) > 127
                can[mp] = PHA_LE
                can[vien(mp, 3 * S2)] = INK
                n, lab, st, cen = cv2.connectedComponentsWithStats(mp.astype(np.uint8))
                for k in range(1, n):
                    if st[k, cv2.CC_STAT_AREA] > 200 * S2 * S2:
                        info["ple"].append([round(cen[k][0] / S2), round(cen[k][1] / S2)])
            if v.endswith("+gai"):
                lum = rgb.mean(-1)
                mg = (al > 110) & (lum > 150)
                mg = cv2.GaussianBlur(cv2.dilate(mg.astype(np.uint8), el(1.5 * S2)) * 255, (0, 0), 1.2 * S2) > 127
                can[mg & m] = C["gai"]
                can[vien(mg, 3 * S2) & m] = INK
                can[vien(m, 3 * S2)] = INK
        elif nen == "ple":
            can[m] = PHA_LE
            can[vien(m, 3 * S2)] = INK
            info["ple"].append([round(xs.mean() / S2), round(ys.mean() / S2)])
        elif nen == "mat":
            ex, ey = xs.mean(), ys.mean()
            er = (xs.max() - xs.min() + ys.max() - ys.min()) / 4 * 1.25
            # mắt xếch dữ: tam giác bo, đáy nằm dưới, đỉnh nhọn chĩa lên sau
            P = np.array([(ex - er * 1.1, ey - er * 1.0), (ex + er * 1.25, ey + er * 0.55), (ex - er * 0.8, ey + er * 1.0)], np.int32)
            mm = np.zeros(can.shape[:2], np.uint8)
            cv2.fillPoly(mm, [P], 1)
            mm = cv2.GaussianBlur(mm * 255, (0, 0), 1.5 * S2) > 110
            sock = cv2.dilate(mm.astype(np.uint8), el(4 * S2)).astype(bool)
            can[sock] = (40, 34, 36)
            can[mm] = LUA[2]
            can[vien(mm, 2 * S2)] = INK
            can[vien(sock, 2 * S2)] = INK
            hop["mat_tam"] = [round(ex / S2), round(ey / S2), round(er / S2)]
        elif nen == "lua":
            base, d, L, w = do_gai(m)
            ve_lua(can, info, a["slot"], base, d, L, w * 0.95, i)
        elif nen == "cum":
            im = G._C["imgs"][a["region"]]
            A = affine(a, T)
            sz = np.array([im.width, im.height], float)
            for j, (ten, g, n_, wk) in enumerate(CUM):
                pg, pn = A(np.array(g) * sz)[0], A(np.array(n_) * sz)[0]
                L = float(np.linalg.norm(pn - pg))
                d = (pn - pg) / L
                wpx = float(np.linalg.norm(A(np.array([wk * im.width, 0.0]))[0] - A(np.array([0.0, 0.0]))[0]))
                ve_lua(can, info, ten, pg, d, L, wpx, 100 + j)
            hop["cum_lua"] = b
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
