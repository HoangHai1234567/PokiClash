# -*- coding: utf-8 -*-
"""Dòng tm05 (Sò Ngọc) của lô 10 tướng mới đảo Thủy: Sò Gai (dạng 1, chibi) và Bạng Vương (dạng 2, dạng cuối).
Rig dựng bằng mã trên thư viện quai/ (README mục 5), học nhịp từ con gốc monster_3237 (inbox/tm05_ghichu.md).

    py -3 -I ArtGen/Spine/tm05.py cat 2          cắt tờ M01..M03 vào inbox/tm05_2/manh (+ _soi.png)
    py -3 -I ArtGen/Spine/tm05.py dat 2          ảnh đặt mảnh khung 0 chồng concept (soi chỗ đặt)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm05.py rig 2     dựng + xuất dạng 2
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm05.py rig 1     dựng dạng 1 + gộp dạng 2 (evolve)

Cấu tạo (cả hai dạng): nửa trên (vỏ trên + thân mềm có mắt + môi trên; vỏ cứng, mặt và môi là vùng mềm), nửa dưới (vỏ dưới +
môi dưới), lòng miệng là màng nối hai vỏ nằm khuất sau hai nửa vỏ (vỏ khép kín được), ngọc trai (và lưỡi ở dạng 2) theo vỏ dưới,
mỗi gai một xương có lò xo, xúc tu / chân là dải lưới nhiều đốt uốn theo đường cong, mí phủ dò bằng fit_lid.
"""
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

from quai import anh, hoat, khung, luoi, mieng, soi, tienhoa, trongso, xuat  # noqa: E402
from quai.hoat import Clip, DayMem, LoXo, an_hien, bao, chuoi_song, cv, ease, lui, rung, song  # noqa: E402
from quai.khung import Dat  # noqa: E402

INBOX = os.path.join(HERE, "inbox")
CODE = "tm05"


def thu_muc(k, *p):
    return os.path.join(INBOX, f"{CODE}_{k}", *p)


# ------------------------------------------------------------------ cấu hình theo concept (toạ độ px ảnh concept, y xuống)
IND, TEAL, BRASS = (35, 42, 102), (21, 130, 127), (201, 146, 60)
SLATE, TURQ = (61, 92, 156), (54, 194, 180)
CFG = {
    2: dict(
        S=0.45, O=(740, 985), dinh=16,
        tren_box=(410, 180, 1168, 472), duoi_box=(412, 495, 1072, 798),
        H=(440, 500),
        U=[(470, 488), (600, 455), (760, 428), (900, 410), (1040, 398)],        # môi trên (chân hàng răng trên)
        D=[(470, 515), (600, 560), (760, 600), (900, 622), (1040, 640)],        # môi dưới (chân hàng răng dưới)
        mat_c=(978, 316),
        mat=[(905, 300), (1075, 300)],                                           # tâm mắt gần, mắt xa
        gai=[("gt0", "vo_tren", (515, 318), (360, 282)), ("gt1", "vo_tren", (575, 262), (412, 178)),
             ("gt2", "vo_tren", (660, 215), (500, 96)), ("gt3", "vo_tren", (775, 190), (630, 28)),
             ("gt4", "vo_tren", (880, 180), (860, 66)),
             ("gd0", "vo_duoi", (470, 625), (328, 662)), ("gd1", "vo_duoi", (485, 690), (362, 727)),
             ("gd2", "vo_duoi", (525, 748), (432, 792))],
        chan=[  # tên, ảnh, đường gốc → ngọn (concept), cha, số đốt, đổi mặt giác bám
            ("cbs", "chan_b", [(575, 760), (470, 820), (390, 870), (330, 905), (300, 880)], -1),
            ("cbt", "chan_a", [(665, 770), (615, 850), (580, 920), (555, 965), (585, 975)], -1),
            ("cfs", "chan_b", [(800, 770), (800, 850), (795, 920), (790, 960), (825, 965)], 1),
            ("cft", "chan_a", [(905, 760), (990, 830), (1070, 890), (1135, 945), (1160, 920)], 1)],
        luoi=[(640, 588), (760, 600), (880, 612), (1010, 618)],
        ngoc=((880, 535), 220),
        mien=((930, 228), 230),
        xt=[("xta", "xt_a", [(1035, 470), (1085, 455), (1120, 470), (1110, 500)], "vo_tren", 1),
            ("xtb", "xt_b", [(1030, 610), (1080, 600), (1115, 585), (1105, 560)], "vo_duoi", -1)],
        mieng=((995, 528), 0.0),
    ),
    1: dict(
        S=0.52, O=(760, 822), dinh=165,
        tren_box=(405, 250, 1045, 615), duoi_box=(415, 585, 1012, 772),
        H=(440, 555),
        U=[(455, 560), (560, 596), (665, 612), (780, 566), (880, 542), (968, 524)],
        D=[(455, 568), (560, 603), (665, 620), (780, 614), (880, 612), (978, 600)],
        mat_c=(908, 468),
        mat=[(888, 470), (962, 452)],
        gai=[("gt0", "vo_tren", (478, 380), (405, 355)), ("gt1", "vo_tren", (552, 312), (500, 262)),
             ("gt2", "vo_tren", (655, 285), (640, 210)), ("gt3", "vo_tren", (800, 268), (810, 172)),
             ("gt4", "vo_tren", (925, 300), (960, 235)),
             ("gd0", "vo_duoi", (540, 728), (505, 790)), ("gd1", "vo_duoi", (632, 755), (615, 805))],
        chan=[("chan", "chan", [(760, 700), (790, 760), (830, 800), (890, 815), (935, 808)], 1)],
        ngoc=((862, 600), 92),
        xt=[("xta", "xt_a", [(990, 505), (1050, 470), (1110, 465), (1135, 450)], "vo_tren", 1),
            ("xtb", "xt_b", [(995, 525), (1060, 515), (1120, 520), (1150, 510)], "vo_duoi", 1),
            ("xtc", "xt_c", [(990, 545), (1045, 560), (1090, 585), (1100, 610)], "vo_duoi", -1)],
        mieng=((985, 560), 8.0),
    ),
}

# hình giữ chỗ (cỡ theo tờ GPT) khi chưa có ảnh
GIU = {
    2: {"tren": ("bo", 690, 440, IND), "duoi": ("bo", 660, 320, IND), "long": ("mieng", 440, 320, (158, 46, 77)),
        "luoi": ("luoi", 400, 90, TEAL), "ngoc": ("tron", 220, 220, (239, 234, 247)), "mien": ("giot", 210, 150, BRASS),
        "mi_a": ("mi", 130, 80, TEAL), "mi_b": ("mi", 110, 70, TEAL), "xt_a": ("dai", 260, 60, TEAL), "xt_b": ("dai", 210, 50, TEAL),
        "chan_a": ("dai", 760, 125, TEAL), "chan_b": ("dai", 680, 105, TEAL),
        **{f"g{i}": ("giot", 110, h, (210, 73, 58)) for i, h in enumerate((320, 290, 260, 220, 180, 130, 110, 95))}},
    1: {"tren": ("bo", 640, 360, SLATE), "duoi": ("bo", 600, 280, SLATE), "long": ("mieng", 380, 260, (184, 58, 90)),
        "ngoc": ("tron", 130, 130, (245, 240, 230)), "mi_a": ("mi", 150, 110, TURQ), "mi_b": ("mi", 125, 95, TURQ),
        "chan": ("dai", 330, 130, (126, 216, 203)), "xt_a": ("dai", 300, 34, TURQ), "xt_b": ("dai", 260, 30, TURQ),
        "xt_c": ("dai", 220, 28, TURQ), **{f"g{i}": ("giot", 85, h, (240, 127, 85)) for i, h in enumerate((190, 180, 170, 160, 150, 120, 110))}},
}
GAI_ANH = {2: ["g0", "g1", "g2", "g3", "g4", "g5", "g6", "g7"], 1: ["g0", "g1", "g2", "g3", "g4", "g5", "g6"]}


# ------------------------------------------------------------------ cắt tờ
def _o(to, R, C):
    """nhóm mảnh theo ô lưới R×C: {(r, c): [mảnh...]}."""
    out = {}
    for m in to.manh:
        cx, cy = (m["x0"] + m["x1"]) / 2, (m["y0"] + m["y1"]) / 2
        out.setdefault((min(R - 1, int(cy / (to.h / R))), min(C - 1, int(cx / (to.w / C)))), []).append(m)
    return out


def cat(k):
    tv, ra = thu_muc(k, "tai_ve"), thu_muc(k, "manh")
    names = {}
    p1 = anh.to_moi_nhat(tv, "M01")
    if p1:
        to = anh.doc_to(p1)
        g = anh.gan_theo_o(to, [["tren", "duoi"]])
        anh.luu_manh(to, g, ra)
        names.update(g)
    p2 = anh.to_moi_nhat(tv, "M02")
    if p2:
        to = anh.doc_to(p2)
        o = _o(to, 2, 3)
        big = lambda L: max(L, key=lambda m: m["dt"])  # noqa: E731
        g = {}
        if k == 2:
            for (r, c), nm in (((0, 0), "long"), ((0, 1), "luoi"), ((0, 2), "ngoc"), ((1, 0), "mien")):
                if o.get((r, c)):
                    g[nm] = big(o[(r, c)])
            if o.get((1, 1)):
                g.update(anh.gan_theo_thu_tu(sorted(o[(1, 1)], key=lambda m: -m["dt"])[:2], ["mi_a", "mi_b"], "x"))
            if o.get((1, 2)):
                g.update(anh.gan_theo_thu_tu(sorted(o[(1, 2)], key=lambda m: -m["dt"])[:2], ["xt_a", "xt_b"], "y"))
        else:
            for (r, c), nm in (((0, 0), "long"), ((0, 1), "ngoc"), ((0, 2), "chan")):
                if o.get((r, c)):
                    g[nm] = big(o[(r, c)])
            if o.get((1, 0)):
                g.update(anh.gan_theo_thu_tu(sorted(o[(1, 0)], key=lambda m: -m["dt"])[:2], ["mi_a", "mi_b"], "x"))
            rest = o.get((1, 1), []) + o.get((1, 2), [])
            if rest:
                g.update(anh.gan_theo_thu_tu(sorted(rest, key=lambda m: -m["dt"])[:3], ["xt_a", "xt_b", "xt_c"], "y"))
        anh.luu_manh(to, g, ra)
        names.update(g)
    p3 = anh.to_moi_nhat(tv, "M03")
    if p3:
        to = anh.doc_to(p3)
        if k == 2:
            top = [m for m in to.manh if (m["y0"] + m["y1"]) / 2 < to.h * 0.42]
            low = [m for m in to.manh if (m["y0"] + m["y1"]) / 2 >= to.h * 0.42]
            g = anh.gan_theo_thu_tu(sorted(top, key=lambda m: -m["dt"])[:2], ["chan_a", "chan_b"], "y")
            g.update(anh.gan_theo_thu_tu(sorted(low, key=lambda m: -m["dt"])[:8], GAI_ANH[2], "x"))
        else:
            g = anh.gan_theo_thu_tu(sorted(to.manh, key=lambda m: -m["dt"])[:7], GAI_ANH[1], "x")
        anh.luu_manh(to, g, ra)
        names.update(g)
    print("soi:", anh.to_soi(ra, list(GIU[k])))


# ------------------------------------------------------------------ hình học
def buoc(k):
    """bước lưới theo chiều cao con (đặc tả mục 5): viền 1,5%, trong 2% chiều cao (đơn vị rig = px atlas)."""
    c = CFG[k]
    cao = (c["O"][1] - c["dinh"]) * c["S"]
    return 0.013 * cao, 0.0175 * cao, cao


class Hinh:
    """đổi toạ độ concept (px, y xuống) -> rig (y lên, gốc ở chân)."""

    def __init__(self, k):
        c = CFG[k]
        self.S, (self.ox, self.gy) = c["S"], c["O"]

    def __call__(self, x, y=None):
        if y is None:
            P = np.asarray(x, float).reshape(-1, 2)
            return np.stack([(P[:, 0] - self.ox) * self.S, (self.gy - P[:, 1]) * self.S], 1)
        return np.array([(x - self.ox) * self.S, (self.gy - y) * self.S])


def dat_hop(im, box_rig):
    """Dat đặt ảnh im vừa khung bao (x0, y0, x1, y1) rig (y lên): tâm khớp tâm, tỉ lệ riêng hai trục."""
    x0, y0, x1, y1 = box_rig
    return Dat((x0 + x1) / 2, (y0 + y1) / 2, 0.0, ((x1 - x0) / im.width, (y1 - y0) / im.height))


def nguoc(dat, im, P):
    """rig -> toạ độ ảnh (nghịch của Dat.ra, không xoay hay xoay đều được)."""
    P = np.asarray(P, float).reshape(-1, 2)
    c, s = math.cos(math.radians(dat.goc)), math.sin(math.radians(dat.goc))
    dx, dy = P[:, 0] - dat.x, P[:, 1] - dat.y
    lx, ly = c * dx + s * dy, -s * dx + c * dy
    ax, ay = (dat.neo if dat.neo_px else (dat.neo[0] * im.width, dat.neo[1] * im.height))
    return np.stack([ax + lx / dat.sx * (-1 if dat.lat else 1), ay - ly / dat.sy], 1)


def duong_deu(P, n=200):
    """đường gấp khúc -> n điểm cách đều (Catmull-Rom cho mượt)."""
    P = np.asarray(P, float)
    if len(P) > 2:
        Q = [P[0]]
        ext = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
        for i in range(1, len(ext) - 2):
            p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
            for t in np.linspace(0, 1, 12)[1:]:
                Q.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
        P = np.array(Q)
    d = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(P, axis=0).T))])
    s = np.linspace(0, d[-1], n)
    return np.stack([np.interp(s, d, P[:, 0]), np.interp(s, d, P[:, 1])], 1), d[-1]


def dai_cong(L, im, path_rig, ti, mat_duoi=1):
    """dải lưới vẽ thẳng ngang (gốc trái) uốn theo đường cong path_rig (rig): đỉnh (s, n) -> C(s·ti) + N·n·ti. mat_duoi=+1: mép
    dưới ảnh nằm bên PHẢI hướng đi (đi sang phải thì mép dưới ở dưới), -1 thì ngược. Trả (V thế giới, hàm vị trí theo s ảnh)."""
    D, cum = L.truc
    D = np.asarray(D, float)
    tg = np.gradient(D, axis=0)
    tg /= np.maximum(1e-9, np.hypot(*tg.T))[:, None]
    nrm = np.stack([-tg[:, 1], tg[:, 0]], 1)    # ảnh y xuống: pháp tuyến chĩa xuống khi trục sang phải
    s = np.asarray(L.s, float)
    ax = np.stack([np.interp(s, cum, D[:, 0]), np.interp(s, cum, D[:, 1])], 1)
    nn = np.stack([np.interp(s, cum, nrm[:, 0]), np.interp(s, cum, nrm[:, 1])], 1)
    off = ((L.pts - ax) * nn).sum(1)            # khoảng lệch về phía mép dưới ảnh
    C, plen = duong_deu(path_rig, 400)
    dC = np.gradient(C, axis=0)
    dC /= np.maximum(1e-9, np.hypot(*dC.T))[:, None]
    cs = np.linspace(0, plen, len(C))

    def at(sv):
        sv = np.atleast_1d(np.asarray(sv, float)) * ti
        x = np.interp(sv, cs, C[:, 0]) + np.maximum(sv - plen, 0) * dC[-1, 0]
        y = np.interp(sv, cs, C[:, 1]) + np.maximum(sv - plen, 0) * dC[-1, 1]
        tx, ty = np.interp(sv, cs, dC[:, 0]), np.interp(sv, cs, dC[:, 1])
        return np.stack([x, y], 1), np.stack([tx, ty], 1)

    P, T = at(s)
    right = np.stack([T[:, 1], -T[:, 0]], 1)    # bên phải hướng đi (y lên)
    V = P + right * (off * ti * mat_duoi)[:, None]
    return V, (lambda sv: at(sv)[0])


def doc_khop(k):
    """kết quả dò tự động (tm05_khop.py, chạy bằng venv có cv2); chưa có thì {}."""
    import json
    p = thu_muc(k, "rig", "khop.json")
    if not os.path.exists(p):
        print("  (chưa có khop.json: đặt mảnh theo khung bao dự kiến)")
        return {}
    return json.load(open(p, encoding="utf-8"))


# ------------------------------------------------------------------ dựng rig
def dung(k, chi_dat=False):
    if os.path.exists(thu_muc(k, "manh_lai", "lai.json")) and not chi_dat:
        return dung_lai(k)
    c = CFG[k]
    R = Hinh(k)
    S = c["S"]
    kj = doc_khop(k)
    tr = {}
    for nm, o in kj.items():
        tr[o.get("anh", nm)] = o["s"]
    pc = anh.nap_manh(thu_muc(k, "manh"), GIU[k], ti_le=S, ti_le_rieng=tr)
    sk = khung.Sk(f"{CODE}_{k}")

    def dat_kj(nm, im):
        o = kj[nm]
        return Dat(*R(o["cx"], o["cy"]), o["r"], 1.0)

    for n, im in pc.items():
        sk.anh(n, im)
    H = R(*c["H"])
    U, D = R(c["U"]), R(c["D"])
    # ---- xương thân, vỏ
    sk.xuong("root")
    sk.xuong("move", "root")
    body_c = R(*((np.array(c["tren_box"][:2]) + np.array(c["duoi_box"][2:])) / 2))
    sk.xuong("than", "move", body_c[0], body_c[1], the_gioi=True, dai=40)
    front = (U[-1] + D[-1]) / 2
    ang = math.degrees(math.atan2(*(front - H)[::-1]))
    sk.xuong("vo_duoi", "than", H[0], H[1], goc=ang, dai=float(np.hypot(*(front - H))), the_gioi=True)
    sk.xuong("vo_tren", "than", H[0], H[1], goc=ang, dai=float(np.hypot(*(front - H))), the_gioi=True)
    mc = R(*c["mat_c"])
    sk.xuong("mat", "vo_tren", mc[0], mc[1], the_gioi=True, dai=30)
    mt = sk.chuoi("mt", "vo_tren", U)          # môi trên (vùng mềm của nửa trên)
    md = sk.chuoi("md", "vo_duoi", D)          # môi dưới
    # ---- gai: mỗi cái một xương (gốc ở chân gai, trục chĩa tới ngọn)
    gai = []
    dat_gai = {}
    for (nm, par, b, t), gim in zip(c["gai"], GAI_ANH[k]):
        B, T = R(*b), R(*t)
        if nm in kj:
            im = pc[gim]
            dat_gai[nm] = dat_kj(nm, im)
            B, T = dat_gai[nm].ra([[im.width / 2, im.height * 0.97], [im.width / 2, 0]], im.width, im.height)
        sk.xuong(nm, par, B[0], B[1], goc=math.degrees(math.atan2(*(T - B)[::-1])), dai=float(np.hypot(*(T - B))), the_gioi=True)
        gai.append(nm)
    # ---- ngọc, lưỡi, miệng
    if k == 2:
        Lu = R(c["luoi"])
        luoi_x = sk.chuoi("lu", "vo_duoi", Lu)
        ng = R(*c["ngoc"][0]) if "ngoc" not in kj else R(kj["ngoc"]["cx"], kj["ngoc"]["cy"])
        sk.xuong("ngoc", luoi_x[1], ng[0], ng[1], the_gioi=True, dai=20)
        mc2 = R(*c["mien"][0]) if "mien" not in kj else dat_kj("mien", pc["mien"]).mot((pc["mien"].width / 2, pc["mien"].height * 0.92),
                                                                                    pc["mien"].width, pc["mien"].height)
        sk.xuong("mien", "vo_tren", mc2[0], mc2[1], goc=90, dai=30, the_gioi=True)
    else:
        luoi_x = []
        ng = R(*c["ngoc"][0]) if "ngoc" not in kj else R(kj["ngoc"]["cx"], kj["ngoc"]["cy"])
        sk.xuong("ngoc", "vo_duoi", ng[0], ng[1], the_gioi=True, dai=20)
    mp = R(*c["mieng"][0])
    sk.xuong("mieng", "ngoc" if k == 2 else "vo_duoi", mp[0], mp[1], goc=c["mieng"][1], dai=40, the_gioi=True)
    # ---- chân / xúc tu: chuỗi theo đường cong
    chains = {}
    for nm, im_n, path, side in c["chan"]:
        chains[nm] = (im_n, R(path), "move", 5 if k == 2 else 4, side, "than")
    for nm, im_n, path, par, side in c["xt"]:
        chains[nm] = (im_n, R(path), par, 3, side, par)
    built = {}
    for nm, (im_n, path, par, nseg, side, hoa) in chains.items():
        im = pc[im_n]
        L = luoi.luoi_dai(im, nseg, cot_moi_dot=3, buoc=buoc(k)[1] * 0.85, buoc_ngang=buoc(k)[0], ten=nm)
        _, plen = duong_deu(path, 400)
        ti = plen / L.truc[1][-1]
        V, at = dai_cong(L, im, path, ti, side)
        print(f"  {nm}: dài đường {plen:.0f}, ảnh {L.truc[1][-1]:.0f} px, tỉ lệ {ti:.2f}")
        J = at(np.linspace(0, L.truc[1][-1], nseg + 1))
        names = sk.chuoi(nm, par, J)
        built[nm] = (L, V, names, im_n, hoa)
    # ---- slot (sau → trước)
    for nm in ("cbs", "cbt", "cfs", "cft", "chan"):
        if nm in built:
            sk.slot(nm, built[nm][2][0], built[nm][3])
    for nm, par, _, _ in c["gai"]:
        sk.slot(nm, nm, None)
    sk.slot("long", "vo_duoi", "long")
    if k == 2:
        sk.slot("luoi", luoi_x[0], "luoi")
    sk.slot("ngoc", "ngoc", "ngoc")
    for nm in ("xtb", "xtc"):
        if nm in built:
            sk.slot(nm, built[nm][2][0], built[nm][3])
    sk.slot("duoi", "vo_duoi", "duoi")
    if "xta" in built:
        sk.slot("xta", built["xta"][2][0], built["xta"][3])
    sk.slot("tren", "vo_tren", "tren")
    sk.slot("mi_a", "mat", "mi_a", an=True)
    sk.slot("mi_b", "mat", "mi_b", an=True)
    if k == 2:
        sk.slot("mien", "mien", "mien")
    # ---- hai nửa vỏ: lưới vùng; vỏ cứng 100%, mặt mềm (xương mat), môi là chuỗi
    tb, db = c["tren_box"], c["duoi_box"]
    dat_t = dat_kj("tren", pc["tren"]) if "tren" in kj else dat_hop(pc["tren"], (*R(tb[0], tb[3]), *R(tb[2], tb[1])))
    dat_d = dat_kj("duoi", pc["duoi"]) if "duoi" in kj else dat_hop(pc["duoi"], (*R(db[0], db[3]), *R(db[2], db[1])))
    info = {"k": k, "pc": pc, "dat_t": dat_t, "dat_d": dat_d, "gai": gai, "mt": mt, "md": md, "luoi": luoi_x,
            "chains": {n: v[2] for n, v in built.items()}, "R": R, "H": H}
    if chi_dat:
        return sk, info
    _vo(sk, info, "tren", dat_t, "vo_tren", mt, U, mat=True)
    _vo(sk, info, "duoi", dat_d, "vo_duoi", md, D, mat=False)
    # ---- lòng miệng: màng nối hai vỏ (khuất sau hai nửa vỏ)
    _long(sk, info, U, D, H)
    # ---- gai: mảnh cứng trên xương riêng (đặt theo dò; chưa dò thì theo chân → ngọn trong CFG, chân lùi vào dưới vỏ 18%)
    for (nm, par, b, t), gim in zip(c["gai"], GAI_ANH[k]):
        im = pc[gim]
        if nm in dat_gai:
            sk.manh(nm, gim, dat_gai[nm])
        else:
            B, T = R(*b), R(*t)
            Ln = float(np.hypot(*(T - B)))
            u = (T - B) / Ln
            base = B - u * Ln * 0.18
            sk.manh(nm, gim, Dat(base[0], base[1], math.degrees(math.atan2(*(T - B)[::-1])) - 90, Ln * 1.18 / im.height, neo=(0.5, 1.0)))
        sk._slot(nm)["att"] = gim
    # ---- ngọc, lưỡi, mũ miện
    d_ng = c["ngoc"][1] * S
    sk.manh("ngoc", "ngoc", dat_kj("ngoc", pc["ngoc"]) if "ngoc" in kj else Dat(ng[0], ng[1], 0, d_ng / pc["ngoc"].width))
    if k == 2:
        im = pc["luoi"]
        Ll = luoi.luoi_dai(im, 3, cot_moi_dot=3, buoc=buoc(k)[1] * 0.85, buoc_ngang=buoc(k)[0], ten="luoi")
        _, plen = duong_deu(Lu, 400)
        V, _ = dai_cong(Ll, im, Lu, plen / Ll.truc[1][-1], 1)
        Wl = trongso.chuoi(Ll.s, Ll.truc[1][-1] / 3, luoi_x, cha="vo_duoi", cha_hoa=0.8)
        sk.luoi_gan("luoi", "luoi", Ll, Wl, the_gioi=V)
        im = pc["mien"]
        sk.manh("mien", "mien", dat_kj("mien", im) if "mien" in kj else Dat(mc2[0], mc2[1], 0, c["mien"][1] * S / im.width, neo=(0.5, 0.92)))
    # ---- chân, xúc tu: trọng số B-spline dọc dải, gốc hoà vào cha
    for nm, (L, V, names, im_n, hoa) in built.items():
        W = trongso.chuoi(L.s, L.truc[1][-1] / len(names), names, cha=hoa, cha_hoa=0.6 if nm.startswith("c") else 0.5)
        sk.luoi_gan(nm, im_n, L, W, the_gioi=V)
    # ---- mí mắt: mặt nạ cả con mắt, fit_lid dò cho phủ kín
    for slot, (ex, ey) in zip(("mi_a", "mi_b"), c["mat"]):
        hat = nguoc(dat_t, pc["tren"], [R(ex, ey)])[0]
        try:
            em, seed = mat_mask(pc["tren"], hat)
            kq = mieng.fit_lid(pc["tren"], pc[slot], mat=em, ten=slot)
            info.setdefault("mat_mask", {})[slot] = em
        except ValueError as e:
            print("  mí", slot, e)
            kq = (hat[0], hat[1], 0.0, pc["tren"].width * 0.12 / pc[slot].width, -1)
        info.setdefault("mi", {})[slot] = kq
        sk.manh(slot, slot, mieng.dat_mi(dat_t, pc["tren"], kq))
    for e, m in (("trung", "khung đòn thường trúng"), ("phun", "bắt đầu nhả (VFX bám xương mieng)"), ("het_phun", "hết nhả"),
                 ("gam", "chiêu cuối bung"), ("het_gam", "hết chiêu cuối"), ("gai", "gai bay lên (Mưa Gai)"), ("dap", "xúc tu đập đất"),
                 ("song", "sóng trồi từ chân (VFX)")):
        sk.su_kien(e, m)
    # chỗ chân xúc tu chạm đất (ngọn dáng gốc) để giữ bám đất
    W0 = sk.the_gioi()
    info["foot"] = {}
    for nm, names in info["chains"].items():
        if nm.startswith("c"):
            b = names[-1]
            ln = sk.bones[sk.bi[b]]["length"]
            info["foot"][nm] = (W0[b] @ np.array([ln, 0, 1.0]))[:2]
    return sk, info


def dung_lai(k):
    """dựng rig theo cách lai: mọi mảnh cắt từ concept (tm05_lai.py) đặt đúng chỗ của nó trong concept (khớp 100%)."""
    import json
    c = CFG[k]
    R = Hinh(k)
    S = c["S"]
    md_ = thu_muc(k, "manh_lai")
    lai = json.load(open(os.path.join(md_, "lai.json"), encoding="utf-8"))
    pc, dat, goc_anh = {}, {}, {}
    sk = khung.Sk(f"{CODE}_{k}")
    for n, e in lai.items():
        raw = Image.open(os.path.join(md_, n + ".png")).convert("RGBA")
        bb = raw.getbbox()
        raw = raw.crop(bb)
        w, h = raw.size
        aw, ah = max(1, int(round(w * S))), max(1, int(round(h * S)))
        im = anh.loang_mau(raw.resize((aw, ah), Image.LANCZOS))
        pc[n] = im
        tlx, tly = e["x0"] + bb[0], e["y0"] + bb[1]     # góc trái trên của ảnh đã cắt sát, px concept
        goc_anh[n] = (tlx, tly, w / aw, h / ah)          # đổi px atlas -> px concept: tl + p * k
        dat[n] = Dat(*R(tlx, tly), 0.0, ((w * S) / aw, (h * S) / ah), neo=(0.0, 0.0))
        sk.anh(n, im)

    def anh_tu_concept(n, P):
        tlx, tly, kx, ky = goc_anh[n]
        P = np.asarray(P, float).reshape(-1, 2)
        return np.stack([(P[:, 0] - tlx) / kx, (P[:, 1] - tly) / ky], 1)

    H = R(*c["H"])
    U, D = R(c["U"]), R(c["D"])
    # ---- xương thân, vỏ
    sk.xuong("root")
    sk.xuong("move", "root")
    e_t, e_d = lai["tren"], lai["duoi"]
    body_c = R((min(e_t["x0"], e_d["x0"]) + max(e_t["x1"], e_d["x1"])) / 2, (e_t["y0"] + e_d["y1"]) / 2)
    sk.xuong("than", "move", body_c[0], body_c[1], the_gioi=True, dai=40)
    front = (U[-1] + D[-1]) / 2
    ang = math.degrees(math.atan2(*(front - H)[::-1]))
    L_hm = float(np.hypot(*(front - H)))
    sk.xuong("vo_duoi", "than", H[0], H[1], goc=ang, dai=L_hm, the_gioi=True)
    sk.xuong("vo_tren", "than", H[0], H[1], goc=ang, dai=L_hm, the_gioi=True)
    mc = R(*c["mat_c"])
    sk.xuong("mat", "vo_tren", mc[0], mc[1], the_gioi=True, dai=30)
    mt = sk.chuoi("mt", "vo_tren", U)
    md = sk.chuoi("md", "vo_duoi", D)
    gai = []
    for (nm, par, b, t), gim in zip(c["gai"], GAI_ANH[k]):
        B, T = R(*b), R(*t)
        sk.xuong(nm, par, B[0], B[1], goc=math.degrees(math.atan2(*(T - B)[::-1])), dai=float(np.hypot(*(T - B))), the_gioi=True)
        gai.append(nm)
    ng = R(lai["ngoc"]["cx"], lai["ngoc"]["cy"])
    sk.xuong("ngoc", "vo_duoi", ng[0], ng[1], the_gioi=True, dai=20)
    if "mien" in lai:
        e = lai["mien"]
        mb = R((e["x0"] + e["x1"]) / 2, e["y1"] - 0.12 * (e["y1"] - e["y0"]))
        sk.xuong("mien", "vo_tren", mb[0], mb[1], goc=90, dai=30, the_gioi=True)
    if k == 2:   # chỗ nhả: mép trước viên ngọc, trục x chĩa sang phải
        mp = R(lai["ngoc"]["cx"] + lai["ngoc"]["r"] * 0.9, lai["ngoc"]["cy"])
        sk.xuong("mieng", "ngoc", mp[0], mp[1], goc=0.0, dai=40, the_gioi=True)
    else:
        mp = R(*c["mieng"][0])
        sk.xuong("mieng", "vo_duoi", mp[0], mp[1], goc=c["mieng"][1], dai=40, the_gioi=True)
    # ---- chân / xúc tu: chuỗi theo đường giữa tìm được trên concept
    cha = {"cbs": "move", "cbt": "move", "cfs": "move", "cft": "move", "chan": "move",
           "xt_a": "vo_tren", "xt_b": "vo_duoi", "xt_c": "vo_duoi"}
    hoa = {"cbs": "than", "cbt": "than", "cfs": "than", "cft": "than", "chan": "than",
           "xt_a": "vo_tren", "xt_b": "vo_duoi", "xt_c": "vo_duoi"}
    nseg = {"xt_a": 4, "xt_b": 4, "xt_c": 4, "chan": 5}
    chains = {}
    for n in ("cfs", "cbs", "cbt", "cft", "chan", "xt_a", "xt_b", "xt_c"):
        if n not in lai:
            continue
        path = np.array(lai[n]["duong"], float)
        ns = nseg.get(n, 6)
        Cp, plen = duong_deu(path, 300)
        idx = np.linspace(0, len(Cp) - 1, ns + 1).round().astype(int)
        Jc = Cp[idx]
        names = sk.chuoi(n, cha[n], R(Jc))
        chains[n] = (names, Jc)
    # ---- slot (sau → trước)
    for n in ("cfs", "cbs", "cbt", "cft", "chan"):
        if n in chains:
            sk.slot(n, chains[n][0][0], n)
    for (nm, par, b, t), gim in zip(c["gai"], GAI_ANH[k]):
        sk.slot(nm, nm, gim)
    sk.slot("long", "vo_duoi", "long")
    sk.slot("ngoc", "ngoc", "ngoc")
    for n in ("xt_c", "xt_b", "xt_a"):
        if n in chains:
            sk.slot(n, chains[n][0][0], n)
    sk.slot("duoi", "vo_duoi", "duoi")
    sk.slot("tren", "vo_tren", "tren")
    sk.slot("mi_a", "mat", "mi_a", an=True)
    sk.slot("mi_b", "mat", "mi_b", an=True)
    if "mien" in lai:
        sk.slot("mien", "mien", "mien")
    info = {"k": k, "pc": pc, "dat_t": dat["tren"], "dat_d": dat["duoi"], "gai": gai, "mt": mt, "md": md, "luoi": [],
            "chains": {n: v[0] for n, v in chains.items()}, "R": R, "H": H, "lai": lai}
    # ---- hai nửa vỏ
    _vo(sk, info, "tren", dat["tren"], "vo_tren", mt, U, mat=True)
    _vo(sk, info, "duoi", dat["duoi"], "vo_duoi", md, D, mat=False)
    # ---- lòng miệng: màng nối hai vỏ (trọng số theo vị trí giữa môi trên và môi dưới)
    bv, bt, _ = buoc(k)
    im = pc["long"]
    Ll = luoi.luoi_vung(im, bv, bt, vien=3, ten="long")
    Q = dat["long"].ra(Ll.pts, im.width, im.height)
    Cu, _ = duong_deu(U, 200)
    Cd, _ = duong_deu(D, 200)

    def kc(Qp, C):
        d = np.hypot(Qp[:, None, 0] - C[None, :, 0], Qp[:, None, 1] - C[None, :, 1])
        j = d.argmin(1)
        return d[np.arange(len(Qp)), j], j

    du, ju = kc(Q, Cu)
    dd, jd = kc(Q, Cd)
    # phía trên môi trên (theo pháp tuyến cục bộ) thì 100% vỏ trên, dưới môi dưới 100% vỏ dưới, giữa hoà theo tỉ lệ khoảng cách
    up = Cu[ju] - Cd[np.clip(ju, 0, len(Cd) - 1)]
    up /= np.maximum(1e-6, np.hypot(*up.T))[:, None]
    above = ((Q - Cu[ju]) * up).sum(1) > 0
    below = ((Q - Cd[jd]) * up).sum(1) < 0
    t = dd / np.maximum(1e-6, du + dd)
    t = np.where(above, 1.0, np.where(below, 0.0, t))
    t = t * t * (3 - 2 * t)
    Wl = [({"vo_tren": float(v), "vo_duoi": float(1 - v)} if 0.002 < v < 0.998 else ({"vo_tren": 1.0} if v >= 0.998 else {"vo_duoi": 1.0}))
          for v in t]
    Wl = trongso.lam_tron(Ll, Wl, 2)
    sk.luoi_gan("long", "long", Ll, Wl, dat=dat["long"])
    # ---- gai, ngọc, mũ miện, mí: mảnh cứng đặt đúng chỗ
    for (nm, par, b, t_), gim in zip(c["gai"], GAI_ANH[k]):
        sk.manh(nm, gim, dat[gim])
    sk.manh("ngoc", "ngoc", dat["ngoc"])
    if "mien" in lai:
        sk.manh("mien", "mien", dat["mien"])
    for n in ("mi_a", "mi_b"):
        sk.manh(n, n, dat[n])
    # ---- chân, xúc tu: lưới vùng trên mảnh cong + trọng số B-spline theo khoảng cách đi trong hình từ gốc
    for n, (names, Jc) in chains.items():
        im = pc[n]
        L = luoi.luoi_vung(im, bv, bt, ten=n)
        J_anh = anh_tu_concept(n, Jc)
        W = trongso.chuoi_geo(L, J_anh, names, cha=hoa[n], cha_hoa=0.6 if not n.startswith("xt") else 0.5)
        W = trongso.lam_tron(L, W, 1)
        trongso.kiem(W, n)
        sk.luoi_gan(n, n, L, W, dat=dat[n])
    for e_, m_ in (("trung", "khung đòn thường trúng"), ("phun", "bắt đầu nhả (VFX bám xương mieng)"), ("het_phun", "hết nhả"),
                   ("gam", "chiêu cuối bung"), ("het_gam", "hết chiêu cuối"), ("gai", "gai bay lên (Mưa Gai)"),
                   ("dap", "xúc tu đập đất"), ("song", "sóng trồi từ chân (VFX)")):
        sk.su_kien(e_, m_)
    W0 = sk.the_gioi()
    info["foot"] = {}
    for n, names in info["chains"].items():
        if not n.startswith("x"):
            b = names[-1]
            ln = sk.bones[sk.bi[b]]["length"]
            info["foot"][n] = (W0[b] @ np.array([ln, 0, 1.0]))[:2]
    return sk, info


def _vo(sk, info, slot, dat, xb, moi, LIP, mat):
    """lưới nửa vỏ: vỏ cứng 100% xb; vùng môi (dải 26% dày từ mép lên) theo chuỗi môi; vùng mặt theo xương mat."""
    k, R, c = info["k"], info["R"], CFG[info["k"]]
    im = info["pc"][slot]
    bv, bt, _ = buoc(k)
    L = luoi.luoi_vung(im, bv, bt, ten=slot)
    Q = dat.ra(L.pts, im.width, im.height)               # đỉnh thế giới
    # khoảng cách tới đường môi (theo pháp tuyến): vùng môi = trong dải `band` quanh đường
    C, _ = duong_deu(LIP, 300)
    dmin = np.min(np.hypot(Q[:, None, 0] - C[None, :, 0], Q[:, None, 1] - C[None, :, 1]), axis=1)
    band = (50 if k == 2 else 28) * c["S"] / 0.45
    f_lip = np.clip(1.0 - dmin / band, 0, 1) ** 1.2
    # bỏ phần môi sát bản lề (khớp vỏ cứng)
    u = (Q - info["H"]) @ (C[-1] - info["H"]) / max(1e-9, float((C[-1] - info["H"]) @ (C[-1] - info["H"])))
    f_lip *= np.clip((u - 0.12) / 0.15, 0, 1)
    W_lip = trongso.chuoi_chieu(Q, LIP, moi, cha=xb, cha_hoa=0.6)
    if mat:
        mc = R(*c["mat_c"])
        rad = (150 if k == 2 else 130) * c["S"]
        f_mat = np.clip(1.0 - np.hypot(*(Q - mc).T) / rad, 0, 1)
        f_mat = f_mat * f_mat * (3 - 2 * f_mat)
        f_mat = np.minimum(f_mat, 1 - f_lip) * 0.85
    else:
        f_mat = np.zeros(len(Q))
    f_v = 1.0 - f_lip - f_mat
    parts = [(f_v, trongso.cung(L.n, xb)), (f_lip * 0.9, W_lip), (f_lip * 0.1, trongso.cung(L.n, xb))]
    if mat:
        parts.append((f_mat, trongso.cung(L.n, "mat")))
    W = trongso.chuan(trongso.tron(*parts))
    W = trongso.lam_tron(L, W, 2)
    trongso.kiem(W, slot, cho_cung=(xb,))
    sk.luoi_gan(slot, slot, L, W, dat=dat)
    info.setdefault("luoi_vo", {})[slot] = L


def _long(sk, info, U, D, H):
    """lòng miệng: màng lưới cot×hang trên ảnh lòng miệng (họng sẫm ở trái = phía bản lề). Hàng trên nằm trong nửa trên (cao hơn
    môi trên `lift`), hàng dưới trong nửa dưới (thấp hơn môi dưới): cả màng khuất sau hai nửa vỏ ở mọi độ há. Hàng dưới bám vỏ
    dưới 100%, hàng trên bám vỏ trên, giữa hoà: vỏ khép thì màng gập lại; không mảng thịt nào thò khỏi môi trên."""
    k, c = info["k"], CFG[info["k"]]
    im = sk.images["long"]
    cot, hang = 13, 8
    L = luoi.luoi_o(im.width, im.height, cot, hang, 0.06, 0.96, 0.06, 0.94, ten="long")
    Cu, _ = duong_deu(U, cot)
    Cd, _ = duong_deu(D, cot)
    lift = (60 if k == 2 else 40) * c["S"] / 0.45
    V, W = [], []
    for r in range(hang):
        kk = r / (hang - 1)
        for i in range(cot):
            fu = i / (cot - 1)
            up = Cu[i] - Cd[i]
            up = up / max(1e-6, float(np.hypot(*up)))
            g = 0.35 + 0.65 * fu
            top = Cu[i] + up * lift * g
            bot = Cd[i] - up * lift * 0.8 * g
            V.append(top + (bot - top) * kk)
            W.append({"vo_tren": 1 - kk, "vo_duoi": kk} if 0 < kk < 1 else ({"vo_duoi": 1.0} if kk >= 1 else {"vo_tren": 1.0}))
    sk.luoi_gan("long", "long", L, W, the_gioi=np.array(V))


def mat_mask(im, hat, noi=4, tim=40):
    """mặt nạ cả con mắt (tròng trắng + mống + con ngươi) trên ảnh nửa trên: điểm sáng hoặc ấm (không phải da xanh, không phải
    mực) liền với điểm gần hat nhất, bao lồi, nới noi px cho hết viền mực."""
    a = np.asarray(im.convert("RGBA")).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    light = (np.minimum(np.minimum(r, g), b) > 200)
    warm = (r > 170) & (r - b > 70) & (g > 90)
    cand = (light | warm) & (al > 128)
    hx, hy = int(hat[0]), int(hat[1])
    ys, xs = np.nonzero(cand[max(0, hy - tim):hy + tim, max(0, hx - tim):hx + tim])
    if not len(xs):
        raise ValueError(f"không thấy mắt quanh ({hx}, {hy})")
    j = int(np.argmin((xs + max(0, hx - tim) - hx) ** 2 + (ys + max(0, hy - tim) - hy) ** 2))
    sx, sy = xs[j] + max(0, hx - tim), ys[j] + max(0, hy - tim)
    lab, _ = anh.thanh_phan(cand)
    yy, xx = np.nonzero(lab == lab[sy, sx])
    hull = anh.bao_loi(np.stack([xx + 0.5, yy + 0.5], 1))
    eye = anh.to_da_giac(cand.shape, hull)
    return anh.gian(eye, noi, tron=True), (sx, sy)


# ------------------------------------------------------------------ soi chỗ đặt
def soi_dat(k):
    sk, info = dung(k)
    ve = soi.Ve(sk)
    P = khung.Pose()
    B = soi._union([ve.bao(P)], 0.05)
    a = ve.ve(P, B, 1.0, bg=(255, 255, 255), ss=2)
    R = info["R"]
    con = Image.open(thu_muc(k, "tai_ve", "L1_chon.png")).convert("RGBA")
    # concept về cùng hệ: rig x = (px - ox)·S → ảnh khung: phụ thuộc B; dựng ảnh concept co S rồi dán
    S = CFG[k]["S"]
    cs = con.resize((int(con.width * S), int(con.height * S)))
    out = Image.new("RGBA", a.size, (255, 255, 255, 255))
    ox, gy = CFG[k]["O"]
    # điểm rig (0,0) trong ảnh khung: x = (0 - B[0]) * 1, y = (B[3] - 0)
    X0, Y0 = -B[0], B[3]
    out.alpha_composite(cs, (int(round(X0 - ox * S)), int(round(Y0 - gy * S))))
    ov = Image.blend(out.convert("RGB"), a.convert("RGB"), 0.6)
    ra = thu_muc(k, "rig")
    os.makedirs(ra, exist_ok=True)
    ov.save(os.path.join(ra, "dat_chong.png"))
    a.convert("RGB").save(os.path.join(ra, "dat_khung0.png"))
    a2 = ve.ve(P, B, 1.0, bg=(150, 150, 150), ss=2, luoi=True, xuong=True)
    a2.convert("RGB").save(os.path.join(ra, "dat_luoi.png"))
    print(os.path.join(ra, "dat_chong.png"))


def so_concept(k, sk, P, ra):
    """so_concept.png: concept (co theo S, cùng gốc) | khung P của rig | chồng hai bản, cùng tỉ lệ, cùng đường đất."""
    ve = soi.Ve(sk)
    S = CFG[k]["S"]
    ox, gy = CFG[k]["O"]
    con = Image.open(thu_muc(k, "tai_ve", "L1_chon.png")).convert("RGBA")
    cs = con.resize((int(con.width * S), int(con.height * S)), Image.LANCZOS)
    bb = ve.bao(P)
    x0 = min(bb[0], -ox * S) - 10
    x1 = max(bb[2], (con.width - ox) * S) + 10
    y0 = min(bb[1], -(con.height - gy) * S) - 10
    y1 = max(bb[3], gy * S) + 10
    a = ve.ve(P, (x0, y0, x1, y1), 1.0, bg=(255, 255, 255), ss=2).convert("RGBA")
    c = Image.new("RGBA", a.size, (255, 255, 255, 255))
    c.alpha_composite(cs, (int(round(-x0 - ox * S)), int(round(y1 - gy * S))))
    ov = Image.blend(c.convert("RGB"), a.convert("RGB"), 0.55)
    mc_ = np.asarray(c.convert("RGB")).min(axis=2) < 235
    ma_ = np.asarray(a.convert("RGB")).min(axis=2) < 235
    iou = float((mc_ & ma_).sum() / max(1, (mc_ | ma_).sum()))
    thua = float((ma_ & ~mc_).sum() / max(1, ma_.sum()))
    thieu = float((mc_ & ~ma_).sum() / max(1, mc_.sum()))
    print(f"  so_concept dạng {k}: IoU mặt nạ {iou:.3f} (rig thừa {thua:.1%}, thiếu {thieu:.1%} so với concept)")
    W_, H_ = a.size
    out = Image.new("RGB", (W_ * 3 + 20, H_ + 26), (255, 255, 255))
    d = ImageDraw.Draw(out)
    f = anh.font(16)
    for i, (im, t) in enumerate(((c.convert("RGB"), "concept (co S)"), (a.convert("RGB"), "rig: idle t=0"), (ov, f"chồng: IoU {iou:.3f}"))):
        out.paste(im, (i * (W_ + 10), 26))
        d.text((i * (W_ + 10) + 6, 4), t, fill=(0, 0, 0), font=f)
    gyy = int(round(y1)) + 26
    d.line([(0, gyy), (out.width, gyy)], fill=(200, 60, 60), width=1)
    out.save(os.path.join(ra, "so_concept.png"))
    return iou


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    kk = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    if cmd == "cat":
        cat(kk)
    elif cmd == "dat":
        soi_dat(kk)
    elif cmd == "rig":
        from tm05_clip import chay
        chay(kk)
    else:
        print(__doc__)
