# -*- coding: utf-8 -*-
"""Khủng long núi lửa đảo Hỏa (nui_lua, concept "sừng" người dùng chốt 2026-11-14): MẢNH theo đúng khung từng part của rig gốc
monster_3654 (skill pokiclash-spine-rig mục 00). Dùng lại bộ máy của hoa_ho_manh.py (hình bóng, xếp ô, cắt tờ, đo IoU).

Mọi mảnh của con này là đá cứng có viền riêng → tất cả đi đường KHUNG PART: mỗi part một ô đúng khung ảnh vùng × z, hình bóng kín của
họ, bên trong tô phẳng theo THIẾT KẾ CỦA MÌNH (không lấy hoa văn của họ):
- ống núi lửa: tháp vòng đá xếp tầng: khe dung nham giữa các vòng, vành miệng cam có giọt chảy, lòng miệng vàng;
- đá thân, đá chân: một màu đá; chỗ họ để hở lòng đỏ (mép trong vỏ sườn) thành dung nham; bàn chân sau nhúng dung nham ở đáy;
- đỉnh lưng `P_beijia_03`: miệng núi lửa chính + sông dung nham chẻ ba; các phiến lưng khác đá sẫm;
- sọ trên: đá, con mắt vàng khe dọc vẽ sẵn (họ không có slot mắt bật), khối lòng miệng sẫm; hàm dưới, răng xa, móng: ngà;
- bốn tảng nhìn thấy ở sườn có núm xương ngà (đặt ở tâm phần KHÔNG bị che ở dáng đứng);
- HAI SỪNG HÚC ngà: mảnh THÊM (rig gốc không có), hình bóng tự dựng, bám xương sọ `bone9` (mau/sung.json).
BỎ: `shadow`, 6 cụm khói `P_yan_*`, mắt `P_yanjing_02` (họ không bật ở clip nào).

    nui_lua_manh.py nhom_part [tờ...]      tờ hướng dẫn mau/part_<tờ>.png + .json (+ mau/sung.json)
    nui_lua_manh.py cat_part <tờ|het> [ep] cắt tai_ve/N_<tờ>*.png → manh/part/<vùng>.png, in IoU
    nui_lua_manh.py so_part [tờ...]        tờ so mau/so_part.png (đỏ = thiếu, xanh lá = thừa)
    nui_lua_manh.py can_mau                cân màu đá giữa các tờ (chạy sau khi cắt xong mọi tờ)
    nui_lua_manh.py mat                    dán con mắt vẽ bằng mã lên manh/part/P_shagne_1.png (khi máy vẽ làm hỏng mắt)
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nui_lua as G0  # noqa: E402,F401  (đổi con của hoa_ho sang monster_3654 TRƯỚC khi nạp hoa_ho_manh)
import hoa_ho_manh as M  # noqa: E402
import nui_lua_bo_cuc as BC  # noqa: E402

G = M.G
W, H, INK = M.W, M.H, M.INK
MAU, TAI, MANH = M.MAU, M.TAI, M.MANH
el = M.el
PAL = dict(rock=(86, 80, 92), dark=(54, 50, 60), lava=(240, 120, 40), core=(250, 204, 80), bone=(228, 206, 164), mat=(250, 214, 70),
           sang=(255, 250, 236))
A_TL = 0.5                                   # px ảnh vùng của họ cho mỗi đơn vị rig

ONG = ["P_jiao_09", "P_jiao_10", "P_jiao_02", "P_jiao_14", "P_jiao_13", "P_jiao_15", "P_jiao_03", "P_jiao_04", "P_jiao_06",
       "P_jiao_07", "P_jiao_01", "P_jiao_11", "P_jiao_12"]
ONG_CHAN = ["P_qiantuiR5", "P_qiantuiR1"]    # mảnh chân có một ống núi lửa: chỗ miệng dò theo ảnh của họ
SUNG = ["sung_gan", "sung_xa"]
TO = {
    "O1": ["P_jiao_09", "P_jiao_10", "P_jiao_02", "P_jiao_14", "P_jiao_13"],
    "O2": ["P_jiao_15", "P_jiao_03", "P_jiao_04", "P_jiao_06", "P_jiao_07", "P_jiao_01", "P_jiao_11", "P_jiao_12", "P_jiao_08",
           "P_jiao_16"],
    "L": ["P_beijia_03", "P_beijia_05", "P_beijia_02", "P_beijia_04", "P_beijia_01", "P_beijia_06"],
    "D": ["P_shagne_1", "P_xiae_1", "P_xiae_2", "P_houlong", "sung_gan", "sung_xa", "P_jiaozhi_01", "P_jiaozhi_02"],
    "B": ["P_duzi", "P_duzi_01", "P_duzi_02", "P_duzi_03", "P_duzi_04", "P_duzi_05", "P_duzi_06"],
    "C1": ["P_qiantuiR1", "P_qiantuiR2", "P_qiantuiR3", "P_qiantuiR4", "P_qiantuiR5", "P_houtuiR1", "P_houtuiR2", "P_houtuiR3",
           "P_houtuiR4", "P_houtuiR5"],
    "C2": ["P_qiantuiL_01", "P_qiantuiL_02", "P_qiantuiL_03", "P_houtuiL_01", "P_houtuiL_02", "P_houtuiL_03"],
    # tờ SỬA sau khi soi rig lần đầu (17:30): sọ bỏ hai miệng ống (đọc nhầm thành hai con mắt), bốn tảng sườn đổi núm tam giác thành gai xương
    "S": ["P_shagne_1", "P_houtuiR5", "P_qiantuiR4", "P_qiantuiR3", "P_duzi_02"],
}
NHUNG = ("P_houtuiR1", "P_houtuiL_01")       # bàn chân sau: đáy nhúng dung nham
LONG_DO = ("P_duzi", "P_houtuiL_02", "P_houtuiR2", "P_houtuiR4")           # họ tô đỏ cả mảnh (lòng dung nham lộ ở khe)
VO = ("P_duzi_01", "P_duzi_02", "P_duzi_03", "P_duzi_04", "P_duzi_05", "P_duzi_06", "P_houtuiR3", "P_houtuiL_03")   # vỏ có mép trong đỏ
NUM = ("P_houtuiR5", "P_qiantuiR4", "P_qiantuiR3", "P_duzi_02")            # tảng sườn có núm xương
# sừng: đường tâm Bézier bậc hai trên khung sơ đồ 1536x1024 (gốc, điểm kéo, mũi) và bề dày ở gốc (px sơ đồ)
SUNG_DUONG = {"sung_gan": ((1172, 664), (1296, 662), (1350, 512), 66), "sung_xa": ((1128, 584), (1250, 580), (1296, 448), 52)}
SUNG_XUONG = "bone9"

M.TO, M.NHOM, M.TO_LIEN = TO, {}, {}


# ---------------------------------------------------------------- toạ độ: sơ đồ ↔ thế giới (dáng idle0) ↔ ô của part
_I0 = {}


def idle0():
    if not _I0:
        D0 = json.load(open(os.path.join(G.scan(), "att_idle0.json"), encoding="utf-8"))
        _I0["bones"] = {b["name"]: b for b in D0["bones"]}
        _I0["atts"] = {}
        for a in D0["atts"]:
            if a.get("region") and a.get("cur") and "uv" in a:
                _I0["atts"].setdefault(a["region"], a)
        _I0["hh"] = json.load(open(os.path.join(MAU, "bo_cuc.json"), encoding="utf-8"))
    return _I0


def so_do_tg(p):
    """điểm trên sơ đồ bố cục (px) → thế giới ở dáng idle0."""
    hh = idle0()["hh"]
    p = np.asarray(p, float)
    return np.stack([(p[..., 0] - hh["_ox"]) / hh["_sc"], (hh["_oy"] - p[..., 1]) / hh["_sc"]], -1)


def tg_o(ten, w, h):
    """ma trận afin thế giới idle0 → px ô của part (bình phương tối thiểu trên lưới; part cứng một xương thì khít)."""
    a = idle0()["atts"][ten]
    U = np.array(a["uv"], float).reshape(-1, 2) * np.array([w, h])
    V = np.array(a["xy"], float).reshape(-1, 2)
    A, *_ = np.linalg.lstsq(np.c_[V, np.ones(len(V))], U, rcond=None)
    return A


def so_do_o(ten, p, w, h):
    q = so_do_tg(p)
    return np.c_[q.reshape(-1, 2), np.ones(q.reshape(-1, 2).shape[0])] @ tg_o(ten, w, h)


def ti_o(ten, w, h):
    """px ô cho mỗi px sơ đồ (trung bình hai chiều)."""
    A = tg_o(ten, w, h)[:2]
    return float(math.sqrt(abs(np.linalg.det(A)))) / idle0()["hh"]["_sc"]


# ---------------------------------------------------------------- sừng (mảnh thêm)
_S = {}


def sung_hinh():
    """hình bóng hai sừng ở thế giới idle0: đa giác quanh đường tâm Bézier, dày ở gốc, nhọn ở mũi."""
    if _S:
        return _S
    b9 = idle0()["bones"][SUNG_XUONG]
    Wb = np.array([[b9["a"], b9["b"], b9["x"]], [b9["c"], b9["d"], b9["y"]], [0, 0, 1.0]])
    Wi = np.linalg.inv(Wb)
    for ten, (p0, p1, p2, day) in SUNG_DUONG.items():
        u = np.linspace(0, 1, 40)[:, None]
        C = (1 - u) ** 2 * np.array(p0, float) + 2 * u * (1 - u) * np.array(p1, float) + u ** 2 * np.array(p2, float)
        d = np.gradient(C, axis=0)
        n = np.stack([-d[:, 1], d[:, 0]], 1) / np.maximum(1e-6, np.linalg.norm(d, axis=1))[:, None]
        r = 0.5 * day * (1 - u[:, 0]) ** 0.72 * np.minimum(1.0, (u[:, 0] + 0.012) / 0.07) ** 0.5     # gốc bo tròn, mũi nhọn
        poly = np.concatenate([C + n * r[:, None], (C - n * r[:, None])[::-1]])
        Pw = so_do_tg(poly)
        x0, y0, x1, y1 = Pw[:, 0].min() - 8, Pw[:, 1].min() - 8, Pw[:, 0].max() + 8, Pw[:, 1].max() + 8
        loc = (np.c_[Pw, np.ones(len(Pw))] @ Wi.T)[:, :2]
        _S[ten] = dict(poly=Pw, tam=so_do_tg(C), hop=(x0, y0, x1, y1), local=loc)
    return _S


def sung_o(ten, z, p=None):
    """điểm thế giới → px ô của sừng (p=None: đa giác hình bóng)."""
    s = sung_hinh()[ten]
    x0, y0, x1, y1 = s["hop"]
    q = s["poly"] if p is None else np.asarray(p, float)
    return np.stack([(q[:, 0] - x0) * A_TL * z, (y1 - q[:, 1]) * A_TL * z], 1)


_co_o_goc = M.co_o


def co_o(ten, z):
    if ten in SUNG:
        x0, y0, x1, y1 = sung_hinh()[ten]["hop"]
        return int(round((x1 - x0) * A_TL * z)), int(round((y1 - y0) * A_TL * z))
    return _co_o_goc(ten, z)


M.co_o = co_o
_bong_goc = M.bong


def bong(ten, z):
    if ten in SUNG:
        w, h = co_o(ten, z)
        m = np.zeros((h, w), np.uint8)
        cv2.fillPoly(m, [np.round(sung_o(ten, z)).astype(np.int32)], 1)
        return m.astype(bool)
    return _bong_goc(ten, z)


def by():
    B = M.by()
    for ten in SUNG:
        if ten not in B:                      # mục giả để cat_part kẻ nét mực theo mép hình bóng
            x0, y0, x1, y1 = sung_hinh()[ten]["hop"]
            P = sung_hinh()[ten]["poly"]
            uv = np.stack([(P[:, 0] - x0) / (x1 - x0), (y1 - P[:, 1]) / (y1 - y0)], 1)
            B[ten] = {"uv": uv.ravel().tolist(), "hull": len(P), "region": ten}
    return B


# ---------------------------------------------------------------- dò trên ảnh của họ
def do_goc(ten, z):
    """mặt nạ theo màu ảnh part của họ: (đỏ, lòng miệng núi lửa màu đào, rất tối)."""
    s = M.nguon(ten, z)
    a = s[..., 3] > 100
    R, Gc, Bc = s[..., 0], s[..., 1], s[..., 2]
    dao = a & (R > 200) & (Gc > 110)
    do = a & (R - Gc > 45) & (R > 85) & ~dao
    toi = a & (np.maximum(np.maximum(R, Gc), Bc) < 48)
    return do, dao, toi


def lon_nhat(m, mo=0.0, dong=0.0):
    m = m.astype(np.uint8)
    if mo:
        m = cv2.morphologyEx(m, cv2.MORPH_OPEN, el(mo))
    if dong:
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, el(dong))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    if n < 2:
        return np.zeros(m.shape, bool)
    return lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))


_NUM = {}


def cho_num():
    """tâm phần KHÔNG bị che (dáng idle0) của các tảng có núm xương → toạ độ sơ đồ."""
    if _NUM:
        return _NUM
    SC, ox, oy, T = BC.khung_T()
    chu = None
    ds = []
    for a in BC.atts_dung():
        m = BC.B.bong(a, T, 3.0)
        if chu is None:
            chu = np.full(m.shape, -1, np.int32)
        chu[m] = len(ds)
        ds.append(a["region"] if a["slot"] != "P_beijia_07" else "_")
    for ten in NUM:
        if ten not in ds:
            continue
        v = (chu == ds.index(ten)).astype(np.uint8)
        d = cv2.distanceTransform(v, cv2.DIST_L2, 5)
        if d.max() < 12 * BC.S2:
            continue
        y, x = np.unravel_index(d.argmax(), d.shape)
        _NUM[ten] = (x / BC.S2, y / BC.S2)
    G._C.pop("att", None)
    return _NUM


# ---------------------------------------------------------------- thiết kế từng part
def truc_ong(ten, m, z):
    """(điểm trên trục gần miệng, vectơ đơn vị gốc → miệng) trong ô."""
    h, w = m.shape
    ys, xs = np.nonzero(m)
    tam = np.array([xs.mean(), ys.mean()])
    if ten in ONG_CHAN:
        _, dao, _ = do_goc(ten, z)
        dao = lon_nhat(dao, mo=0.6 * z)
        py, px = np.nonzero(dao)
        pm = np.array([px.mean(), py.mean()])
        a = pm - tam
    else:
        o = idle0()["hh"]["ong"][ten[-2:]]
        q = so_do_o(ten, np.array([o["mieng"], o["day"]], float), w, h)
        pm, a = q[0], q[0] - q[1]
    return pm, a / max(1e-6, np.linalg.norm(a))


def thiet_ke(ten, z):
    """THIẾT KẾ CỦA MÌNH cho một part, vẽ phẳng bằng mã trong đúng khung ảnh vùng của part (× z). Trả (RGB nền trắng, mặt nạ)."""
    m = bong(ten, z)
    h, w = m.shape
    im = np.full((h, w, 3), 255, np.uint8)
    nt = M.net(m, z)
    trong = cv2.erode(m.astype(np.uint8), el(nt)).astype(bool)
    ys, xs = np.mgrid[0:h, 0:w]

    def ranh(mm):
        im[cv2.morphologyEx(mm.astype(np.uint8), cv2.MORPH_GRADIENT, el(0.5 * nt)).astype(bool) & trong] = INK

    def to(mm, mau, vien=True):
        mm = mm & m
        im[mm] = PAL[mau]
        if vien:
            ranh(mm)

    if ten in ONG or ten in ONG_CHAN:
        im[m] = PAL["rock"]
        pm, a = truc_ong(ten, m, z)
        dx, dy = xs - pm[0], ys - pm[1]
        t = dx * a[0] + dy * a[1]
        s = -dx * a[1] + dy * a[0]
        t1, t0 = t[m].max(), t[m].min()
        L = t1 - t0
        wm = float(np.abs(s[m & (t > t1 - 0.2 * L)]).max())
        tc = t + 0.035 * L * (1 - np.clip(s / wm, -1, 1) ** 2)       # đường ngang hơi võng về phía gốc ở giữa (vòng nhìn từ trên)
        vanh = min(0.16 * L, 0.55 * wm)
        lava = tc > t1 - vanh                                         # vành miệng
        for s0, dai, rong in ((-0.5, 0.6, 0.20), (0.08, 1.05, 0.24), (0.58, 0.45, 0.18)):   # giọt chảy từ vành xuống
            tau = ((t1 - vanh) - tc) / (dai * vanh)
            lava |= (tau >= 0) & (tau <= 1) & (np.abs(s - s0 * wm) < rong * wm * (1 - 0.75 * tau))
        day = t1 - 2.2 * vanh                                         # dưới các giọt: thân tháp
        khe = (0.38, 0.70) if L > 3.2 * wm else ((0.55,) if L > 1.9 * wm and ten in ONG else ())
        day_khe = max(2.2 * z, 0.016 * L)
        for f in khe:                                                 # khe dung nham giữa các vòng đá
            lava |= np.abs(tc - (t0 + f * (day - t0))) < day_khe
        to(lava, "lava")
        cy = t1 - 0.5 * vanh
        to(((tc - cy) / (0.38 * vanh)) ** 2 + (s / (0.6 * wm)) ** 2 < 1, "core")
    elif ten in SUNG:
        im[m] = PAL["bone"]
        C = sung_o(ten, z, sung_hinh()[ten]["tam"])
        for f in (0.10, 0.20, 0.31, 0.43):                           # bốn rãnh vòng gần gốc
            i = int(f * (len(C) - 1))
            d = C[i + 1] - C[i]
            n = np.array([-d[1], d[0]]) / max(1e-6, np.linalg.norm(d))
            r = 0.5 * SUNG_DUONG[ten][3] * A_TL * z / idle0()["hh"]["_sc"]
            g = np.zeros((h, w), np.uint8)
            cv2.line(g, tuple(np.round(C[i] - n * r).astype(int)), tuple(np.round(C[i] + n * r).astype(int)), 1,
                     max(2, int(round(0.55 * nt))))
            im[g.astype(bool) & trong] = INK
    elif ten == "P_beijia_03":
        im[m] = PAL["dark"]
        k = ti_o(ten, w, h)
        tam, ban = BC.MIENG_CHINH
        c = so_do_o(ten, np.array([tam, (tam[0] + 10, tam[1]), (tam[0], tam[1] + 10)], float), w, h)
        goc = math.degrees(math.atan2(c[1][1] - c[0][1], c[1][0] - c[0][0]))
        song = np.zeros((h, w), np.uint8)
        for duong, day in (([(775, 178), (800, 240), (822, 300)], 34), ([(822, 300), (812, 350), (800, 395)], 24),
                           ([(822, 300), (836, 355), (842, 405)], 22), ([(808, 262), (846, 318), (868, 365)], 20)):
            q = np.round(so_do_o(ten, np.array(duong, float), w, h)).astype(np.int32)
            cv2.polylines(song, [q], False, 1, max(3, int(round(day * k))), cv2.LINE_8)
            for p_ in q:
                cv2.circle(song, tuple(int(v) for v in p_), max(2, int(round(day * k / 2))), 1, -1)
        vanh = np.zeros((h, w), np.uint8)
        cv2.ellipse(vanh, (int(c[0][0]), int(c[0][1])), (int((ban[0] + 14) * k), int((ban[1] + 9) * k)), goc, 0, 360, 1, -1)
        to(song.astype(bool) | vanh.astype(bool), "lava")
        loi = np.zeros((h, w), np.uint8)
        cv2.ellipse(loi, (int(c[0][0]), int(c[0][1])), (int(ban[0] * k), int(ban[1] * k)), goc, 0, 360, 1, -1)
        to(loi.astype(bool), "core")
    elif ten.startswith("P_beijia"):
        im[m] = PAL["dark"]
    elif ten in LONG_DO:
        im[m] = PAL["lava"]
    elif ten == "P_houlong":
        im[m] = PAL["lava"]
        to(M.loi(m, 0.42) & trong, "core")
    elif ten in ("P_xiae_1", "P_xiae_2", "P_jiaozhi_01", "P_jiaozhi_02"):
        im[m] = PAL["bone"]
    elif ten == "P_shagne_1":
        im[m] = PAL["rock"]
        _, _, toi = do_goc(ten, z)
        to(lon_nhat(toi, mo=1.5 * z, dong=2.0 * z), "dark")          # khối lòng miệng sau hàm răng
        ve_mat(im, ten, w, h, trong)
    else:
        im[m] = PAL["rock"]
        if ten in VO:                                                 # mép trong của vỏ: lòng dung nham
            s_ = M.nguon(ten, z)                                      # mép đỏ của họ rất sẫm: ngưỡng thấp hơn do_goc
            do = (s_[..., 3] > 100) & (s_[..., 0] - s_[..., 1] > 20) & (s_[..., 0] > 50)
            do = cv2.morphologyEx(do.astype(np.uint8), cv2.MORPH_OPEN, el(1.0 * z))
            do = cv2.GaussianBlur(cv2.morphologyEx(do, cv2.MORPH_CLOSE, el(2.5 * z)) * 255, (0, 0), 1.2 * z) > 127
            if do.sum() > 0.04 * m.sum():
                to(do, "lava")
        if ten in NHUNG:                                              # đáy bàn chân sau nhúng dung nham (mép trên răng cưa)
            A = tg_o(ten, w, h)[:2]
            xuong = np.array([0.0, -1.0]) @ A
            xuong /= np.linalg.norm(xuong)
            ngang = np.array([-xuong[1], xuong[0]])
            d = xs * xuong[0] + ys * xuong[1]
            n = xs * ngang[0] + ys * ngang[1]
            d1, d0 = d[m].max(), d[m].min()
            cua = 0.035 * (d1 - d0) * (2 * np.abs(((n / (0.11 * (d1 - d0))) % 1.0) - 0.5))
            to(d > d1 - 0.16 * (d1 - d0) - cua, "lava")
        if ten in NUM and ten in cho_num():                           # núm xương: gai ngà nhỏ chĩa lên
            k = ti_o(ten, w, h)
            c = cho_num()[ten]
            gai = [(-20, 14), (-17, 2), (-12, -12), (-6, -24), (1, -34), (5, -22), (10, -8), (17, 5), (21, 14), (10, 18), (-9, 18)]
            q = so_do_o(ten, np.array([(c[0] + x_, c[1] + y_) for x_, y_ in gai], float), w, h)   # gai xương cong, ngả về phía sau
            g = np.zeros((h, w), np.uint8)
            cv2.fillPoly(g, [np.round(q).astype(np.int32)], 1)
            g = cv2.dilate(g, el(1.0 * k))
            to(g.astype(bool) & trong, "bone")
    im[m & ~trong] = INK
    im[~m] = 255
    return im, m


def mat_hinh(ten, w, h, S=1):
    """con mắt trong ô sọ: (tâm, bán trục dài, bán trục ngắn, góc độ) theo px ô × S."""
    hh = idle0()["hh"]
    q = so_do_o(ten, np.array([hh["mat"], (hh["mat"][0] + 10, hh["mat"][1] + 6)], float), w, h)
    k = ti_o(ten, w, h)
    goc = math.degrees(math.atan2(q[1][1] - q[0][1], q[1][0] - q[0][0]))
    return (q[0] * S), 27 * k * S, 15 * k * S, goc


def ve_mat(im, ten, w, h, trong=None, S=1):
    """mắt xếch: hốc mực, mống vàng, con ngươi khe dọc, một chấm sáng nhỏ."""
    c, a, b, goc = mat_hinh(ten, w, h, S)
    ci = (int(round(c[0])), int(round(c[1])))
    lop = np.zeros(im.shape[:2], np.uint8)
    cv2.ellipse(lop, ci, (int(a), int(b)), goc, 0, 360, 1, -1, cv2.LINE_AA)
    if trong is not None:
        lop &= trong.astype(np.uint8)
    im[lop.astype(bool), :3] = INK
    mong = np.zeros(im.shape[:2], np.uint8)
    cv2.ellipse(mong, ci, (int(a * 0.72), int(b * 0.66)), goc, 0, 360, 1, -1, cv2.LINE_AA)
    im[mong.astype(bool) & lop.astype(bool), :3] = PAL["mat"]
    cv2.ellipse(im, ci, (max(1, int(a * 0.13)), int(b * 0.62)), goc, 0, 360, INK, -1, cv2.LINE_AA)
    r = math.radians(goc)
    cv2.circle(im, (int(c[0] - math.cos(r) * a * 0.36 + math.sin(r) * b * 0.2), int(c[1] - math.sin(r) * a * 0.36 - math.cos(r) * b * 0.2)),
               max(1, int(b * 0.18)), PAL["sang"], -1, cv2.LINE_AA)
    return lop.astype(bool)


def loai(ten):
    """loại hình của một ô (để file prompt tả cho máy vẽ)."""
    if ten in ONG:
        return "ong"
    if ten in ONG_CHAN:
        return "ong_chan"
    if ten in SUNG:
        return "sung"
    if ten == "P_beijia_03":
        return "dinh"
    if ten.startswith("P_beijia"):
        return "lung"
    if ten in LONG_DO:
        return "long"
    if ten in VO:
        return "vo_num" if ten in NUM else "vo"
    if ten in NHUNG:
        return "chan_nhung"
    if ten in NUM:
        return "da_num"
    return {"P_houlong": "hong", "P_xiae_1": "ham", "P_xiae_2": "rang_xa", "P_jiaozhi_01": "mong", "P_jiaozhi_02": "mong",
            "P_shagne_1": "so"}.get(ten, "da")


def nhom_part(chi=None):
    os.makedirs(MAU, exist_ok=True)
    by()
    for to_, ds in TO.items():
        if chi and to_ not in chi:
            continue
        z = 8.0
        while M.xep(ds, z) is None:
            z = round(z - 0.1, 2)
        cho = M.xep(ds, z)
        im = np.full((H, W, 3), 255, np.uint8)
        khung = {}
        for ten in ds:
            x, y, w, h = cho[ten]
            cell, _ = thiet_ke(ten, z)
            im[y:y + h, x:x + w] = cell[:h, :w]
            khung[ten] = {"x": x, "y": y, "w": w, "h": h, "z": z}
        Image.fromarray(im).save(os.path.join(MAU, f"part_{to_}.png"))
        json.dump(khung, open(os.path.join(MAU, f"part_{to_}.json"), "w", encoding="utf-8"), indent=1)
        print(f"{to_} (x{z}, nét ~{M.NET * z:.0f} px): " + ", ".join(f"{k} {v['w']}x{v['h']}@{v['x'] + v['w'] // 2},{v['y'] + v['h'] // 2}"
                                                                    for k, v in khung.items()))
    S = sung_hinh()
    json.dump({t: dict(hop=[float(v) for v in S[t]["hop"]], local=S[t]["local"].tolist(), xuong=SUNG_XUONG) for t in SUNG},
              open(os.path.join(MAU, "sung.json"), "w", encoding="utf-8"), indent=1)


def can_mau(chuan=("O1", "O2"), bo=("L",)):
    """cân màu ĐÁ giữa các tờ (mỗi lượt vẽ ra một sắc xám hơi khác): đưa màu đá trung bình của từng tờ về màu của các tờ ống.
    Chỉ đụng điểm ảnh họ đá (xám, sáng vừa); mực, dung nham, ngà, đá sẫm của tờ lưng giữ nguyên."""
    ra = os.path.join(MANH, "part")

    def ho_da(c):
        c = c.astype(np.float32)
        mx, mn = c[..., :3].max(-1), c[..., :3].min(-1)
        lum = c[..., :3].mean(-1)
        w = np.clip((lum - 52) / 22, 0, 1) * np.clip((165 - lum) / 25, 0, 1) * np.clip((62 - (mx - mn)) / 16, 0, 1)
        return w * (c[..., 3] > 127)

    tb = {}
    for to_, ds in TO.items():
        if to_ in bo:
            continue
        tong, n = np.zeros(3), 0.0
        for ten in ds:
            p = os.path.join(ra, ten + ".png")
            if not os.path.exists(p) or (to_ != "S" and ten in TO.get("S", ())):
                continue
            c = np.asarray(Image.open(p).convert("RGBA"))
            w = ho_da(c)
            tong += (c[..., :3] * w[..., None]).sum((0, 1))
            n += w.sum()
        if n > 500:
            tb[to_] = tong / n
    dich = np.mean([tb[t] for t in chuan if t in tb], axis=0)
    print("màu đá đích", dich.round(1))
    for to_, m in tb.items():
        g = dich / m
        if to_ in chuan or np.abs(g - 1).max() < 0.012:
            print(f"  {to_}: {m.round(1)} giữ")
            continue
        for ten in TO[to_]:
            p = os.path.join(ra, ten + ".png")
            if not os.path.exists(p) or (to_ != "S" and ten in TO.get("S", ())):
                continue
            c = np.asarray(Image.open(p).convert("RGBA")).astype(np.float32)
            w = ho_da(c)[..., None]
            c[..., :3] = np.clip(c[..., :3] * (1 + (g - 1) * w), 0, 255)
            Image.fromarray(c.astype(np.uint8), "RGBA").save(p)
        print(f"  {to_}: {m.round(1)} × {g.round(3)}")


def zs():
    out = M.zs()
    out.pop("P_biyan", None)
    return out


def mat():
    """dán con mắt vẽ bằng mã lên ảnh sọ đã cắt (đúng chỗ của tờ hướng dẫn)."""
    ten = "P_shagne_1"
    p = os.path.join(MANH, "part", ten + ".png")
    im = np.asarray(Image.open(p).convert("RGBA")).copy()
    h, w = im.shape[:2]
    S = 4
    big = cv2.resize(im, (w * S, h * S), interpolation=cv2.INTER_LINEAR)
    rgb = np.ascontiguousarray(big[..., :3])
    lop = ve_mat(rgb, ten, w, h, None, S)
    big[..., :3] = rgb
    big[..., 3][lop] = 255
    Image.fromarray(big, "RGBA").resize((w, h), Image.LANCZOS).save(p)
    print("mắt →", p)


def main(a):
    lenh = a[0] if a else ""
    if lenh == "nhom_part":
        nhom_part(a[1:] or None)
    elif lenh == "cat_part":
        by()
        for to_ in (a[1].split(",") if len(a) > 1 and a[1] != "het" else list(TO)):
            M.cat_part(to_, ep=len(a) > 2)
    elif lenh == "so_part":
        M.so_part(a[1:] or None)
    elif lenh == "mat":
        mat()
    elif lenh == "can_mau":
        can_mau()
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
