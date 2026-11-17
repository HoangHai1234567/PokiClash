# -*- coding: utf-8 -*-
"""Sa Tích DẠNG 2 (than_lan_cat_2; tướng ải 5 đảo Thổ, id game lung_vuong): hình của mình chạy trên ĐÚNG rig của con gốc monster_3530
(thằn lằn gai ngồi xổm, game tham khảo). Ghi chú: inbox/than_lan_cat_2_ghichu.md. Cách làm như than_lan_cat_rig.py (dạng 1):
- XƯƠNG: đủ xương của họ (FK; 8 IK của họ đã được runtime nướng vào biến đổi riêng `l` của mẫu khung), thêm `move` (cú lao), `day` (đáy
  thân), `tam` (tâm thân), `ham` (hàm dưới, bản lề ở góc miệng, con của đầu all8), `mieng` (chóp mõm), `far` + `fly_k`, `bay_k` (năm phiến
  mũ trùm bay của chiêu mana, game co quãng tới đối thủ, farAim).
- MẢNH: than_lan_cat_2_manh.py (concept nắn L2_tuthe → 6+1 tờ Magnific) → inbox/than_lan_cat_2/manh/. Mỗi mảnh là lưới phủ hình, mỗi
  đỉnh biến dạng như điểm tương ứng trên HỢP lưới các part của họ (trong_so_goc), làm mịn trọng số (lam_muot) cho thân, chi, đuôi, mào.
  Chân sau gần bám chân C của họ (footl_2 + footl_1), chân xa bám chân A (footr_1..3); hai chân lá B, D của họ không có mảnh. Phiến lưng
  bám từng gai beici1..6, hai mào cao bám chuỗi sừng râu jiaol / jiaor, hai phiến cổ pe1 / pe2 cứng trên all7 / all6. Đầu, mắt cứng trên
  all8; hàm + lòng miệng cứng trên `ham`. BỎ: shadow, mắt / con ngươi / mày / vạt miệng ya của họ, gai weici4, vệt xoáy xuanzhuan.
- CHUYỂN ĐỘNG (giống ý dạng 1, mạnh hơn):
    idle   = MỀM: khung 0 idle_01 + sóng sin lệch pha (thở, đầu trễ, phiến trễ dần, đuôi, mào) + trò: nghiêng đầu, chớp mắt, mũ trùm
             dựng phiến lần lượt rồi xếp lại lạch cạch;
    walk   = run_01 + phiến nhấp nhô; hit = hit_01;
    attack = skill_01 (cúi lấy đà, lao tới, tay xa vung) + `move` lao tới, há hàm rồi ĐỚP sập đúng khung trúng, vuốt cào theo đà;
    cast   = skill_03 (thu người, hai tay hất lên cao) + NĂM PHIẾN mũ trùm rời lần lượt bay găm vào đối thủ rồi bay về lắp (code lái far);
    skill  = giơ hai tay cao, gồng rít, ĐẬP xuống hai lần (dam 0,62; trung 1,00), giữ dáng rít rung tới khi lốc cát (VFX) tan (het 1,78);
    appear = nhảy từ trên xuống đáp phịch, dang hai tay gầm rồi về đứng;
    die    = die_01 + phiến mũ trùm rơi lả tả + mờ.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/than_lan_cat_2_rig.py      → inbox/than_lan_cat_2/rig/
    py -3 -I ArtGen/Spine/than_lan_cat_2_rig.py soi <clip> <giây,giây,...|n=12|t0:t1:n> [tỉ lệ]   → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/than_lan_cat_2_rig.py kiem                                            đo góc nhảy, bước dời
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, khung, hoat, xuat, soi, luoi, trongso  # noqa: E402
from quai.hoat import Clip  # noqa: E402
from hoa_ho_rig import ease, tmap, _goc  # noqa: E402
import tho5_dang2 as D2  # noqa: E402

G = D2.dat2("than_lan_cat")                                   # đặt trạng thái hoa_ho về con 3530 SAU mọi import
TEN_RIG = "than_lan_cat_2"
D_PX = float(os.environ.get("TLC2_DPX", "0.62"))            # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~720 đơn vị)
MANH = os.path.join(G.BASE, "manh")
RA = os.environ.get("TLC2_RA") or os.path.join(G.BASE, "rig")
TAN = 0.45
FPS = 30.0
W_C, H_C = 1536, 1024
IMPACT = {"attack": (0.06, 0.35, 0.09), "cast": (0.06, 0.32, 0.07), "skill": (0.14, 0.70, 0.14, "#ffffff40")}

# slot của mình (thứ tự vẽ, sau → trước): (slot = tên mảnh, [hình], nguồn gắn: list slot của họ ở idle 0 | ("cung", xương))
SLOT = [
    ("duoi", ["duoi"], ["tail4"]),                      # chỉ xương đuôi: gai đuôi weici của họ quật 67°/khung ở hit, kéo vặn mảnh đuôi
    ("chan_xa", ["chan_xa"], ["footr_1", "footr_2", "footr_3"]),
    ("than", ["than"], ["tail3", "tail2", "tail1", "chest3", "chest2", "chest1"]),
    # lớp lưng da sau mũ trùm (người dùng: "phần vảy không gắn vào người mà bay lơ lửng"): gốc mọi phiến cắm lên nó, khe giữa phiến lộ da
    ("lot", ["lot"], ["chest3", "chest2", "chest1"]),
    ("chan_gan", ["chan_gan"], ["footl_2", "footl_1"]),
    ("p3", ["p3"], ["beici3"]),
    ("p4", ["p4"], ["beici4"]),
    ("sl", ["sl"], ["jiaol"]),
    ("sr", ["sr"], ["jiaor"]),
    ("p2", ["p2"], ["beici2"]),
    ("p1", ["p1"], ["beici1"]),
    ("pe1", ["pe1"], ("cung", "all7")),
    ("p5", ["p5"], ["beici5"]),
    ("pe2", ["pe2"], ("cung", "all6")),
    ("p6", ["p6"], ["beici6"]),
    ("tay_xa", ["tay_xa"], ["handr_3", "handr_2", "handr_1"]),
    ("tay_gan", ["tay_gan"], ["lhand_3", "lhand_2", "lhand_1"]),
    ("long_mieng", ["long_mieng"], ("cung", "ham")),
    ("ham", ["ham"], ("cung", "ham")),
    ("dau", ["dau"], ("cung", "all8")),
    ("mat", ["mat", "mat_nham"], ("cung", "all8")),
]
# năm phiến mũ trùm bay của cast: khoá → (slot = ảnh, xương của phiến)
PHIEN = {"1": ("p3", "all30"), "2": ("p1", "all28"), "3": ("p2", "all29"), "4": ("p5", "all26"), "5": ("p6", "all27")}
XUONG_PHIEN = ["all30", "all31", "all28", "all29", "all26", "all27"]          # gai lưng của họ (phiến của mình), trên → dưới
CHUOI_MAO = {"l": ("all33", "all34", "all35"), "r": ("all36", "all37", "all38")}
TAY = {"gan": ("all46", "all47", "all48"), "xa": ("all49", "all50", "all51")}
DUOI = ("all21", "all22")
# xương họ để inherit = 2 (NoRotationOrReflection: KHÔNG ăn góc xoay của cha): gốc hai tay, đầu. Khung của mình luôn ăn góc cha, nên
# CUỐI mỗi khung cộng thêm −(góc thế giới của cha) vào góc riêng của các xương này (bu_ke_thua) → góc thế giới = góc riêng như runtime
# Spine của họ (mảnh gắn theo ma trận thế giới idle 0 của họ nên khớp đúng khi góc thế giới khớp).
KE_THUA_2 = ("all46", "all49", "all8")
MUOT = {"than": 10, "lot": 8, "chan_gan": 8, "chan_xa": 8, "tay_gan": 8, "tay_xa": 8, "duoi": 5, "sl": 3, "sr": 3}


# ---------------------------------------------------------------- nạp
def nap():
    scan = G.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    S = json.load(open(os.path.join(scan, "sample_goc.json"), encoding="utf-8"))
    return D, D0, I, S


def mats(Dj):
    return {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in Dj["bones"]}


def tf():
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    to_rig = lambda P: np.stack([cx + (P[:, 0] - W_C / 2) / s, cy - (P[:, 1] - H_C / 2) / s], 1)
    to_px = lambda V: np.stack([W_C / 2 + (V[:, 0] - cx) * s, H_C / 2 - (V[:, 1] - cy) * s], 1)
    return s, to_rig, to_px


def anh_manh(ten):
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    s_px, _, _ = tf()
    g = Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA")
    kq = D_PX / s_px
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), DATJ[ten]["hop"], kq


def hop_luoi(a0s, ten):
    """gộp lưới của nhiều hình của họ (idle 0) thành một: đỉnh, tam giác, trọng số {tên xương: w} (chép than_lan_cat_rig)."""
    Qs, Ts, Wg, off = [], [], [], 0
    for a0 in a0s:
        Q = np.array(a0["xy"], float).reshape(-1, 2)
        tr = np.array(a0["tris"]).reshape(-1, 3) if "tris" in a0 else np.array([[0, 1, 2], [2, 3, 0]])
        if a0.get("w"):
            w = [{ten[k]: ww for k, ww in ws if ww > 0.002} for ws in a0["w"]]
        else:
            b = ten[a0["bone"]] if isinstance(a0["bone"], int) else a0["bone"]
            w = [{b: 1.0} for _ in range(len(Q))]
        Qs.append(Q)
        Ts.append(tr + off)
        Wg += w
        off += len(Q)
    return np.concatenate(Qs), np.concatenate(Ts), Wg


def trong_so_goc(V, a0s, ten, Wi):
    """mỗi điểm V (thế giới) biến dạng như điểm tương ứng trên HỢP lưới của họ a0s (toạ độ trọng tâm trong tam giác chứa nó; ngoài lưới:
    điểm gần nhất trên cạnh + khoảng lệch). Trả hàng (xương, x, y, w) theo ma trận Wi (chép than_lan_cat_rig)."""
    Q, tr, Wg = hop_luoi(a0s, ten)
    A, B_, C = Q[tr[:, 0]], Q[tr[:, 1]], Q[tr[:, 2]]
    v0, v1 = B_ - A, C - A
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)

    def gan_canh(p, a, b):
        d = b - a
        t = np.clip(((p - a) * d).sum(axis=1) / np.maximum((d * d).sum(axis=1), 1e-12), 0, 1)
        return np.hypot(*(p - (a + t[:, None] * d)).T), t

    rows = []
    for p in V:
        v2 = p - A
        b1 = (v2[:, 0] * v1[:, 1] - v2[:, 1] * v1[:, 0]) / den
        b2 = (v0[:, 0] * v2[:, 1] - v0[:, 1] * v2[:, 0]) / den
        b0 = 1 - b1 - b2
        ok = np.flatnonzero((b0 >= -1e-4) & (b1 >= -1e-4) & (b2 >= -1e-4))
        lech = np.zeros(2)
        if len(ok):
            i = int(ok[-1])
            be = (float(b0[i]), float(b1[i]), float(b2[i]))
        else:
            best = None
            for (pa, pb, ia, ib) in ((A, B_, 0, 1), (B_, C, 1, 2), (C, A, 2, 0)):
                dist, t = gan_canh(p, pa, pb)
                j = int(np.argmin(dist))
                if best is None or dist[j] < best[0]:
                    w3 = [0.0, 0.0, 0.0]
                    w3[ia], w3[ib] = 1 - float(t[j]), float(t[j])
                    best = (float(dist[j]), j, tuple(w3), pa[j] + t[j] * (pb[j] - pa[j]))
            _, i, be, c = best
            lech = p - c
        acc = {}
        for vi, bw in zip(tr[i], be):
            for n, w in Wg[vi].items():
                e = acc.setdefault(n, [0.0, np.zeros(2)])
                e[0] += bw * w
                e[1] += bw * w * Q[vi]
        row = []
        for n, (w, q) in acc.items():
            if abs(w) < 1e-5:
                continue
            g = q / w + lech
            lp = np.linalg.solve(Wi[n], np.array([g[0], g[1], 1.0]))
            row.append((n, float(lp[0]), float(lp[1]), float(w)))
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    return rows


def lam_muot(rows, V, tris, Wi, vong, bo=()):
    """làm mịn trọng số trên lưới của mình `vong` lần (giữ 50 % của chính nó), ≤ 4 xương, gắn kiểu LBS (chép than_lan_cat_rig)."""
    n = len(rows)
    ke = [set() for _ in range(n)]
    for a, b, c in np.asarray(tris).reshape(-1, 3):
        ke[a] |= {b, c}
        ke[b] |= {a, c}
        ke[c] |= {a, b}
    w = [{} for _ in range(n)]
    for i, r in enumerate(rows):
        for bn, _, _, ww in r:
            if bn in bo:
                continue
            w[i][bn] = w[i].get(bn, 0.0) + ww
    for _ in range(vong):
        moi = []
        for i in range(n):
            acc = {k: 0.5 * v for k, v in w[i].items()}
            if ke[i]:
                f = 0.5 / len(ke[i])
                for j in ke[i]:
                    for k, v in w[j].items():
                        acc[k] = acc.get(k, 0.0) + f * v
            moi.append(acc)
        w = moi
    out = []
    for i in range(n):
        top = sorted(w[i].items(), key=lambda q: -q[1])[:4]
        tot = sum(v for _, v in top) or 1.0
        row = []
        for bn, v in top:
            if v / tot < 0.01:
                continue
            lp = np.linalg.solve(Wi[bn], np.array([V[i, 0], V[i, 1], 1.0]))
            row.append((bn, float(lp[0]), float(lp[1]), v / tot))
        t2 = sum(q[3] for q in row) or 1.0
        out.append([(a, b, c, d / t2) for a, b, c, d in row])
    return out


def gan_manh(sk, slot, ten_anh, a0s, ten, Wi, mot_xuong=None):
    im, (x0, y0, x1, y1), kq = anh_manh(ten_anh)
    if ten_anh not in sk.images:
        sk.anh(ten_anh, im)
    im = sk.images[ten_anh]
    _, to_rig, _ = tf()
    if mot_xuong is None:
        L = luoi.luoi_vung(im, buoc_vien=9.0, buoc_trong=14.0, vien=2, ten=f"{slot}/{ten_anh}", in_tk=False)
    else:
        L = luoi.luoi_o(im.width, im.height, 2, 2, ten=slot)
    V = to_rig(np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1))
    if mot_xuong is None:
        rows = trong_so_goc(V, a0s, ten, Wi)
        if MUOT.get(slot, 0) > 0:
            rows = lam_muot(rows, V, L.tris, Wi, MUOT[slot])
    else:
        b, Mb = mot_xuong
        rows = [[(b, *[float(v) for v in np.linalg.solve(Mb, np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
    Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
    sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=Vs)
    sk.atts[slot][ten_anh]["verts"] = rows
    return L


# ---------------------------------------------------------------- dựng
def dung():
    D, D0, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    Wi = mats(D0)
    by0 = {a["slot"]: a for a in D0["atts"]}
    P_all = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in D0["atts"] if a.get("region") and a["slot"] != "shadow"])
    y_day = float(P_all[:, 1].min())
    Vb = np.concatenate([np.array(by0[s]["xy"], float).reshape(-1, 2) for s in ("tail3", "tail2", "tail1", "chest3", "chest2", "chest1")])
    tam = np.array([(Vb[:, 0].min() + Vb[:, 0].max()) / 2, (Vb[:, 1].min() + Vb[:, 1].max()) / 2])
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("day", "move", float(tam[0]), y_day)
    sk.xuong("tam", "day", 0.0, float(tam[1] - y_day))
    goc0 = {}
    for b in IB:
        if b["name"] in ("root", "shadow"):
            continue
        cha = ten[b["parent"]]
        g = [b["x"], b["y"], b["rot"], b["sx"], b["sy"]]
        goc0[b["name"]] = g
        if cha == "root":
            sk.xuong(b["name"], "tam", g[0] - float(tam[0]), g[1] - float(tam[1]), goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
        else:
            sk.xuong(b["name"], cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
    s_px, to_rig, _ = tf()
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    # hàm: bản lề ở góc miệng (đầu trái đường miệng); miệng: chóp mõm. Đặt theo thế giới dáng idle 0 qua xương đầu (dáng gốc của họ)
    Wc = mats(D)
    for ten_x, px, rot in (("ham", DATJ["_ban_le"], 0.0), ("mieng", (1108.0, 505.0), 0.0)):
        p = to_rig(np.array([px], float))[0]
        sk.xuong(ten_x, "all8", 0.0, 0.0)
        Ml = np.linalg.solve(Wi["all8"], np.array([p[0], p[1], 1.0]))
        sk.bones[sk.bi[ten_x]]["x"], sk.bones[sk.bi[ten_x]]["y"] = float(Ml[0]), float(Ml[1])
        sk.bones[sk.bi[ten_x]]["rot"] = -_goc(Wi["all8"]) + rot           # trục x của hàm / miệng nằm ngang ở idle 0
    sk.W0 = sk.the_gioi()
    Wb = dict(Wi)
    for x in ("ham", "mieng"):                                            # ma trận thế giới idle 0 của xương thêm (theo all8 ở idle 0)
        b0 = sk.bones[sk.bi[x]]
        Wb[x] = Wi["all8"] @ khung.mat(b0["x"], b0["y"], b0["rot"])
    tong = [0, 0]
    for s, hinhs, nguon in SLOT:
        sk.slot(s, "move", hinhs[0], an=(s == "long_mieng" and False))
        for h in hinhs:
            if isinstance(nguon, tuple):
                L = gan_manh(sk, s, h, None, ten, Wb, mot_xuong=(nguon[1], Wb[nguon[1]]))
            else:
                L = gan_manh(sk, s, h, [by0[x] for x in nguon], ten, Wi)
            tong[0] += L.n
            tong[1] += len(L.tris)
    for e, m in (("trung", "khung trúng"), ("lao", "attack: bắt đầu lao tới (VFX bụi sau chân)"),
                 ("xoe", "cast: mũ trùm bắt đầu dựng (VFX cát bốc quanh mũ)"), ("phong", "cast: một phiến mũ trùm rời thân (chuỗi = 1..5)"),
                 ("ve", "cast: phiến lắp lại"), ("tu", "skill: giơ tay gồng (VFX cát xoáy quanh chân đối thủ bắt đầu)"),
                 ("dam", "skill: hai tay đập đất (VFX sóng bụi, rung)"), ("het", "skill: lốc cát tan"),
                 ("dap", "appear: đáp đất (VFX bụi)"), ("gam", "appear: dang tay gầm"), ("ru", "idle: mũ trùm dựng phiến lạch cạch"),
                 ("roi", "die: phiến chạm đất (VFX bụi)")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; đáy y = {y_day:.1f}, tâm thân "
          f"({tam[0]:.1f}, {tam[1]:.1f})")
    return sk, dict(IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], y_day=y_day, tam=tam, S=S, Wi=Wi)


# ---------------------------------------------------------------- chuyển động của họ
def chuyen_dong(info):
    S, ten, goc0 = info["S"], info["ten"], info["goc0"]
    out = {}
    i_mat = info["slots"].index("beyes1")
    for clip, v in S.items():
        fr = v["frames"]
        L = np.array([F["l"] for F in fr], float)
        res = {}
        for i, n in enumerate(ten):
            if n not in goc0:
                continue
            g = goc0[n]
            A = np.stack([L[:, i, 2] - g[2], L[:, i, 0] - g[0], L[:, i, 1] - g[1], L[:, i, 3] / (g[3] or 1.0), L[:, i, 4] / (g[4] or 1.0)], 1)
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round(A[0, 0] / 360.0)
            if np.abs(A - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[n] = A
        mat = ["mat_nham" if F["n"][i_mat] == "beyes1" else "mat" for F in fr]
        out[clip] = (float(v["dur"]), res, len(fr), mat)
    return out


# ---------------------------------------------------------------- mốc giờ
T_DOP, LAO, D_ATTACK = 0.52, 0.45, 1.00                 # attack: đớp trúng; lao tới (× chiều cao) ở khung đớp; dài
T_PHONG = {"1": 0.46, "2": 0.50, "3": 0.54, "4": 0.58, "5": 0.62}   # cast: phiến rời thân (trên → dưới)
BAY, GIU, VE = 0.20, 0.16, 0.30
TV = max(T_PHONG.values()) + BAY + GIU + VE             # phiến cuối lắp lại
D_CAST = round(TV + 0.36, 2)
T_TRUNG_CAST = T_PHONG["1"] + BAY + 0.012
T_GIO, T_DAM, T_DAM2, T_HET, D_SKILL = 0.50, 0.62, 1.00, 1.78, 2.20   # skill: tay giơ cao, đập 1, đập 2 (= trúng, lốc cát), lốc tan, hết
T_TRUNG_SKILL = T_DAM2
T_ROI_A, T_DAP_A, T_GAM_A, D_APPEAR = 0.10, 0.42, 0.90, 1.60
T_RU0, T_RU1 = 2.30, 3.30                               # idle: mũ trùm dựng phiến lần lượt rồi xếp
VONG_DI = {"1": 110.0, "2": 80.0, "3": 140.0, "4": 60.0, "5": 30.0}
VONG_VE = {"1": 240.0, "2": 190.0, "3": 260.0, "4": 150.0, "5": 110.0}
REF = {}


def lam_clip(sk, info, cao=720.0):
    CD = chuyen_dong(info)
    y_day = info["y_day"]
    far = sk.W0["far"][:2, 2] if "far" in sk.bi else np.array([0.9 * cao + 140.0, 0.45 * cao])

    def bu_ke_thua(P):
        W = sk.the_gioi(P)
        for b in KE_THUA_2:
            P.rot(b, -_goc(W[sk.bones[sk.bi[b]]["parent"]]))

    def boc(f):
        def g(t, P):
            f(t, P)
            bu_ke_thua(P)
        return g

    def dat(P, goc, tau, lap=False, chi=None, bo=None, mat=True, k=1.0):
        dur, R, n, M = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            if chi is not None and b not in chi:
                continue
            if bo is not None and b in bo:
                continue
            v = A[i0] * (1 - w) + A[i1] * w
            if k != 1.0:
                v = np.array([v[0] * k, v[1] * k, v[2] * k, 1 + (v[3] - 1) * k, 1 + (v[4] - 1) * k])
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        if mat:
            P.att["mat"] = M[min(n - 1, int(round(x)))]

    def pha(P, Pb, w):
        """hoà dáng P sang dáng Pb mức w (cộng phần chênh vào P)."""
        if w <= 1e-4:
            return
        for b in set(P.t) | set(Pb.t):
            a_ = P._g(b)
            b_ = Pb.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            for q in range(5):
                a_[q] += (b_[q] - a_[q]) * w

    def dang(goc, tau, **kw):
        """một dáng để hoà (pha): góc đưa về (−180°, 180°] — chuỗi góc đã unwrap của họ có thể lệch ±360° (cú vung > 180°/khung)."""
        Q = khung.Pose()
        dat(Q, goc, tau, mat=False, **kw)
        for b, g in Q.t.items():
            g[2] = ((g[2] + 180.0) % 360.0) - 180.0
        return Q

    def dam(P, a):
        if a < 0.999:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])

    def song_(t, chu_ky, tre=0.0):
        return math.sin(2 * math.pi * (t - tre) / chu_ky)

    def phap_phong(P, t, bien=1.0, chu_ky=2.0):
        """phiến mũ trùm nhấp nhô so le (phiến trên trước, phiến dưới trễ), mào đung đưa."""
        for j, b in enumerate(XUONG_PHIEN):
            P.rot(b, bien * (1.8 + 0.3 * j) * song_(t, chu_ky, 0.06 * j))
        for k_, ch in CHUOI_MAO.items():
            for j, b in enumerate(ch):
                P.rot(b, bien * (1.2 + 0.8 * j) * song_(t, chu_ky, 0.08 + 0.07 * j + (0.05 if k_ == "r" else 0.0)))

    def xoay_quanh(P, b, c_tg, goc):
        if abs(goc) < 1e-4:
            return
        W = sk.the_gioi(P)
        p = W[b][:2, 2]
        ca, sa = math.cos(math.radians(goc)), math.sin(math.radians(goc))
        d = p - c_tg
        p2 = c_tg + np.array([ca * d[0] - sa * d[1], sa * d[0] + ca * d[1]])
        Wp = W[sk.bones[sk.bi[b]]["parent"]]
        dl = np.linalg.solve(Wp[:2, :2], p2 - p)
        P.move(b, float(dl[0]), float(dl[1]))
        P.rot(b, goc)

    TAY_X = ("all46", "all47", "all48", "all49", "all50", "all51")

    def tt_gio(P, w):
        """hai tay giơ cao ra trước, ngả người ra sau, ngẩng đầu, há hàm, mũ trùm xoè."""
        if w <= 1e-4:
            return
        P.rot("body", 8.0 * w)
        P.rot("all5", 4.0 * w)
        P.rot("all8", 10.0 * w)
        P.rot("all46", 150.0 * w)
        P.rot("all47", -30.0 * w)
        P.rot("all49", 140.0 * w)
        P.rot("all50", -25.0 * w)
        P.rot("ham", -16.0 * w)
        P.move("day", 0.0, 22.0 * w)
        for j, b in enumerate(XUONG_PHIEN):
            P.rot(b, 10.0 * w)

    def tt_dap(P, w):
        """hai tay đập xuống đất phía trước, cúi người tới, cúi đầu, bẹp xuống."""
        if w <= 1e-4:
            return
        P.rot("body", -16.0 * w)
        P.rot("all5", -8.0 * w)
        P.rot("all8", -12.0 * w)
        P.rot("all46", 12.0 * w)
        P.rot("all47", 22.0 * w)
        P.rot("all49", 10.0 * w)
        P.rot("all50", 22.0 * w)
        P.move("day", 0.0, -14.0 * w)

    def tt_thu(P, w):
        """gồng thu người: ngả sau nhẹ, hai tay co lên trước ngực, ngẩng đầu."""
        if w <= 1e-4:
            return
        P.rot("body", 6.0 * w)
        P.rot("all8", 8.0 * w)
        P.rot("all46", 35.0 * w)
        P.rot("all47", 28.0 * w)
        P.rot("all49", 30.0 * w)
        P.rot("all50", 28.0 * w)
        P.move("day", 0.0, -8.0 * w)

    def tt_hat(P, w):
        """hất: chúi tới, hai tay vung ra trước và lên, há hàm."""
        if w <= 1e-4:
            return
        P.rot("body", -10.0 * w)
        P.rot("all8", -4.0 * w)
        P.rot("all46", 125.0 * w)
        P.rot("all47", -20.0 * w)
        P.rot("all49", 115.0 * w)
        P.rot("all50", -20.0 * w)
        P.rot("ham", -20.0 * w)

    # ------------------------------------------------ idle: MỀM, sóng lệch pha + trò mũ trùm dựng phiến
    def f_idle(t, P):
        dat(P, "idle_01", 0.0)
        th = song_(t, 2.0)
        P.scale("all5", 1.0, 1.0 + 0.02 * th)                 # ngực nở / xẹp
        P.rot("all3", 0.6 * th)
        P.rot("all6", -0.5 * song_(t, 2.0, 0.05))
        P.rot("all8", 1.2 * song_(t, 2.0, 0.10))
        P.rot("ham", -1.0 * (0.5 + 0.5 * song_(t, 2.0, 0.15)))
        for k_, (a, b, c) in TAY.items():                        # tay buông đung đưa nhẹ, trễ hơn thân
            sg = 1.0 if k_ == "gan" else -1.0
            P.rot(a, sg * 1.5 * song_(t, 2.0, 0.18))
            P.rot(b, sg * 1.2 * song_(t, 2.0, 0.24))
        phap_phong(P, t, 1.0, 2.0)
        for j, b in enumerate(DUOI):
            P.rot(b, (2.0 + 1.5 * j) * song_(t, 4.0, 0.12 + 0.15 * j))
        # trò (2,30 → 3,30 s): nghiêng đầu, mũ trùm dựng phiến lần lượt từ trên xuống rồi xếp lại lạch cạch, chớp mắt
        if T_RU0 < t < T_RU1 + 0.3:
            ng = hoat.cv(t, [(T_RU0, 0.0), (T_RU0 + 0.35, 1.0, "io"), (T_RU1 - 0.1, 1.0), (T_RU1 + 0.3, 0.0, "io")])
            P.rot("all8", 3.5 * ng)
            P.rot("all6", 1.5 * ng)
            for j, b in enumerate(XUONG_PHIEN):
                t0 = T_RU0 + 0.10 + 0.06 * j
                dung_ = hoat.cv(t, [(t0, 0.0), (t0 + 0.14, 1.0, "out"), (T_RU1 - 0.25 + 0.03 * j, 1.0), (T_RU1 - 0.05 + 0.03 * j, 0.0, "in")])
                lc = math.exp(-max(0.0, t - (T_RU1 - 0.05 + 0.03 * j)) / 0.06) * math.sin((t - T_RU1) * 2 * math.pi / 0.1) \
                    if t > T_RU1 - 0.05 + 0.03 * j else 0.0
                P.rot(b, 9.0 * dung_ + 2.5 * lc)
        if T_RU0 + 0.55 < t < T_RU0 + 0.72:
            P.att["mat"] = "mat_nham"

    def f_walk(t, P):
        dat(P, "run_01", t, True)
        phap_phong(P, t, 0.8, CD["run_01"][0])

    def f_hit(t, P):
        dat(P, "hit_01", t)
        k = math.exp(-max(0.0, t - 0.07) / 0.12)
        for j, b in enumerate(XUONG_PHIEN):                     # phiến bật ngược rồi về
            P.rot(b, -6.0 * k * math.sin(min(1.0, t / 0.07) * math.pi * 0.5))

    # ------------------------------------------------ attack: cúi lấy đà, lao tới đớp, vuốt cào theo đà
    M_ATK = [(0.0, 0.0), (0.38, 0.50, "io"), (T_DOP, 0.62, "in"), (0.72, 0.95, "out"), (D_ATTACK, 1.2, "io")]

    def f_attack(t, P):
        tau = tmap(t, M_ATK)
        dat(P, "skill_01", tau, bo=TAY_X)
        # tay: theo skill_01 tới 0,5 (trước cú vung 234°/khung của họ), nhả dần về 0; tự dựng cú cào: hai tay vươn lên trước lúc lao,
        # cào sập xuống đúng khung đớp, quá đà rồi về
        dat(P, "skill_01", min(tau, 0.50), chi=TAY_X, mat=False, k=hoat.cv(t, [(0.0, 1.0), (0.62, 1.0), (D_ATTACK - 0.06, 0.0, "io")]))
        cao_ = hoat.cv(t, [(0.0, 0.0), (0.28, 0.0), (T_DOP - 0.06, 1.0, "out"), (T_DOP + 0.03, -0.35, "in"), (0.70, -0.25),
                           (D_ATTACK - 0.04, 0.0, "io")])
        P.rot("all49", 75.0 * cao_)
        P.rot("all50", -20.0 * max(0.0, cao_))
        P.rot("all46", 55.0 * cao_)
        P.rot("all47", -15.0 * max(0.0, cao_))
        lao = hoat.cv(t, [(0.0, 0.0), (0.36, -0.05, "io"), (T_DOP, LAO, "in"), (0.66, LAO), (0.95, 0.0, "io")])
        P.move("move", cao * lao, 0.0)
        # hàm: há to lúc lao, ĐỚP sập đúng khung trúng, nảy nhẹ
        ha = hoat.cv(t, [(0.0, 0.0), (0.30, 0.35, "io"), (T_DOP - 0.07, 1.0, "out"), (T_DOP, -0.1, "in"), (T_DOP + 0.10, 0.08, "out"),
                         (0.86, 0.0, "io")])
        P.rot("ham", -28.0 * ha)
        P.rot("all8", -6.0 * math.exp(-((t - T_DOP) / 0.05) ** 2))        # đầu thúc tới đúng khung đớp
        k = math.exp(-((t - (T_DOP + 0.02)) / 0.05) ** 2)
        P.scale("day", 1 + 0.08 * k, 1 - 0.07 * k)
        phap_phong(P, t, 0.7)
        if t > T_DOP:                                            # phiến lắc theo cú dừng
            r = math.exp(-(t - T_DOP) / 0.10) * math.sin((t - T_DOP) * 2 * math.pi / 0.12)
            for j, b in enumerate(XUONG_PHIEN):
                P.rot(b, (4.0 + j) * r)

    # ------------------------------------------------ cast: thu người, hai tay hất lên, năm phiến bay găm rồi về
    def than_cast(t, P):
        dat(P, "idle_01", 0.0)
        thu = hoat.cv(t, [(0.0, 0.0), (0.40, 1.0, "io"), (0.52, 0.0, "in")])
        hat = hoat.cv(t, [(0.0, 0.0), (0.40, 0.0), (0.52, 1.0, "out"), (TV - 0.05, 0.9), (D_CAST - 0.04, 0.0, "io")])
        tt_thu(P, thu)
        tt_hat(P, hat)
        if 0.56 < t < TV - 0.05:                                 # giữ tay giơ: hai dáng lệch đổi nhau
            r = hoat.rung(t, 0.56, TV - 0.05, 2)
            P.rot("all8", 1.8 * r)
            P.rot("all46", 2.0 * r)
            P.rot("all49", -2.0 * r)
        if t < 0.46:                                              # mũ trùm dựng dần lúc gồng (xoe)
            u = ease(t / 0.46)
            for j, b in enumerate(XUONG_PHIEN):
                P.rot(b, 8.0 * u)

    def f_cast(t, P):
        than_cast(t, P)
        W = None
        for k_, (s, rb) in PHIEN.items():
            t0 = T_PHONG[k_]
            t_toi, t_ve0 = t0 + BAY, t0 + BAY + GIU
            t_ve1 = t_ve0 + VE
            fb, bb = f"fly_{k_}", f"bay_{k_}"
            if fb not in sk.bi:
                continue
            if t < t0:
                P.alpha[bb] = 0.0
                continue
            tt = min(t, t_ve1)
            if t < t_ve1:
                P.alpha[s] = 0.0
                P.alpha[bb] = 1.0
            else:
                P.alpha[bb] = 0.0
            A = sk.W0[fb][:2, 2].copy()
            g0 = _goc(sk.W0[bb])
            v = far - A
            n = np.array([-v[1], v[0]]) / (float(np.hypot(*v)) or 1.0)
            if tt < t_toi:
                f = ease((tt - t0) / BAY, "in")
                pos = A + f * v + n * VONG_DI[k_] * math.sin(math.pi * f)
                ang = g0 - 540.0 * ease((tt - t0) / BAY, "out")      # phiến xoay như phi tiêu
            elif tt < t_ve0:
                pos = far.copy()
                ang = g0 - 540.0 + 6.0 * math.sin((tt - t_toi) * 70.0) * math.exp(-(tt - t_toi) / 0.09)
            else:
                if W is None:
                    W = sk.the_gioi(P)
                rb_, Wl = REF[k_]
                Mt = W[rb_] @ np.linalg.inv(Wl) @ sk.W0[bb]
                R_, gr = Mt[:2, 2], _goc(Mt)
                u = (tt - t_ve0) / VE
                e = ease(u, "io")
                pos = far * (1 - e) + R_ * e + n * VONG_VE[k_] * math.sin(math.pi * u)
                g1 = gr + ((g0 - 540.0 - gr + 180.0) % 360.0 - 180.0)
                ang = (g0 - 540.0) * (1 - e) + (g1 - 360.0) * e
            P.move(fb, float(pos[0] - A[0]), float(pos[1] - A[1]))
            P.rot(bb, float(ang - g0))

    # ------------------------------------------------ skill: giơ hai tay cao, gồng rít, đập xuống hai lần, giữ dáng rít rung
    def f_skill(t, P):
        dat(P, "idle_01", 0.0)
        gio = hoat.cv(t, [(0.0, 0.0), (T_GIO, 1.0, "io"), (T_DAM - 0.09, 1.05), (T_DAM, 0.0, "in"), (0.76, 0.0),
                          (T_DAM2 - 0.10, 0.75, "out"), (T_DAM2, 0.0, "in")])
        dap = hoat.cv(t, [(0.0, 0.0), (T_DAM - 0.09, 0.0), (T_DAM, 1.0, "in"), (0.76, 0.85, "out"), (T_DAM2 - 0.10, 0.15, "io"),
                          (T_DAM2, 1.15, "in"), (T_HET, 0.9), (D_SKILL - 0.04, 0.0, "io")])
        tt_gio(P, gio)
        tt_dap(P, dap)
        if T_DAM < t < T_HET:                                    # giữ dáng rít: hai dáng lệch 2,5° đổi nhau, nhỏ dần
            r = hoat.rung(t, T_DAM, T_HET, 2) * (1.0 - 0.5 * (t - T_DAM) / (T_HET - T_DAM))
            P.rot("all8", 2.5 * r)
            for j, b in enumerate(XUONG_PHIEN):
                P.rot(b, (2.0 if j % 2 else -2.0) * r)
            P.rot("ham", -14.0 * hoat.cv(t, [(T_DAM, 0.4), (T_DAM2, 1.0, "out"), (T_HET, 0.8), (T_HET + 0.2, 0.0, "io")]))
        for td in (T_DAM, T_DAM2):                               # chạm đất: bẹp rồi nảy
            if t > td:
                b = math.exp(-(t - td) / 0.08) * math.sin((t - td) * 2 * math.pi / 0.22)
                P.scale("day", 1 + 0.10 * b, 1 - 0.12 * b)
        if t < T_DAM:
            P.move("day", 0.0, 16.0 * hoat.cv(t, [(0.0, 0.0), (T_GIO, 1.0, "io"), (T_DAM, 0.0, "in")]))
        phap_phong(P, t, 0.5)

    # ------------------------------------------------ appear: nhảy từ trên xuống, đáp phịch, dang tay gầm, về đứng
    P_NHAY = dang("skill_02", 0.17)                             # dáng nhảy co người

    def f_appear(t, P):
        dat(P, "idle_01", 0.0)
        if t < T_ROI_A:
            for sl in sk.slots:
                P.alpha[sl["name"]] = 0.0
            P.move("day", 0.0, 1.6 * cao)
            return
        if t < T_DAP_A:
            u = (t - T_ROI_A) / (T_DAP_A - T_ROI_A)
            P.move("day", 0.0, 1.3 * cao * (1 - ease(u, "in")))
            pha(P, P_NHAY, 1.0 - 0.6 * ease(u, "in"))
        else:
            b = math.exp(-(t - T_DAP_A) / 0.09) * math.sin((t - T_DAP_A) * 2 * math.pi / 0.24)
            P.scale("day", 1 + 0.14 * b, 1 - 0.16 * b)
            gam = hoat.cv(t, [(T_DAP_A, 0.0), (T_DAP_A + 0.12, 0.0), (T_GAM_A, 1.0, "out"), (1.22, 1.0), (D_APPEAR - 0.05, 0.0, "io")])
            tt_gio(P, 0.85 * gam)
            if T_GAM_A < t < 1.22:
                r = hoat.rung(t, T_GAM_A, 1.22, 2)
                P.rot("all8", 2.0 * r)
            P.rot("ham", -20.0 * gam)
            for j, b_ in enumerate(XUONG_PHIEN):                 # phiến lạch cạch khi chạm đất, dựng lúc gầm
                P.rot(b_, 7.0 * gam + 5.0 * math.exp(-(t - T_DAP_A) / 0.1) * math.sin((t - T_DAP_A - 0.02 * j) * 2 * math.pi / 0.12))

    # ------------------------------------------------ die: die_01 + phiến mũ trùm rơi lả tả + mờ
    D_DIE = CD["die_01"][0]
    ROI = [("all30", "p3", 0.30), ("all28", "p1", 0.36), ("all29", "p2", 0.42), ("all26", "p5", 0.48), ("all27", "p6", 0.54)]

    def f_die(t, P):
        dat(P, "die_01", t)
        for j, (b, s, t0) in enumerate(ROI):
            if t <= t0:
                continue
            c0 = sk.atts[s][s]["V"].mean(0)
            W = sk.the_gioi(P)
            c = (W[b] @ np.linalg.solve(sk.W0[b], np.array([c0[0], c0[1], 1.0])))[:2]
            u = t - t0
            g_ = 1500.0
            h0 = max(0.0, c[1] - (y_day + 30.0))
            t_cham = math.sqrt(2 * h0 / g_) if h0 > 0 else 0.0
            if u < t_cham:
                dy = -0.5 * g_ * u * u
            else:
                v = u - t_cham
                dy = -h0 + max(0.0, 90.0 * v - 0.5 * g_ * v * v)
            dx = (-90.0, -50.0, -120.0, -70.0, -40.0)[j] * min(u, t_cham + 0.12)
            quay = (-40.0, 32.0, -50.0, 26.0, -30.0)[j] * min(1.0, u / max(0.15, t_cham))
            xoay_quanh(P, b, c, quay)
            Wp = sk.the_gioi(P)[sk.bones[sk.bi[b]]["parent"]]
            dl = np.linalg.solve(Wp[:2, :2], np.array([dx, dy]))
            P.move(b, float(dl[0]), float(dl[1]))
        dam(P, float(np.clip(1.0 - (t - D_DIE) / (TAN - 0.1), 0.0, 1.0)))

    ev_cast = [(0.05, "xoe", "")] + [(round(T_PHONG[k_], 4), "phong", k_) for k_ in PHIEN] + [(round(T_TRUNG_CAST, 3), "trung", "")] + \
              [(round(T_PHONG[k_] + BAY + GIU + VE, 3), "ve", k_) for k_ in PHIEN]
    ev_skill = [(0.08, "tu", ""), (T_DAM, "dam", "1"), (T_DAM2, "dam", "2"), (T_TRUNG_SKILL, "trung", ""), (T_HET, "het", "")]
    clips = [
        Clip("appear", D_APPEAR, boc(f_appear), ev=[(T_DAP_A, "dap", ""), (T_GAM_A, "gam", "")]),
        Clip("idle", 4.0, boc(f_idle), loop=True, ev=[(T_RU0 + 0.1, "ru", "")]),
        Clip("walk", CD["run_01"][0], boc(f_walk), loop=True),
        Clip("attack", D_ATTACK, boc(f_attack), ev=[(0.38, "lao", ""), (T_DOP, "trung", "")], trung=T_DOP),
        Clip("cast", D_CAST, boc(f_cast), ev=ev_cast, trung=T_TRUNG_CAST),
        Clip("skill", D_SKILL, boc(f_skill), ev=ev_skill, trung=T_TRUNG_SKILL),
        Clip("hit", CD["hit_01"][0], boc(f_hit)),
        Clip("die", D_DIE + TAN, boc(f_die), ev=[(0.75, "roi", "")]),
    ]
    return clips, than_cast


def them_phien_bay(sk, info, than_cast, cao):
    """xương far + fly_<k> (tâm phiến lúc rời) + bay_<k> (dáng phiến lúc rời) và slot bản sao (ẩn, vẽ trước hết) cho năm phiến bay."""
    sk.xuong("far", "root", 0.9 * cao + 140.0, 0.45 * cao)
    for k_, (s, rb) in PHIEN.items():
        P = khung.Pose()
        than_cast(T_PHONG[k_], P)
        W = sk.the_gioi(P)
        att = sk.atts[s][s]
        V = np.array([sum(w * (W[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in att["verts"]])
        c = V.mean(0)
        sk.xuong(f"fly_{k_}", "root", float(c[0]), float(c[1]))
        sk.xuong(f"bay_{k_}", f"fly_{k_}", float(c[0]), float(c[1]), goc=_goc(W[rb]), the_gioi=True)
        inv = np.linalg.inv(sk.W0[f"bay_{k_}"])
        rows = [[(f"bay_{k_}", *[float(q) for q in (inv @ np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
        sk.slot(f"bay_{k_}", "move", s, an=True)
        sk.luoi_gan(f"bay_{k_}", s, sk.luoi[(s, s)], trongso.cung(len(rows), "move"), the_gioi=V)
        sk.atts[f"bay_{k_}"][s]["verts"] = rows
        REF[k_] = (rb, W[rb].copy())


def dung_het(far_xy=None):
    """dựng đủ rig + clip (cho bản xem trước tho5_fx_than_lan_cat2.py): trả (sk, info, clips, cao)."""
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips, than_cast = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0) - info["y_day"]
    them_phien_bay(sk, info, than_cast, cao)
    if far_xy is not None:
        b = sk.bones[sk.bi["far"]]
        b["x"], b["y"] = float(far_xy[0]), float(far_xy[1])
        sk.W0 = sk.the_gioi()
    clips, _ = lam_clip(sk, info, cao)
    return sk, info, clips, cao


def main(a):
    sk, info, clips, cao = dung_het()
    ve0 = soi.Ve(sk)
    idle0 = hoat.nuong(sk, clips[1])[0]
    print(f"chiều cao {cao:.0f}")
    if a and a[0] == "kiem":
        for c in clips:
            fr = hoat.nuong(sk, c)
            xau = []
            al = lambda P, s: P.alpha.get(s, sk.slots[sk.si[s]]["alpha"])
            for i in range(1, len(fr)):
                A, B = fr[i - 1], fr[i]
                for b in set(A.t) | set(B.t):
                    da = abs(B.t.get(b, khung.ZERO)[2] - A.t.get(b, khung.ZERO)[2])
                    if da > 35.0 and not b.startswith("bay_"):
                        xau.append(f"{i / 30:.2f}s {b} xoay {da:.0f}°")
            Wl = [sk.the_gioi(P) for P in fr]
            for s, b in (("than", "all5"), ("dau", "all8"), ("p3", "all30"), ("p2", "all29"), ("tay_gan", "all48"), ("tay_xa", "all51"),
                         ("bay_1", "bay_1"), ("bay_5", "bay_5")):
                if b not in sk.bi:
                    continue
                for i in range(1, len(fr)):
                    d = float(np.hypot(*(Wl[i][b][:2, 2] - Wl[i - 1][b][:2, 2])))
                    if al(fr[i], s) > 0.5 and al(fr[i - 1], s) > 0.5 and d > 0.22 * cao:
                        xau.append(f"{i / 30:.2f}s {s} dời {d / cao:.2f} cao/khung")
            print(f"{c.ten}: {len(fr)} khung" + ("" if not xau else " | " + "; ".join(xau[:14]) + (" ..." if len(xau) > 14 else "")))
        return
    if a and a[0] == "soi":
        c = [x for x in clips if x.ten == a[1]][0]
        fr = hoat.nuong(sk, c)
        if ":" in a[2]:
            t0, t1, n = a[2].split(":")
            ts = list(np.linspace(float(t0), float(t1), int(n)))
        elif a[2].startswith("n="):
            ts = list(np.linspace(0, c.dur, int(a[2][2:])))
        else:
            ts = [float(x) for x in a[2].split(",")]
        Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
        bxs = [ve0.bao(P) for P in Ps if any(x[5] > 0.02 for x in ve0.skin(P)[0])] or [ve0.bao(idle0)]
        Bx = soi._union(bxs, 0.04)
        sc = float(a[3]) if len(a) > 3 else 0.4
        cot = min(len(Ps), 6)
        hang = (len(Ps) + cot - 1) // cot
        out = None
        for i, P in enumerate(Ps):
            im = ve0.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
            d = ImageDraw.Draw(im)
            d.text((6, 4), f"{ts[i]:.2f}", fill=(255, 255, 255))
            if out is None:
                out = Image.new("RGB", (im.width * cot, im.height * hang), (150, 150, 150))
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de="Sa Tích dạng 2 (than_lan_cat_2): tướng ải 5 đảo Thổ", dang=2, so_dang=2,
                  dung_yen=("cast", "skill"), far=("cast",), far_aim=("cast",), ma_goc=None, khop_idle=0.2, cao=cao, impact=IMPACT,
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.3, tran_mb=0.5, span=3.8)


if __name__ == "__main__":
    main(sys.argv[1:])
