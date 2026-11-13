# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của quỷ lửa cầm đao lớn (quy_dao, tướng thứ 7 đảo Hỏa): khối từng part của rig monster_3655 ở khung 0 idle_01, tô
phẳng theo màu của THIẾT KẾ MÌNH. Giữ của con gốc: dáng (quỷ lưng gù nhìn sang PHẢI, tay gần to buông trước, tay xa vòng lên sau đầu
nắm cán vũ khí, vũ khí khổng lồ dựng chéo sau lưng mũi chống đất bên phải, chân ngắn), chỗ, cỡ, thứ tự chồng từng part.
Đổi dáng (mảnh cứng một xương nên đổi tự do, vẽ bằng mã):
  - kiếm thẳng có chắn tay hình sao  →  ĐAO lớn một lưỡi (cán dài có khâu tròn, chắn tay bầu nhỏ, bản đao loe dần về mũi, mũi vát,
    sống đao có một khấc); lưỡi sắc ở phía DẪN ĐẦU của cú chém trong clip gốc (trục −y của xương wuqi_03)
  - hai sừng chữ S móc ngược            →  hai sừng nón to, cong nhẹ, chĩa lên
  - mặt nạ đá + bốn gai rời trên trán   →  một mặt nạ quỷ liền có mào ba mũi (bốn slot gai bỏ)
  - giáp vai nhiều gai chĩa tứ phía      →  giáp vai vòm tròn có vành + một gai cong
  - bờm tóc dáng lửa tô chuyển màu      →  LỬA thật ba vùng màu phẳng, viền ngoài thêm các lưỡi lửa nhọn
Chỉ để GPT lấy chỗ đặt, cỡ, thứ tự chồng.

Người dùng (2026-11-13): "làm tướng thứ 7 đảo hỏa, concept quỷ lửa cầm đao lớn". Ba hướng màu là ĐỀ XUẤT của Claude (tránh tông đã
dùng ở đảo Hỏa: nâu đỏ gạch quy_lava, vỏ chai đen tím mat_lua, giáp cháy cung_lua, đá tro xám kem golem_lua, bazan xám lam rua_lua,
áo đỏ phap_lua):
  do_tham  da đỏ thẫm, mặt nạ + sừng màu ngà, giáp sắt đen
  than     da xám than, giáp đồng, mặt nạ đỏ son, sừng ngà
  tro      da tro nhạt, giáp + mặt nạ sắt đen, sừng đỏ thẫm

    quy_dao_bo_cuc.py [hướng|all]   → inbox/quy_dao_1/mau/bo_cuc_<hướng>.png (+ bo_cuc.json, _luoi_<hướng>.png)
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
import quy_dao as G  # noqa: E402
from quai.soi import _tris  # noqa: E402

W, H = 1536, 1024
S2 = 2
INK = (43, 33, 24)
ATT = "att_idle0.json"

LUA = ((224, 68, 31), (247, 144, 42), (255, 212, 90))          # lửa: ngoài → trong
HUONG = {
    "do_tham": dict(da=(176, 52, 44), giap=(62, 60, 68), vai=(78, 56, 46), mat_na=(236, 226, 200), sung=(240, 232, 212),
                    sung_mui=(96, 70, 60), vuot=(240, 232, 212), dao=(112, 118, 130), can=(96, 62, 44), dao_vanh=(62, 60, 68)),
    "than": dict(da=(84, 80, 92), giap=(186, 120, 58), vai=(52, 46, 52), mat_na=(150, 44, 38), sung=(240, 232, 212),
                 sung_mui=(110, 84, 70), vuot=(240, 232, 212), dao=(70, 70, 80), can=(110, 44, 38), dao_vanh=(186, 120, 58)),
    "tro": dict(da=(206, 196, 186), giap=(58, 56, 64), vai=(124, 42, 38), mat_na=(50, 46, 54), sung=(132, 38, 36),
                sung_mui=(70, 30, 32), vuot=(58, 56, 64), dao=(88, 90, 102), can=(124, 42, 38), dao_vanh=(58, 56, 64)),
}

# vai trò từng slot (khung 0 idle). "da+giap": phần tối của mảnh gốc → giáp; "da+vai": phần tối → vải / da thuộc; "da+vuot": phần sáng → vuốt
VAI = {
    "hsouzhitou": "da", "damuzhi_l": "da", "shou_l": "da", "dabi_l": "da", "xiaobi_l": "da", "jiajia_l": "giap",
    "wuqi_02": "dao", "yao": "da", "shenti": "da", "xiaotui_l": "vai", "xiaotui_r": "vai", "tuishi_01": "giap", "tuishi_02": "giap",
    "datui_l": "da+vai", "datui_r": "da+vai", "yaojia_05": "giap", "yaojia_04": "giap", "yaojia_03": "giap",
    "yaojia_02": "vai", "yaojia_01": "giap",
    "toufa_01": "lua", "toufa_07": "lua", "toufa_03": "lua", "toufa_02": "lua", "toufa_06": "lua", "huzi": "rau",
    "dajiao_l": "sung_xa", "dajiao_r": "sung_gan", "lian_01": "mat_na",
    "shouzhi_01": "da", "dabi_r": "da", "xiaobi_r": "da+giap", "shou_r": "da",
    "shouzhi_02": "da+vuot", "shouzhi_03": "da+vuot", "shouzhi_04": "da+vuot", "shouzhi_05": "da+vuot",
    "jianjia": "giap_vai",
}
BO = {"jiao_01", "jiao_02", "jiao_03", "jiao_04"}              # bốn gai rời trên trán: bỏ (mào liền vào mặt nạ)
NHOM = {
    "than": ["shenti", "yao"], "tay_gan": ["dabi_r", "xiaobi_r", "shou_r", "shouzhi_02", "shouzhi_03", "shouzhi_04", "shouzhi_05"],
    "cang_tay_gan": ["xiaobi_r"], "ban_tay_gan": ["shou_r", "shouzhi_02", "shouzhi_03", "shouzhi_04", "shouzhi_05"],
    "tay_xa": ["dabi_l", "xiaobi_l", "jiajia_l"], "ban_tay_xa": ["shou_l", "damuzhi_l", "hsouzhitou"], "giap_tay_xa": ["jiajia_l"],
    "chan_gan": ["datui_r", "xiaotui_r"], "chan_xa": ["datui_l", "xiaotui_l", "tuishi_01", "tuishi_02"],
    "dai": ["yaojia_01", "yaojia_02", "yaojia_03", "yaojia_04", "yaojia_05"],
    "bom": ["toufa_01", "toufa_02", "toufa_03", "toufa_06", "toufa_07"], "rau": ["huzi"],
}
# số lưỡi lửa thêm ở viền ngoài mỗi búi (hạt giống, số lưỡi, dài theo đơn vị rig)
LUOI = {"toufa_01": (11, 5, 150), "toufa_02": (12, 3, 125), "toufa_07": (13, 3, 120), "toufa_03": (14, 3, 120), "toufa_06": (15, 0, 0)}
QUET = np.array([-0.55, 0.83])       # lửa tạt về sau - lên (con nhìn phải), hệ rig y lên
DAU = np.array([200.0, 430.0])       # tâm đầu (hệ rig)

# ---- hình vẽ bằng mã, toạ độ hệ rig (y lên) ----
# đao: (u dọc trục chuôi → mũi 0..1, v ngang; v > 0 = phía SỐNG đao = +y của xương; v < 0 = phía LƯỠI sắc)
DAO_BAN = [(0.365, 0.040), (0.60, 0.052), (0.775, 0.066), (0.790, 0.100), (0.865, 0.104), (0.93, 0.060), (1.0, -0.062),
           (0.955, -0.118), (0.86, -0.150), (0.74, -0.140), (0.60, -0.108), (0.46, -0.072), (0.365, -0.046)]
DAO_LUOI = [(0.365, -0.046), (0.46, -0.072), (0.60, -0.108), (0.74, -0.140), (0.86, -0.150), (0.955, -0.118), (1.0, -0.062),
            (0.965, -0.060), (0.93, -0.082), (0.86, -0.108), (0.74, -0.100), (0.60, -0.070), (0.46, -0.036), (0.365, -0.012)]
DAO_CAN = [(0.035, 0.022), (0.335, 0.024), (0.335, -0.024), (0.035, -0.022)]
DAO_CHAN = [(0.330, 0.062), (0.372, 0.070), (0.372, -0.076), (0.330, -0.066)]
DAO_KHAU = (0.020, 0.0, 0.034)       # khâu tròn ở chuôi: tâm (u, v), bán kính (theo chiều dài đao)
SUNG_GAN = dict(p=[(190, 468), (36, 520), (8, 812)], w0=156, w1=5)
SUNG_XA = dict(p=[(300, 452), (418, 492), (436, 688)], w0=96, w1=4)
MAT_NA = [(148, 500), (172, 520), (166, 592), (212, 532), (243, 648), (276, 534), (332, 604), (336, 516), (362, 496),
          (352, 432), (318, 380), (268, 348), (212, 376), (156, 424)]
MAT = [((218, 426), (-1, 0.42)), ((276, 417), (1, 0.42))]   # tâm mắt, (dấu phía đuôi mắt, độ xếch)
GIAP_VAI = [(-268, 340), (-264, 470), (-204, 568), (-104, 610), (-6, 584), (52, 500), (58, 420), (12, 352), (-62, 300),
            (-150, 258), (-232, 276)]
GIAP_VANH = [(-270, 318), (-236, 250), (-146, 228), (-52, 268), (26, 330), (72, 410), (40, 428), (2, 366), (-66, 312),
             (-150, 272), (-226, 290), (-250, 336)]
GIAP_GAI = dict(p=[(-170, 560), (-262, 628), (-250, 760)], w0=92, w1=3)


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def vien(m, r):
    return m & ~cv2.erode(m.astype(np.uint8), el(r)).astype(bool)


def khung_T():
    _, _, atts = G.nap(ATT)
    P = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in atts if a["slot"] in VAI])
    x0, y0, x1, y1 = P[:, 0].min() - 20, P[:, 1].min(), P[:, 0].max(), P[:, 1].max()
    SC = min((W - 260) / (x1 - x0), (H - 130) / (y1 - y0))
    ox = W / 2 - (x0 + x1) / 2 * SC
    oy = H - 55 + y0 * SC
    return SC, (lambda p: np.stack([ox + np.asarray(p, float)[..., 0] * SC, oy - np.asarray(p, float)[..., 1] * SC], -1))


def lop(a, T):
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


def da_giac(shape, P, tron=0.0):
    m = np.zeros(shape, np.uint8)
    cv2.fillPoly(m, [np.round(np.asarray(P)).astype(np.int32)], 1)
    if tron > 0:
        m = (cv2.GaussianBlur(m * 255, (0, 0), tron) > 127).astype(np.uint8)
    return m.astype(bool)


def bezier(p, n=40):
    p = np.asarray(p, float)
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * p[0] + 2 * (1 - t) * t * p[1] + t ** 2 * p[2]


def non(p, w0, w1, n=40, mu=1.0):
    """hình nón cong theo đường bezier bậc hai: rộng w0 ở gốc → w1 ở mũi (hệ rig)."""
    c = bezier(p, n)
    d = np.gradient(c, axis=0)
    d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-9
    nn = np.stack([-d[:, 1], d[:, 0]], 1)
    t = np.linspace(0, 1, n)
    w = (w0 + (w1 - w0) * t ** mu) / 2
    return np.concatenate([c + nn * w[:, None], (c - nn * w[:, None])[::-1]], 0)


def to_lua(can, m, day=1.0):
    can[m] = LUA[0]
    giua = cv2.erode(m.astype(np.uint8), el(12 * S2 * day)).astype(bool)
    loi = cv2.erode(m.astype(np.uint8), el(27 * S2 * day)).astype(bool)
    can[giua] = LUA[1]
    can[loi] = LUA[2]
    can[vien(m, 3 * S2)] = INK


def them_luoi(m, T, SC, slot):
    """thêm các lưỡi lửa nhọn ở viền NGOÀI của búi (phía xa đầu, tạt về sau - lên)."""
    seed, n, dai = LUOI.get(slot, (0, 0, 0))
    if not n:
        return m
    rng = np.random.default_rng(seed)
    cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)[:, 0, :].astype(float)
    step = 6
    c = c[::step]
    tg = np.roll(c, -3, 0) - np.roll(c, 3, 0)
    tg /= np.linalg.norm(tg, axis=1, keepdims=True) + 1e-9
    nr = np.stack([tg[:, 1], -tg[:, 0]], 1)                       # pháp tuyến ngoài (contour của OpenCV chạy cùng chiều kim: ảnh y xuống)
    cen = c.mean(0)
    if ((c - cen) * nr).sum(1).mean() < 0:
        nr = -nr
    dau = T(DAU) * S2
    quet = np.array([QUET[0], -QUET[1]])
    diem = (nr @ quet) * 0.6 + ((c - dau) / (np.linalg.norm(c - dau, axis=1, keepdims=True) + 1e-9) * nr).sum(1) * 0.8
    ok = np.nonzero(diem > 0.55)[0]
    if len(ok) < n:
        ok = np.argsort(-diem)[:max(n * 3, 6)]
    chon = []
    for i in sorted(ok, key=lambda i: -diem[i] + rng.uniform(0, 0.5)):
        if all(np.linalg.norm(c[i] - c[j]) > 95 * SC * S2 for j in chon):
            chon.append(i)
        if len(chon) >= n:
            break
    out = m.astype(np.uint8)
    for i in chon:
        L = dai * rng.uniform(0.75, 1.15) * SC * S2
        hw = L * rng.uniform(0.36, 0.46)
        d = nr[i] * 0.55 + quet * 0.6
        d /= np.linalg.norm(d)
        cong = tg[i] * rng.choice([-1, 1]) * 0.35
        b0, b1 = c[i] - tg[i] * hw - nr[i] * 10, c[i] + tg[i] * hw - nr[i] * 10
        tip = c[i] + d * L + cong * L * 0.5
        mid = c[i] + d * L * 0.5
        A = bezier([b0, mid - tg[i] * hw * 0.55 + cong * L * 0.12, tip], 16)
        B = bezier([b1, mid + tg[i] * hw * 0.55 + cong * L * 0.12, tip], 16)
        cv2.fillPoly(out, [np.round(np.concatenate([A, B[::-1]], 0)).astype(np.int32)], 1)
    out = (cv2.GaussianBlur(out * 255, (0, 0), 1.6 * S2) > 120).astype(np.uint8)
    cs, _ = cv2.findContours(out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(out, cs, -1, 1, -1)                          # lấp lỗ giữa lưỡi và búi
    return out.astype(bool)


def ve(huong):
    C = HUONG[huong]
    SC, T0 = khung_T()
    T = lambda p: T0(p) * S2  # noqa: E731
    G._C.pop("att", None)
    _, _, atts = G.nap(ATT)
    shape = (H * S2, W * S2)
    can = np.full(shape + (3,), 255, np.uint8)
    hop, info = {}, {"slot": {}}

    def ghi(ten, m):
        ys, xs = np.nonzero(m)
        b = [xs.min() / S2, ys.min() / S2, xs.max() / S2, ys.max() / S2]
        info["slot"][ten] = [round(x) for x in b]
        return b

    for a in atts:
        slot = a["slot"]
        v = VAI.get(slot)
        if not v or slot in BO:
            continue
        al, rgb = lop(a, T0)
        nho = slot.startswith(("shouzhi", "hsou", "damuzhi", "tuishi", "yaojia"))
        m = bong(al, 1.6 if nho else 3.5)
        if not m.any():
            continue
        nen = v.split("+")[0]
        lum = rgb.mean(-1)
        sat = rgb.max(-1) - rgb.min(-1)
        if nen in ("da", "giap", "vai"):
            can[m] = C[nen]
            if v.endswith("+giap") or v.endswith("+vai"):
                toi = (al > 110) & (lum < 105) & (sat < 60 if v.endswith("+giap") else sat < 90)
                toi = cv2.morphologyEx(toi.astype(np.uint8), cv2.MORPH_OPEN, el(2 * S2))
                toi = cv2.GaussianBlur(cv2.dilate(toi, el(2 * S2)) * 255, (0, 0), 2.5 * S2) > 127
                toi &= m
                can[toi] = C["giap" if v.endswith("+giap") else "vai"]
                can[vien(toi, 2 * S2) & m] = INK
                if v.endswith("+giap"):
                    ys, xs = np.nonzero(toi)
                    hop["giap_cang_tay"] = [xs.min() / S2, ys.min() / S2, xs.max() / S2, ys.max() / S2]
            if v.endswith("+vuot"):
                sang = (al > 110) & (lum > 170)
                sang = cv2.GaussianBlur(cv2.dilate(sang.astype(np.uint8), el(1.5 * S2)) * 255, (0, 0), 1.2 * S2) > 127
                can[sang & m] = C["vuot"]
                can[vien(sang, 2 * S2) & m] = INK
            can[vien(m, 3 * S2)] = INK
        elif nen == "lua":
            m = them_luoi(m, T0, SC, slot)
            to_lua(can, m)
        elif nen == "rau":
            to_lua(can, m, day=0.55)
        elif nen == "dao":
            V = np.array(a["xy"], float).reshape(-1, 2)
            chuoi, mui = (V[1] + V[2]) / 2, (V[0] + V[3]) / 2
            Ld = float(np.linalg.norm(mui - chuoi))
            ax = (mui - chuoi) / Ld
            song = np.array([-ax[1], ax[0]])                      # +y của xương wuqi_03: phía sống đao (lưỡi sắc ở −y: phía dẫn đầu cú chém)
            uvw = lambda P: T(np.array([chuoi + ax * (u * Ld) + song * (w * Ld) for u, w in P]))  # noqa: E731
            m = da_giac(shape, uvw(DAO_BAN), 2.0 * S2)
            can[m] = C["dao"]
            ml = da_giac(shape, uvw(DAO_LUOI), 1.5 * S2) & m
            can[ml] = LUA[1]
            can[vien(ml, 2 * S2) & m] = INK
            can[vien(m, 3 * S2)] = INK
            mc = da_giac(shape, uvw(DAO_CAN), 1.5 * S2)
            can[mc] = C["can"]
            can[vien(mc, 3 * S2)] = INK
            for u in (0.10, 0.18, 0.26):
                P = uvw([(u, 0.022), (u + 0.012, -0.022)]).astype(np.int32)
                cv2.line(can, tuple(P[0]), tuple(P[1]), INK, 2 * S2, cv2.LINE_AA)
            mg = da_giac(shape, uvw(DAO_CHAN), 2.0 * S2)
            can[mg] = C["dao_vanh"]
            can[vien(mg, 3 * S2)] = INK
            ku, kw, kr = DAO_KHAU
            kc = uvw([(ku, kw)])[0]
            cv2.circle(can, tuple(np.round(kc).astype(int)), int(kr * Ld * SC * S2), INK, -1, cv2.LINE_AA)
            cv2.circle(can, tuple(np.round(kc).astype(int)), int(kr * Ld * SC * S2 - 3 * S2), C["dao_vanh"], -1, cv2.LINE_AA)
            cv2.circle(can, tuple(np.round(kc).astype(int)), int(kr * Ld * SC * S2 * 0.48), INK, -1, cv2.LINE_AA)
            cv2.circle(can, tuple(np.round(kc).astype(int)), int(kr * Ld * SC * S2 * 0.48 - 2 * S2), (255, 255, 255), -1, cv2.LINE_AA)
            m = m | mc | mg
            p_mui, p_chuoi = uvw([(1.0, -0.062)])[0] / S2, uvw([(0.0, 0.0)])[0] / S2
            info["dao"] = dict(mui=[round(p_mui[0]), round(p_mui[1])], chuoi=[round(p_chuoi[0]), round(p_chuoi[1])],
                               chan=[round(x) for x in (uvw([(0.35, 0.0)])[0] / S2)], dai_px=round(Ld * SC),
                               khac=[round(x) for x in (uvw([(0.83, 0.10)])[0] / S2)])
            hop["ban_dao"] = ghi("_ban_dao", da_giac(shape, uvw(DAO_BAN)))
        elif nen in ("sung_gan", "sung_xa"):
            sp = SUNG_GAN if nen == "sung_gan" else SUNG_XA
            m = da_giac(shape, T(non(sp["p"], sp["w0"], sp["w1"], mu=0.85)), 1.5 * S2)
            can[m] = C["sung"]
            c = bezier(sp["p"], 40)
            mm = da_giac(shape, T(non([c[26], c[33], c[39]], sp["w0"] * 0.42, sp["w1"], mu=0.9)), 0) & m
            can[mm] = C["sung_mui"]
            can[vien(mm, 2 * S2) & m] = INK
            can[vien(m, 3 * S2)] = INK
            tip = T(np.array(sp["p"][2])) / S2
            info[nen] = dict(mui=[round(tip[0]), round(tip[1])], goc=[round(x) for x in (T(np.array(sp["p"][0])) / S2)])
        elif nen == "mat_na":
            m = da_giac(shape, T(np.array(MAT_NA, float)), 2.2 * S2)
            can[m] = C["mat_na"]
            P = T(np.array([(172, 462), (232, 446), (256, 452), (300, 440), (346, 452)], float)).astype(np.int32)   # gờ mày
            cv2.polylines(can, [P], False, INK, 3 * S2, cv2.LINE_AA)
            P = T(np.array([(256, 452), (262, 400)], float)).astype(np.int32)                                     # sống mũi
            cv2.polylines(can, [P], False, INK, 2 * S2, cv2.LINE_AA)
            tam = []
            for (ex, ey), (sg, xech) in MAT:
                e = np.array([(ex - sg * 24, ey + 2 - 0), (ex + sg * 22, ey + 26 * xech + 12), (ex + sg * 14, ey - 8)], float)
                me = da_giac(shape, T(e), 1.0 * S2)
                can[me] = LUA[2]
                can[vien(me, 2 * S2)] = INK
                tam.append([round(x) for x in (T(np.array([ex, ey])) / S2)])
            can[vien(m, 3 * S2)] = INK
            info["mat"] = tam
            mao = T(np.array([243, 648])) / S2
            info["mao"] = [round(mao[0]), round(mao[1])]
        elif nen == "giap_vai":
            mg = da_giac(shape, T(non(GIAP_GAI["p"], GIAP_GAI["w0"], GIAP_GAI["w1"], mu=0.8)), 1.5 * S2)
            can[mg] = C["giap"]
            can[vien(mg, 3 * S2)] = INK
            m = da_giac(shape, T(np.array(GIAP_VAI, float)), 9 * S2)
            can[m] = C["giap"]
            can[vien(m, 3 * S2)] = INK
            mv = da_giac(shape, T(np.array(GIAP_VANH, float)), 4 * S2)
            can[mv] = C["giap"]
            can[vien(mv, 3 * S2)] = INK
            cx, cy = T(np.array([-112.0, 440.0]))
            cv2.circle(can, (int(cx), int(cy)), int(34 * SC * S2), INK, 3 * S2, cv2.LINE_AA)
            m = m | mg | mv
            tip = T(np.array(GIAP_GAI["p"][2])) / S2
            info["giap_gai"] = [round(tip[0]), round(tip[1])]
        else:
            continue
        b = ghi(slot, m)
        for ten, sl in NHOM.items():
            if slot in sl:
                h = hop.get(ten)
                hop[ten] = b if h is None else [min(h[0], b[0]), min(h[1], b[1]), max(h[2], b[2]), max(h[3], b[3])]
        if nen in ("sung_gan", "sung_xa", "mat_na", "giap_vai", "dao"):
            hop[nen] = b
    im = Image.fromarray(can, "RGB").resize((W, H), Image.LANCZOS)
    os.makedirs(G.MAU, exist_ok=True)
    p = os.path.join(G.MAU, f"bo_cuc_{huong}.png")
    im.save(p)
    out = {k: [round(x) for x in v] for k, v in hop.items()}
    out.update(info)
    allb = np.array(list(info["slot"].values()))
    out["_khung"] = [int(allb[:, 0].min()), int(allb[:, 1].min()), int(allb[:, 2].max()), int(allb[:, 3].max())]
    out["_sc"] = round(SC, 4)
    g0 = T0(np.array([0.0, 0.0]))
    out["_goc"] = [round(float(g0[0]), 2), round(float(g0[1]), 2)]
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
