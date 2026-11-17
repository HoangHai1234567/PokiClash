# -*- coding: utf-8 -*-
"""Thằn lằn áo choàng đất nung (than_lan_cat; tướng 2 đảo Thổ, ải 5): hình của mình chạy trên ĐÚNG rig của con gốc monster_3257 (game
tham khảo). Ghi chú: inbox/than_lan_cat_ghichu.md. Cách làm như quang_sat_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ xương của họ (FK; 5 IK của họ đã được runtime nướng vào biến đổi riêng `l` của mẫu khung), thêm `move` (cú lao), `day` (đáy
  thân), `tam` (tâm thân, cha của `bone`), `far` + `fly_k`, `bay_k` (ba phiến áo choàng bay của chiêu mana: game co quãng tới đối thủ,
  farAim), `mieng` (miệng, con của đầu), `ao4` (phiến thứ tư, con của bone4: rơi ở die), `cat_x` (mặt nạ cắt: trồi khỏi đất ở appear).
- MẢNH: ảnh của mình "đúng chỗ, đúng cỡ" (than_lan_cat_manh.py → inbox/than_lan_cat_1/manh/), đặt vào thế giới rig ở dáng idle 0; mỗi
  mảnh là lưới phủ hình, mỗi đỉnh biến dạng ĐÚNG như điểm tương ứng trên lưới của họ (trọng số + điểm gắn riêng từng xương). Mỗi chi
  của mình là MỘT mảnh liền bám HỢP các part của họ (đùi + cẳng + ngón), khỏi đường nối. Mắt hai hình (mở / nhắm theo khung của họ).
  BỎ slot shadow, gai cằm P_qi04 (concept không có), và các part chi đã gộp.
- CHUYỂN ĐỘNG (đề xuất tho5_anim.py, người dùng "làm đi" 2026-11-17):
    idle   = MỀM: khung 0 idle_01 + sóng sin lệch pha (thở 2 %, đầu trễ 0,1 s, phiến trễ 0,15–0,35 s, đuôi chu kỳ 4 s) + nghiêng
             đầu, chớp mắt chậm, thè lưỡi nếm gió một nhịp chậm (2,45 → 3,55 s);
    walk   = run_01; hit = hit_01;
    attack = skill_01 (chồm lên rồi phóng rạp đớp, lưỡi quất) + lao tới bằng `move`, hàm há rồi đớp đúng khung trúng;
    cast   = skill_02 (xoè áo choàng, há miệng rít) + BA PHIẾN ÁO CHOÀNG bay găm vào đối thủ rồi bay về lắp đúng chỗ (code lái far);
    skill  = xoè mũ trùm (skill_02) + nhổm lên rồi ĐẬP hai chân trước xuống (skill_01), giữ dáng rít rung tới khi lốc cát (VFX) tan;
    appear = trồi khỏi đất: đầu và mũ trùm nhô lên, hai chân trước BẤU đất (chi chĩa về chỗ bấu đứng yên) kéo thân lên, rũ cát, xoè mũ;
    die    = die_01 + bốn phiến áo choàng rơi lả tả xuống đất + mờ.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/than_lan_cat_rig.py        → inbox/than_lan_cat_1/rig/
    py -3 -I ArtGen/Spine/than_lan_cat_rig.py soi <clip> <giây,giây,...|n=12|t0:t1:n> [tỉ lệ]   → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/than_lan_cat_rig.py kiem                                            đo góc nhảy, bước dời
    TLC_GOC=1 ...                                                                             chạy thử bằng da gốc (manh_goc)
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
from quai.soi import _tris  # noqa: E402
import tho5  # noqa: E402
from hoa_ho_rig import ease, tmap, _goc  # noqa: E402

G = tho5.dat("than_lan_cat")
TEN_RIG = "than_lan_cat_1"
GOC = os.environ.get("TLC_GOC") == "1"
D_PX = float(os.environ.get("TLC_DPX", "1.4"))       # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~270 đơn vị)
MANH = os.path.join(G.BASE, "manh_goc" if GOC else "manh")
RA = os.environ.get("TLC_RA") or os.path.join(G.BASE, "rig_goc" if GOC else "rig")
TAN = 0.45
FPS = 30.0
W_C, H_C = 1536, 1024
IMPACT = {"attack": (0.05, 0.30, 0.08), "cast": (0.05, 0.28, 0.06), "skill": (0.12, 0.60, 0.12, "#ffffff40")}

# slot của mình (thứ tự vẽ, sau → trước): (slot, [hình], nguồn gắn: list slot của họ ở idle 0 | "ao4" | "luoi")
SLOT = [
    ("P_shoubi01", ["tay_xa"], ["P_shoubi04", "P_shoubi01", "P_shouzhi02"]),
    ("P_jiao03", ["chan_xa"], ["P_jiao04", "P_jiao03", "P_jiaozhi02"]),
    ("P_weiba01", ["duoi"], ["P_weiba01"]),
    ("P_shenti", ["than"], ["P_shenti"]),
    ("P_jiao01", ["chan_gan"], ["P_jiao02", "P_jiao01", "P_jiaozhi01"]),
    ("P_shoubi02", ["tay_gan"], ["P_shoubi03", "P_shoubi02", "P_shouzhi01"]),
    ("P_qi03", ["ao3"], ["P_qi03"]),
    ("P_qi02", ["ao2"], ["P_qi02"]),
    ("P_qi01", ["ao1"], ["P_qi01"]),
    ("ao4", ["ao4"], "ao4"),
    ("long_mieng", ["long_mieng"], "ham_cung"),          # lòng miệng: cứng trên xương hàm, nấp sau đầu khi ngậm
    ("P_zhui", ["ham"], ["P_zhui"]),
    ("P_shetou", ["luoi"], "luoi"),
    ("P_tou", ["dau"], ["P_tou"]),
    ("P_yanjing01", ["mat", "mat_nham"], ["P_yanjing01"]),
]
PHIEN = {"3": ("P_qi03", "ao3", "bone9"), "2": ("P_qi02", "ao2", "bone8"), "1": ("P_qi01", "ao1", "bone7")}   # phiến bay của cast
CHAN_TRUOC = {"gan": ("bone28", "bone11", "bone12"), "xa": ("bone29", "bone13", "bone14")}
GIAM_QI = {"skill_02": {"bone7": 0.45, "bone8": 0.40, "bone9": 0.32, "bone10": 0.45},
           "skill_01": {"bone7": 0.6, "bone8": 0.55, "bone9": 0.5}}
MAU_NHOM = {"mu": {"bone27", "bone6", "bone7", "bone8", "bone9", "bone10", "bone15", "bone31", "bone32", "bone33", "bone34"}}


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
    thu = MANH
    DATJ = json.load(open(os.path.join(thu, "dat.json")))
    if ten not in DATJ:
        thu = os.path.join(G.BASE, "manh_goc")
        DATJ = json.load(open(os.path.join(thu, "dat.json")))
        print(f"  (tạm) {ten}: lấy từ manh_goc")
    s_px, _, _ = tf()
    g = Image.open(os.path.join(thu, ten + ".png")).convert("RGBA")
    kq = D_PX / s_px
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), DATJ[ten]["hop"], kq


def hop_luoi(a0s, ten):
    """gộp lưới của nhiều hình của họ (idle 0) thành một: đỉnh, tam giác, trọng số {tên xương: w}."""
    Qs, Ts, Wg, off = [], [], [], 0
    for a0 in a0s:
        Q = np.array(a0["xy"], float).reshape(-1, 2)
        if "tris" in a0:
            tr = np.array(a0["tris"]).reshape(-1, 3)
        else:                                            # hình chữ nhật (region): 4 góc
            tr = np.array([[0, 1, 2], [2, 3, 0]])
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
    """mỗi điểm V (thế giới) biến dạng như điểm tương ứng trên HỢP lưới của họ a0s: toạ độ trọng tâm trong tam giác chứa nó (nhiều tam
    giác chứa: lấy của hình vẽ SAU CÙNG; ngoài lưới: điểm gần nhất trên cạnh + khoảng lệch), trọng số W_b = Σ β_k w_b(k), điểm gắn riêng
    q_b = Σ β_k w_b(k) v_k / W_b (xem rong_vay_rig.gan_goc, quang_sat_rig.trong_so_goc). Trả hàng (xương, x, y, w) theo ma trận Wi."""
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


# người dùng chê "bụng bị lỗi" (walk 0,2: nét mực vụn, khe hở giữa chân sau gần và chân trước gần): đỉnh của mình nằm trên tam giác của
# part họ khác nhau (đùi / cẳng / thân / gốc đuôi) nhận trọng số nhảy bậc → bước đi thì tam giác gập, viền lộn ra giữa hình. Làm mịn
# trọng số trên lưới của mình (số vòng) rồi gắn kiểu LBS (điểm gắn = đỉnh trong hệ từng xương), bỏ ảnh hưởng xương lạ.
MUOT = {"P_shenti": 10, "P_jiao01": 8, "P_shoubi02": 8, "P_shoubi01": 8, "P_jiao03": 8, "P_weiba01": 4}
# chân sau của mình nằm thấp hơn đùi của họ (phần lộ ra là cẳng + bàn): bỏ ảnh hưởng xương đùi, khỏi nếp gấp ngang đùi khi gối gập
BO_XUONG = {"P_shenti": ("bone17", "bone18", "bone19"), "P_jiao01": ("bone21",), "P_jiao03": ("bone24",)}


def lam_muot(rows, V, tris, Wi, vong, bo=()):
    """trọng số mỗi đỉnh (gộp theo xương) → trung bình với láng giềng trên lưới `vong` lần (giữ 50 % của chính nó), bỏ xương trong `bo`,
    giữ ≤ 4 xương, chuẩn hoá; điểm gắn từng xương = đỉnh (thế giới idle 0) trong hệ xương đó."""
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


def gan_manh(sk, slot, ten_anh, a0s, ten, Wi, M=None, mot_xuong=None):
    """mảnh của mình (manh/<ten_anh>.png, hộp trên concept) → lưới đặt đúng chỗ concept ở dáng idle 0 (M: đổi chỗ thế giới, cho lưỡi).
    a0s: list hình của họ để gắn theo (lưới hợp) ; mot_xuong: (xương, ma trận) → ô 4 đỉnh bám cứng một xương."""
    im, (x0, y0, x1, y1), kq = anh_manh(ten_anh)
    if ten_anh not in sk.images:
        sk.anh(ten_anh, im)
    im = sk.images[ten_anh]
    _, to_rig, _ = tf()
    if mot_xuong is None:
        L = luoi.luoi_vung(im, buoc_vien=9.0, buoc_trong=14.0, vien=2, ten=f"{slot}/{ten_anh}", in_tk=False)
    else:
        L = luoi.luoi_o(im.width, im.height, 2, 2, ten=slot)
    Px = np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1)
    V = to_rig(Px)
    if M is not None:
        V = (M @ np.c_[V, np.ones(len(V))].T).T[:, :2]
    if mot_xuong is None:
        rows = trong_so_goc(V, a0s, ten, Wi)
        if MUOT.get(slot, 0) > 0:
            rows = lam_muot(rows, V, L.tris, Wi, MUOT[slot], BO_XUONG.get(slot, ()))
    else:
        b, Mb = mot_xuong
        rows = [[(b, *[float(v) for v in np.linalg.solve(Mb, np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
    Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
    sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=Vs)
    sk.atts[slot][ten_anh]["verts"] = rows
    return L


def khop_luoi_luoi(a_luoi):
    """ma trận affine đưa ảnh lưỡi của mình (đặt theo hộp trên concept → thế giới idle 0) về đúng chỗ lưỡi của họ ở DÁNG GỐC (att_goc):
    khớp tâm, trục dài (PCA), độ dài; gốc lưỡi (đầu trên trái của ảnh) về đầu gần xương hàm."""
    im, (x0, y0, x1, y1), kq = anh_manh("luoi")
    _, to_rig, _ = tf()
    al = np.asarray(im)[..., 3] > 100
    ys, xs = np.nonzero(al)
    P = to_rig(np.stack([x0 + xs / kq, y0 + ys / kq], 1))
    Q = np.array(a_luoi["xy"], float).reshape(-1, 2)

    def truc(X):
        c = X.mean(0)
        _, _, vt = np.linalg.svd(X - c)
        ax = vt[0]
        t = (X - c) @ ax
        return c, ax, t.max() - t.min()

    cP, aP, lP = truc(P)
    cQ, aQ, lQ = truc(Q)
    # gốc ảnh của mình: phía trên trái của ảnh = điểm có (x - y) ảnh nhỏ nhất → trên thế giới: x nhỏ, y lớn
    goc_m = P[np.argmin(P[:, 0] - P[:, 1])]
    if np.dot(goc_m - cP, aP) > 0:
        aP = -aP                                         # aP chĩa từ gốc ra chóp
    j_ham = a_luoi["_ham"]
    if np.dot(j_ham - cQ, aQ) > 0:
        aQ = -aQ
    aP, aQ = -aP, -aQ                                    # cả hai chĩa gốc → chóp
    s = lQ / max(lP, 1e-6)
    ang = math.atan2(aQ[1], aQ[0]) - math.atan2(aP[1], aP[0])
    ca, sa = math.cos(ang) * s, math.sin(ang) * s
    R = np.array([[ca, -sa], [sa, ca]])
    t = cQ - R @ cP
    M = np.eye(3)
    M[:2, :2], M[:2, 2] = R, t
    return M


# ---------------------------------------------------------------- dựng
def dung():
    D, D0, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    Wc, Wi = mats(D), mats(D0)
    by0 = {a["slot"]: a for a in D0["atts"]}
    byg = {a["slot"]: a for a in D["atts"] if a["cur"] or a["slot"] == "P_shetou"}
    P_all = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in D0["atts"] if a.get("region")])
    y_day = float(P_all[:, 1].min())
    Vb = np.array(by0["P_shenti"]["xy"], float).reshape(-1, 2)
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
    # mặt nạ cắt (trồi khỏi đất), phiến thứ tư (con của bone4, gốc trùng bone4), miệng (con của đầu, ở chóp mõm concept)
    sk.xuong("cat_x", "move", float(tam[0]), -CAT_SAU, sx=CAT_TI, sy=CAT_TI)
    sk.xuong("ao4", "bone4", 0.0, 0.0)
    s_px, to_rig, _ = tf()
    p_mieng = to_rig(np.array([[1188.0, 520.0]]))[0]
    sk.xuong("mieng", "bone27", 0.0, 0.0)
    # đặt `mieng` theo thế giới dáng gốc: chỗ chóp mõm ở idle 0 đổi về dáng gốc qua xương đầu
    Ml = np.linalg.solve(Wi["bone27"], np.array([p_mieng[0], p_mieng[1], 1.0]))
    sk.bones[sk.bi["mieng"]]["x"], sk.bones[sk.bi["mieng"]]["y"] = float(Ml[0]), float(Ml[1])
    sk.bones[sk.bi["mieng"]]["rot"] = 20.9                          # trục x mõm chĩa phải (đầu xoay −20,9° ở dáng gốc)
    sk.W0 = sk.the_gioi()
    # ---- slot
    sk.slot("cat", "cat_x")
    tong = [0, 0]
    Wb_ao4 = dict(Wi)
    Wb_ao4["ao4"] = Wi["bone4"]
    for s, hinhs, nguon in SLOT:
        sk.slot(s, "move", hinhs[0], an=(s == "P_shetou"))
        for h in hinhs:
            if nguon == "ao4":
                L = gan_manh(sk, s, h, None, ten, Wi, mot_xuong=("ao4", Wi["bone4"]))
            elif nguon == "ham_cung":
                L = gan_manh(sk, s, h, None, ten, Wi, mot_xuong=("bone6", Wi["bone6"]))
            elif nguon == "luoi":
                a_l = dict(byg["P_shetou"])
                a_l["_ham"] = Wc["bone6"][:2, 2]
                M = khop_luoi_luoi(a_l)
                L = gan_manh(sk, s, h, [a_l], ten, Wc, M=M)
            elif s == "P_yanjing01":
                L = gan_manh(sk, s, h, None, ten, Wi, mot_xuong=("bone15", Wi["bone15"]))
            else:
                L = gan_manh(sk, s, h, [by0[x] for x in nguon], ten, Wi)
            tong[0] += L.n
            tong[1] += len(L.tris)
    sk.cat("cat", "P_yanjing01", mat_na(float(tam[0])))
    for e, m in (("trung", "khung trúng"), ("phong", "cast: một phiến áo choàng rời thân (chuỗi = 3 / 2 / 1)"),
                 ("ve", "cast: phiến lắp lại"), ("dam", "skill: hai chân trước đập đất (VFX bụi, rung; lốc cát bắt đầu ở đối thủ)"),
                 ("het", "skill: lốc cát tan, thu mũ trùm"), ("troi", "appear: đất / cát nổ, đầu nhô lên (VFX)"),
                 ("bam", "appear: chân trước bấu đất (VFX bụi nhỏ)"), ("ru_cat", "appear: rũ cát (VFX cát rơi)"),
                 ("liem", "idle: thè lưỡi nếm gió"), ("roi", "die: phiến áo choàng chạm đất (VFX bụi)"),
                 ("lao", "attack: bắt đầu phóng tới (VFX bụi sau chân)"), ("xoe", "cast: áo choàng bắt đầu xoè (VFX cát bốc nhẹ)"),
                 ("tu", "skill: xoè mũ, nhổm lên (VFX cát xoáy quanh chân đối thủ bắt đầu tụ)")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; đáy y = {y_day:.1f}, tâm thân "
          f"({tam[0]:.1f}, {tam[1]:.1f})")
    return sk, dict(IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], y_day=y_day, tam=tam, S=S, Wi=Wi)


CAT_TI, CAT_SAU = 12.0, 3000.0


def mat_na(x_tam):
    """đa giác LỒI của mặt nạ (hệ của cat_x khi về đúng chỗ: gốc ở mặt đất dưới tâm thân): giữ phần TRÊN mặt đất. Ở dáng gốc xương nằm
    sâu CAT_SAU và phóng CAT_TI lần (không cắt gì); clip đặt về đúng chỗ, cỡ khi cần."""
    pts = [(-1500.0, 0.0), (1500.0, 0.0), (1500.0, 2200.0), (-1500.0, 2200.0)]
    return [(x_tam + px * CAT_TI, -CAT_SAU + py * CAT_TI) for px, py in pts]


# ---------------------------------------------------------------- chuyển động của họ
def chuyen_dong(info):
    S, ten, goc0 = info["S"], info["ten"], info["goc0"]
    out = {}
    sl = info["slots"]
    i_mat, i_luoi = sl.index("P_yanjing01"), sl.index("P_shetou")
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
        mat = ["mat_nham" if F["n"][i_mat] == "P_yanjing02" else "mat" for F in fr]
        luoi_ = [bool(F["n"][i_luoi]) for F in fr]
        out[clip] = (float(v["dur"]), res, len(fr), mat, luoi_)
    return out


# ---------------------------------------------------------------- mốc giờ
T_DOP = 0.56                                            # attack: đớp trúng (khung lao rạp của skill_01)
LAO = 0.42                                              # attack: lao tới (× chiều cao) ở khung đớp; game nắn lại
T_PHONG = {"3": 14 / 30.0, "2": 16 / 30.0, "1": 18 / 30.0}   # cast: phiến rời thân (bội 1/30)
BAY, GIU, VE = 0.20, 0.18, 0.30
TV = max(T_PHONG.values()) + BAY + GIU + VE             # phiến cuối lắp lại
D_CAST = TV + 0.34
T_NHOM, T_DAM, T_HET, D_SKILL = 0.42, 0.62, 1.78, 2.20   # skill: nhổm lên, đập đất, thu mũ, hết
T_TRUNG_SKILL = 1.00
T_TROI, T_BAM, T_LEN, T_RU, D_APPEAR = 0.12, 0.56, 0.95, 1.25, 1.60
T_LIEM0, T_LIEM1 = 2.45, 3.35                           # idle: lè lưỡi liếm mắt


def lam_clip(sk, info, cao=270.0):
    CD = chuyen_dong(info)
    tam = info["tam"]
    y_day = info["y_day"]
    far = sk.W0["far"][:2, 2] if "far" in sk.bi else np.array([0.9 * cao + 140.0, 0.45 * cao])

    def dat(P, goc, tau, lap=False, chi=None, bo=None, mat=True):
        dur, R, n, M, LU = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        giam = GIAM_QI.get(goc, {})
        for b, A in R.items():
            if chi is not None and b not in chi:
                continue
            if bo is not None and b in bo:
                continue
            v = A[i0] * (1 - w) + A[i1] * w
            if b in giam:                                   # phiến của mình là ngói xếp lớp: xoè ít hơn diềm của họ
                f = giam[b]
                v = np.array([v[0] * f, v[1] * f, v[2] * f, 1 + (v[3] - 1) * f, 1 + (v[4] - 1) * f])
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        k = min(n - 1, int(round(x)))
        if mat:
            P.att["P_yanjing01"] = M[k]
            P.alpha["P_shetou"] = 1.0 if LU[k] else 0.0

    def dam(P, a):
        if a < 0.999:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])

    def pha(Pa, Pb, w):
        Q = khung.Pose()
        for b in set(Pa.t) | set(Pb.t):
            a_ = Pa.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            b_ = Pb.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            Q.t[b] = [a_[q] + (b_[q] - a_[q]) * w for q in range(5)]
        Q.alpha = dict(Pa.alpha if w < 0.5 else Pb.alpha)
        Q.att = dict(Pb.att if w > 0.5 else Pa.att)
        return Q

    def dat_tg(P, b, xy, goc_tg, k=1.0, gan=None):
        """đặt xương b tới chỗ xy, góc goc_tg THẾ GIỚI (trong tư thế P); k = mức hoà 0..1; gan: góc riêng tham chiếu (giữ liền mạch giữa
        các khung: chọn bội 360 gần nó nhất thay vì gần góc hiện tại)."""
        if k <= 1e-4:
            return
        W = sk.the_gioi(P)
        cha = sk.bones[sk.bi[b]]["parent"]
        Wp = W[cha]
        lp = np.linalg.solve(Wp, np.array([xy[0], xy[1], 1.0]))
        b0 = sk.bones[sk.bi[b]]
        g = P._g(b)
        dx, dy = float(lp[0]) - b0["x"], float(lp[1]) - b0["y"]
        dr = goc_tg - _goc(Wp) - b0["rot"]
        cur = _goc(W[b]) - _goc(Wp) - b0["rot"] if gan is None else gan
        dr = cur + ((dr - cur + 180.0) % 360.0 - 180.0)
        g[0] += k * (dx - g[0])
        g[1] += k * (dy - g[1])
        g[2] += k * (dr - g[2])

    IK_TRUOC = {}                                            # (xương) → (giờ, góc thêm khung trước): giữ liền mạch giữa các khung

    def lien(b, t, d):
        """chọn bội 360 của góc thêm d gần góc thêm khung trước nhất (khỏi nhảy một vòng khi góc vượt ±180)."""
        tr = IK_TRUOC.get(b)
        if tr is not None and tr[0] <= t + 1e-9 and t - tr[0] < 0.2:
            d = tr[1] + ((d - tr[1] + 180.0) % 360.0 - 180.0)
        IK_TRUOC[b] = (t, d)
        return d

    def ik2(P, a, b, c, T, k=1.0, t=0.0, gap=None):
        """IK hai xương: xoay a rồi b cho gốc xương c tới điểm thế giới T (chiều gập cố định = chiều gập ở khung 0 idle); k = mức hoà."""
        if k <= 1e-4:
            return
        W = sk.the_gioi(P)
        pa, pb, pc = W[a][:2, 2], W[b][:2, 2], W[c][:2, 2]
        L1, L2 = float(np.hypot(*(pb - pa))), float(np.hypot(*(pc - pb)))
        d_v = np.asarray(T) - pa
        d = float(np.clip(np.hypot(*d_v), abs(L1 - L2) + 1e-3, L1 + L2 - 1e-3))
        u1, u2 = pb - pa, pc - pb
        if gap is None:
            gap = GAP.get(a) or (np.sign(u1[0] * u2[1] - u1[1] * u2[0]) or 1.0)
        cA = (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d)
        A = math.degrees(math.acos(max(-1.0, min(1.0, cA))))
        huong = math.degrees(math.atan2(d_v[1], d_v[0]))
        muon = huong - gap * A
        hien = math.degrees(math.atan2(u1[1], u1[0]))
        P.rot(a, lien(a, t, k * (((muon - hien + 180.0) % 360.0) - 180.0)))
        W = sk.the_gioi(P)
        pb, pc = W[b][:2, 2], W[c][:2, 2]
        u2 = pc - pb
        muon2 = math.degrees(math.atan2(T[1] - pb[1], T[0] - pb[0]))
        hien2 = math.degrees(math.atan2(u2[1], u2[0]))
        P.rot(b, lien(b, t, k * (((muon2 - hien2 + 180.0) % 360.0) - 180.0)))

    def aim1(P, a, c, T, k=1.0, t=0.0):
        """xoay MỘT xương a (cả chi theo) cho gốc xương c chĩa về điểm thế giới T: ổn định hơn IK hai xương khi cẳng ngắn (không lật
        khuỷu); bàn chân không đứng đúng điểm, chỉ đúng hướng."""
        if k <= 1e-4:
            return
        W = sk.the_gioi(P)
        pa, pc = W[a][:2, 2], W[c][:2, 2]
        hien = math.degrees(math.atan2(pc[1] - pa[1], pc[0] - pa[0]))
        muon = math.degrees(math.atan2(T[1] - pa[1], T[0] - pa[0]))
        P.rot(a, lien(a, t, k * (((muon - hien + 180.0) % 360.0) - 180.0)))

    GAP = {}
    _P0 = khung.Pose()
    dat(_P0, "idle_01", 0.0)
    _W0 = sk.the_gioi(_P0)
    for _a, _b, _c in CHAN_TRUOC.values():
        _u1, _u2 = _W0[_b][:2, 2] - _W0[_a][:2, 2], _W0[_c][:2, 2] - _W0[_b][:2, 2]
        GAP[_a] = float(np.sign(_u1[0] * _u2[1] - _u1[1] * _u2[0]) or 1.0)

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

    def tam_phien(s, h):
        return sk.atts[s][h]["V"].mean(0)

    def phap_phong(P, t, bien=1.0, chu_ky=2.0):
        """phiến áo choàng phập phồng so le (phiến trên trước, phiến dưới trễ), quanh gốc xương; chu kỳ chia hết 4 s."""
        for k, (b, tre, A) in enumerate((("bone9", 0.0, 2.2), ("bone8", 0.12, 2.6), ("bone7", 0.24, 3.0))):
            P.rot(b, bien * A * math.sin(2 * math.pi * (t - tre) / chu_ky))
        P.rot("ao4", bien * 1.6 * math.sin(2 * math.pi * (t - 0.36) / chu_ky))

    def cat_bat(P, bat):
        if bat:
            P.move("cat_x", 0.0, CAT_SAU)
            P.scale("cat_x", 1.0 / CAT_TI, 1.0 / CAT_TI)

    # ------------------------------------------------ idle: idle_01 + phập phồng + lè lưỡi liếm mắt
    W_i0 = None
    p_mat = sk.atts["P_yanjing01"]["mat"]["V"]
    mat_tg = np.array([p_mat[:, 0].min() + 0.30 * (p_mat[:, 0].max() - p_mat[:, 0].min()), p_mat[:, 1].mean()])  # tâm mắt gần (thế giới idle 0)

    def song_(t, chu_ky, tre=0.0):
        return math.sin(2 * math.pi * (t - tre) / chu_ky)

    def f_idle(t, P):
        """idle MỀM (người dùng chê idle tatu "giật, không mềm mại", 2026-11-17): dáng nền = khung 0 idle_01 đứng yên; mọi chuyển động là
        sóng sin lệch pha, biên độ nhỏ: thở (ngực nở 2 %, chu kỳ 2 s), cổ / đầu trễ 0,05 / 0,10 s, phiến áo choàng trễ 0,15–0,35 s, đuôi
        đung đưa chu kỳ 4 s trễ dần từng đốt; trò nhỏ: nghiêng đầu, chớp mắt chậm, thè lưỡi nếm gió một nhịp CHẬM (đều êm, không bật)."""
        dat(P, "idle_01", 0.0)
        th = song_(t, 2.0)
        P.scale("bone4", 1.0, 1.0 + 0.02 * th)               # ngực nở / xẹp
        P.rot("bone3", 0.8 * th)
        P.rot("bone5", -0.6 * song_(t, 2.0, 0.05))
        P.rot("bone27", 1.1 * song_(t, 2.0, 0.10))
        P.rot("bone6", -1.2 * (0.5 + 0.5 * song_(t, 2.0, 0.15)))   # hàm hé theo nhịp thở
        for b, tre, A in (("bone9", 0.15, 2.0), ("bone8", 0.25, 2.4), ("bone7", 0.35, 2.8), ("ao4", 0.30, 1.6)):
            P.rot(b, A * song_(t, 2.0, tre))
        for j, b in enumerate(("bone16", "bone17", "bone18", "bone19")):
            P.rot(b, (1.6 + 1.1 * j) * song_(t, 4.0, 0.12 + 0.15 * j))
        # trò nhỏ (2,45 → 3,55 s): nghiêng đầu tò mò, chớp mắt chậm, hé hàm thè lưỡi nếm gió một nhịp chậm
        if T_LIEM0 < t < T_LIEM1 + 0.2:
            ng = hoat.cv(t, [(T_LIEM0, 0.0), (T_LIEM0 + 0.40, 1.0, "io"), (T_LIEM1 - 0.15, 1.0), (T_LIEM1 + 0.2, 0.0, "io")])
            P.rot("bone27", 3.0 * ng)
            P.rot("bone5", 1.5 * ng)
            ha = hoat.cv(t, [(T_LIEM0 + 0.30, 0.0), (T_LIEM0 + 0.50, 1.0, "io"), (T_LIEM1, 1.0), (T_LIEM1 + 0.18, 0.0, "io")])
            P.rot("bone6", -9.0 * ha)
            ra = hoat.cv(t, [(T_LIEM0 + 0.40, 0.0), (T_LIEM0 + 0.62, 1.0, "io"), (T_LIEM0 + 0.68, 1.0), (T_LIEM1 - 0.02, 0.0, "io")])
            if T_LIEM0 + 0.30 < t < T_LIEM1 + 0.12:        # lưỡi chĩa sẵn từ lúc hàm bắt đầu hé (còn ẩn), hiện khi thò ra: không quét
                W = sk.the_gioi(P)
                dat_tg(P, "bone31", W["bone31"][:2, 2] + np.array([5.0, 0.0]) * ra, -20.0 + 6.0 * ra,
                       k=ease((t - T_LIEM0 - 0.30) / 0.09) * ease((T_LIEM1 + 0.12 - t) / 0.08))
                s_ = 0.55 + 0.55 * ra
                P.scale("bone31", s_, s_)                    # tỉ lệ đều: tỉ lệ lệch trục làm các đốt con xiên góc
                P.rot("bone33", 6.0 * song_(t, 0.5, T_LIEM0) * ra)
            P.alpha["P_shetou"] = 1.0 if ra > 0.15 else 0.0
        if T_LIEM0 + 0.10 < t < T_LIEM0 + 0.28:              # chớp mắt chậm
            P.att["P_yanjing01"] = "mat_nham"

    def f_walk(t, P):
        dat(P, "run_01", t, True)
        phap_phong(P, t, 0.7, 0.8)

    def f_hit(t, P):
        dat(P, "hit_01", t)

    # ------------------------------------------------ attack: chồm lên rồi phóng rạp đớp
    M_ATK = [(0.0, 0.0), (0.40, 0.44, "io"), (T_DOP, 0.56, "in"), (0.74, 0.70, "out"), (1.0, 1.0, "io")]

    def f_attack(t, P):
        tau = tmap(t, M_ATK)
        dat(P, "skill_01", tau)
        # lao tới: lùi nhẹ lúc chồm, phóng tới đúng khung đớp, giữ, lùi về
        lao = hoat.cv(t, [(0.0, 0.0), (0.38, -0.05, "io"), (T_DOP, LAO, "in"), (0.68, LAO), (0.96, 0.0, "io")])
        P.move("move", cao * lao, 0.0)
        # hàm: há to lúc phóng, đớp sập đúng khung trúng, nảy nhẹ
        ha = hoat.cv(t, [(0.0, 0.0), (0.34, 0.4, "io"), (T_DOP - 0.06, 1.0, "out"), (T_DOP, -0.15, "in"), (T_DOP + 0.10, 0.1, "out"),
                         (0.84, 0.0, "io")])
        P.rot("bone6", -32.0 * ha)
        k = math.exp(-((t - (T_DOP + 0.02)) / 0.05) ** 2)
        P.scale("day", 1 + 0.08 * k, 1 - 0.07 * k)          # duỗi dài theo chiều lao đúng khung chạm
        phap_phong(P, t, 0.6)

    # ------------------------------------------------ cast: xoè áo choàng, ba phiến bay găm rồi về
    M_CAST = [(0.0, 0.0), (0.42, 0.39, "io"), (TV, 0.91, "lin"), (D_CAST, 1.167, "io")]

    def than_cast(t, P):
        dat(P, "skill_02", tmap(t, M_CAST))
        if 0.42 < t < TV:
            P.rot("bone27", 1.6 * hoat.rung(t, 0.42, TV, 2))  # rít: hai dáng lệch đổi nhau

    def f_cast(t, P):
        than_cast(t, P)
        W = None
        for k, (s, h, rb) in PHIEN.items():
            t0 = T_PHONG[k]
            t_toi, t_ve0 = t0 + BAY, t0 + BAY + GIU
            t_ve1 = t_ve0 + VE
            fb, bb = f"fly_{k}", f"bay_{k}"
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
                pos = A + f * v + n * VONG_DI[k] * math.sin(math.pi * f)
                ang = g0 - 540.0 * ease((tt - t0) / BAY, "out")     # phiến xoay như phi tiêu (−1,5 vòng)
            elif tt < t_ve0:
                pos = far.copy()
                ang = g0 - 540.0 + 6.0 * math.sin((tt - t_toi) * 70.0) * math.exp(-(tt - t_toi) / 0.09)
            else:
                if W is None:
                    W = sk.the_gioi(P)
                rb_, Wl = REF[k]
                Mt = W[rb_] @ np.linalg.inv(Wl) @ sk.W0[bb]
                R_, gr = Mt[:2, 2], _goc(Mt)
                u = (tt - t_ve0) / VE
                e = ease(u, "io")
                pos = far * (1 - e) + R_ * e + n * VONG_VE[k] * math.sin(math.pi * u)
                g1 = gr + ((g0 - 540.0 - gr + 180.0) % 360.0 - 180.0)
                ang = (g0 - 540.0) * (1 - e) + (g1 - 360.0) * e
            P.move(fb, float(pos[0] - A[0]), float(pos[1] - A[1]))
            P.rot(bb, float(ang - g0))

    # ------------------------------------------------ skill: xoè mũ trùm, nhổm lên, đập hai chân trước, giữ dáng rít rung
    mu = MAU_NHOM["mu"]

    M_SKILL = [(0.0, 0.0), (T_NHOM, 0.39, "io"), (T_DAM, 0.50, "out"), (T_HET, 0.85, "lin"), (D_SKILL, 1.167, "io")]

    def f_skill(t, P):
        # cả con theo skill_02 (xoè mũ trùm, há miệng rít); mình tự thêm cú nhổm + ĐẬP hai chân trước (IK bám đúng chỗ chân của dáng gốc)
        tau = tmap(t, M_SKILL)
        dat(P, "skill_02", tau)
        Pg = khung.Pose()
        dat(Pg, "skill_02", tau, mat=False)
        Wg = sk.the_gioi(Pg)
        nhac = hoat.cv(t, [(0.0, 0.0), (0.12, 0.0), (T_NHOM, 1.0, "out"), (T_DAM - 0.06, 1.05), (T_DAM, 0.0, "in")])
        for k, (a, b, c) in CHAN_TRUOC.items():
            goc_c = Wg[c][:2, 2]
            T = goc_c + np.array([0.10 * cao, 0.26 * cao]) * nhac * (1.0 if k == "gan" else 0.8)
            aim1(P, a, c, T, k=1.0, t=t)
            P.rot(b, -25.0 * nhac)                          # gập cẳng khi nhấc (vuốt chĩa xuống), duỗi lúc đập
        if T_DAM < t < T_HET:                                # giữ dáng rít: hai dáng lệch 2,5° đổi nhau mỗi 2 khung, nhỏ dần
            r = hoat.rung(t, T_DAM, T_HET, 2) * (1.0 - 0.5 * (t - T_DAM) / (T_HET - T_DAM))
            P.rot("bone27", 2.5 * r)
            P.rot("bone7", -2.0 * r)
            P.rot("bone8", 2.0 * r)
            P.rot("bone9", -2.0 * r)
        if t > T_DAM:                                        # chạm đất: bẹp rồi nảy
            b = math.exp(-(t - T_DAM) / 0.08) * math.sin((t - T_DAM) * 2 * math.pi / 0.22)
            P.scale("day", 1 + 0.10 * b, 1 - 0.12 * b)
        elif t > T_NHOM:
            u = ease((t - T_NHOM) / (T_DAM - T_NHOM), "in")
            P.move("day", 0.0, 18.0 * (1 - u))
        else:
            P.move("day", 0.0, 18.0 * ease(t / T_NHOM))

    # ------------------------------------------------ appear: trồi khỏi đất, bấu chân, kéo thân lên, rũ cát, xoè mũ
    W0i = {}

    def chan_dat(P0):
        W = sk.the_gioi(P0)
        return {k: W[c][:2, 2].copy() for k, (_, _, c) in CHAN_TRUOC.items()}

    P_i0 = khung.Pose()
    dat(P_i0, "idle_01", 0.0)
    BAM = chan_dat(P_i0)                                     # chỗ bấu = chỗ bàn chân trước ở khung 0 idle

    def f_appear(t, P):
        dat(P, "idle_01", 0.0)
        if t < T_TROI:
            for sl in sk.slots:
                P.alpha[sl["name"]] = 0.0
            cat_bat(P, True)
            P.move("day", 0.0, -1.2 * cao)
            return
        # độ sâu thân: vọt lên tới −0,30 cao (đầu, mũ trùm nhô lên) rồi kéo lên mặt đất
        sau = hoat.cv(t, [(T_TROI, -1.15), (0.42, -0.30, "out"), (T_BAM, -0.28), (T_LEN - 0.06, 0.03, "io"), (T_LEN, 0.0, "in")])
        P.move("day", 0.0, sau * cao)
        P.rot("tam", hoat.cv(t, [(T_TROI, 10.0), (0.42, -6.0, "out"), (T_BAM, -4.0), (T_LEN, 0.0, "io")]))
        cat_bat(P, t < T_LEN + 0.04)
        # hai chân trước: vươn lên trước rồi đập xuống bấu đúng chỗ đứng, giữ yên chỗ bám trong lúc thân được kéo lên
        for k, (a, b, c) in CHAN_TRUOC.items():
            tre = 0.0 if k == "gan" else 0.05
            tb = T_BAM + tre
            if not (0.30 + tre < t < T_LEN + 0.12):
                continue
            # hướng chĩa về chỗ bấu (đích đứng yên, vai đi lên đều → góc đổi êm), tính trên dáng chưa nhấc
            W = sk.the_gioi(P)
            pa, pc = W[a][:2, 2], W[c][:2, 2]
            hien = math.degrees(math.atan2(pc[1] - pa[1], pc[0] - pa[0]))
            muon = math.degrees(math.atan2(BAM[k][1] - pa[1], BAM[k][0] - pa[0]))
            d_aim = ((muon - hien + 180.0) % 360.0) - 180.0
            if t < tb:                                      # vươn lên trước (nhấc chi) rồi đập xuống, hoà dần sang hướng bấu
                u = (t - 0.30 - tre) / (tb - 0.30 - tre)
                nhac = 60.0 * math.sin(math.pi * min(1.0, u * 1.15))
                w = ease((t - (tb - 0.10)) / 0.10)
                P.rot(a, (1 - w) * nhac + w * d_aim)
                P.rot(b, -20.0 * math.sin(math.pi * u))
            else:
                P.rot(a, d_aim * (1.0 if t < T_LEN else 1.0 - ease((t - T_LEN) / 0.12)))
        # rũ cát: thân lắc, phiến lạch cạch trễ dần
        if T_LEN < t < T_RU + 0.1:
            u = (t - T_LEN) / (T_RU + 0.1 - T_LEN)
            r = math.sin((t - T_LEN) * 2 * math.pi / 0.12) * (1 - u)
            P.rot("tam", 3.5 * r)
            for b, tre, A in (("bone9", 0.02, 6.0), ("bone8", 0.04, 7.0), ("bone7", 0.06, 8.0), ("ao4", 0.08, 5.0)):
                P.rot(b, A * math.sin((t - T_LEN - tre) * 2 * math.pi / 0.12) * (1 - u))
        if t >= T_LEN:                                       # chạm đất: bẹp rồi nảy
            b = math.exp(-(t - T_LEN) / 0.08) * math.sin((t - T_LEN) * 2 * math.pi / 0.2)
            P.scale("day", 1 + 0.08 * b, 1 - 0.10 * b)
        if t > T_RU:                                         # xoè mũ một lần (skill_02 tới 0,39) rồi xếp lại
            w = hoat.cv(t, [(T_RU, 0.0), (T_RU + 0.14, 1.0, "out"), (D_APPEAR - 0.06, 0.0, "io")])
            Pq = khung.Pose()
            dat(Pq, "skill_02", 0.39, chi={"bone7", "bone8", "bone9", "bone10", "bone27"}, mat=False)
            for bn, g in Pq.t.items():
                q = P._g(bn)
                q[2] += w * g[2]
                q[0] += w * g[0]
                q[1] += w * g[1]
                q[3] *= 1 + w * (g[3] - 1)
                q[4] *= 1 + w * (g[4] - 1)

    # ------------------------------------------------ die: die_01 + phiến áo choàng rơi lả tả + mờ
    D_DIE = CD["die_01"][0]
    ROI = {"bone9": 0.38, "bone8": 0.46, "ao4": 0.52, "bone7": 0.58}      # giờ rời
    DIE_LUC = {}

    SL_PHIEN = {"bone9": ("P_qi03", "ao3"), "bone8": ("P_qi02", "ao2"), "bone7": ("P_qi01", "ao1"), "ao4": ("ao4", "ao4")}

    def f_die(t, P):
        dat(P, "die_01", t)
        # phiến rời thân: rơi theo trọng lực tới đất (tâm phiến chạm mặt đất), nảy một lần nhỏ rồi nằm, xoay quanh tâm của chính nó
        for j, (b, t0) in enumerate(ROI.items()):
            if t <= t0:
                continue
            s, h = SL_PHIEN[b]
            c0 = sk.atts[s][h]["V"].mean(0)                  # tâm phiến ở dáng gốc
            W = sk.the_gioi(P)
            c = (W[b] @ np.linalg.solve(sk.W0[b], np.array([c0[0], c0[1], 1.0])))[:2]
            u = t - t0
            g_ = 1500.0
            h0 = max(0.0, c[1] - (y_day + 22.0))              # độ cao tâm phiến trên đất (lúc này)
            t_cham = math.sqrt(2 * h0 / g_) if h0 > 0 else 0.0
            if u < t_cham:
                dy = -0.5 * g_ * u * u
            else:
                v = u - t_cham
                dy = -h0 + max(0.0, 90.0 * v - 0.5 * g_ * v * v)
            dx = (-70.0, -40.0, -95.0, -55.0)[j] * min(u, t_cham + 0.12)
            quay = (-38.0, 30.0, -46.0, 24.0)[j] * min(1.0, u / max(0.15, t_cham))
            xoay_quanh(P, b, c, quay)
            Wp = sk.the_gioi(P)[sk.bones[sk.bi[b]]["parent"]]
            dl = np.linalg.solve(Wp[:2, :2], np.array([dx, dy]))
            P.move(b, float(dl[0]), float(dl[1]))
        dam(P, float(np.clip(1.0 - (t - D_DIE) / (TAN - 0.1), 0.0, 1.0)))

    ev_cast = [(round(T_PHONG[k], 4), "phong", k) for k in PHIEN] + [(round(T_PHONG["3"] + BAY + 0.012, 3), "trung", "")] + \
              [(round(T_PHONG[k] + BAY + GIU + VE, 3), "ve", k) for k in PHIEN]
    ev_skill = [(0.08, "tu", ""), (T_DAM, "dam", ""), (T_TRUNG_SKILL, "trung", ""), (T_HET, "het", "")]
    ev_cast = [(0.12, "xoe", "")] + ev_cast
    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=[(T_TROI, "troi", ""), (T_BAM, "bam", ""), (T_LEN, "ru_cat", "")]),
        Clip("idle", CD["idle_01"][0], f_idle, loop=True, ev=[(T_LIEM0 + 0.3, "liem", "")]),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", 1.0, f_attack, ev=[(0.42, "lao", ""), (T_DOP, "trung", "")], trung=T_DOP),
        Clip("cast", D_CAST, f_cast, ev=ev_cast, trung=T_PHONG["3"] + BAY + 0.012),
        Clip("skill", D_SKILL, f_skill, ev=ev_skill, trung=T_TRUNG_SKILL),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", D_DIE + TAN, f_die, ev=[(0.70, "roi", "")]),
    ]
    return clips, than_cast


VONG_DI = {"3": 90.0, "2": 60.0, "1": 40.0}
VONG_VE = {"3": 220.0, "2": 170.0, "1": 120.0}
REF = {}


def them_phien_bay(sk, info, than_cast, cao):
    """xương far + fly_<k> (tâm phiến lúc rời) + bay_<k> (dáng phiến lúc rời) và slot bản sao (ẩn, vẽ trước hết) cho ba phiến bay."""
    sk.xuong("far", "root", 0.9 * cao + 140.0, 0.45 * cao)
    for k, (s, h, rb) in PHIEN.items():
        P = khung.Pose()
        than_cast(T_PHONG[k], P)
        W = sk.the_gioi(P)
        att = sk.atts[s][h]
        V = np.array([sum(w * (W[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in att["verts"]])
        c = V.mean(0)
        sk.xuong(f"fly_{k}", "root", float(c[0]), float(c[1]))
        sk.xuong(f"bay_{k}", f"fly_{k}", float(c[0]), float(c[1]), goc=_goc(W[rb]), the_gioi=True)
        inv = np.linalg.inv(sk.W0[f"bay_{k}"])
        rows = [[(f"bay_{k}", *[float(q) for q in (inv @ np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
        sk.slot(f"bay_{k}", "move", h, an=True)
        sk.luoi_gan(f"bay_{k}", h, sk.luoi[(s, h)], trongso.cung(len(rows), "move"), the_gioi=V)
        sk.atts[f"bay_{k}"][h]["verts"] = rows
        REF[k] = (rb, W[rb].copy())


def main(a):
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips, than_cast = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0) - info["y_day"]
    them_phien_bay(sk, info, than_cast, cao)
    ve0 = soi.Ve(sk)
    clips, _ = lam_clip(sk, info, cao)
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
            for s, b in (("P_shenti", "bone4"), ("P_tou", "bone27"), ("P_qi01", "bone7"), ("P_qi03", "bone9"), ("ao4", "ao4"),
                         ("P_shoubi02", "bone12"), ("bay_3", "bay_3"), ("bay_1", "bay_1")):
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
        sc = float(a[3]) if len(a) > 3 else 0.6
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
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de="Thằn lằn áo choàng đất nung (than_lan_cat_1): tướng 2 đảo Thổ", dang=1, so_dang=1,
                  dung_yen=("cast", "skill"), far=("cast",), far_aim=("cast",), ma_goc=None, khop_idle=0.2, cao=cao, impact=IMPACT,
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.3, tran_mb=0.5, span=3.8)


# ---------------------------------------------------------------- bộ mảnh tạm bằng da gốc (chạy thử rig khi chưa có mảnh của mình)
GOC_NGUON = {"tay_xa": ["P_shoubi04", "P_shoubi01", "P_shouzhi02"], "chan_xa": ["P_jiao04", "P_jiao03", "P_jiaozhi02"],
             "duoi": ["P_weiba01"], "than": ["P_shenti"], "chan_gan": ["P_jiao02", "P_jiao01", "P_jiaozhi01"],
             "tay_gan": ["P_shoubi03", "P_shoubi02", "P_shouzhi01"], "ao3": ["P_qi03"], "ao2": ["P_qi02"], "ao1": ["P_qi01"],
             "ao4": ["P_qi04"], "ham": ["P_zhui"], "dau": ["P_tou"], "mat": ["P_yanjing01"]}


def goc():
    ra = os.path.join(G.BASE, "manh_goc")
    os.makedirs(ra, exist_ok=True)
    _, to_rig, to_px = tf()
    _, imgs, atts = G.nap("att_idle0.json")
    by0 = {a["slot"]: a for a in atts}
    DATJ = {}

    def ve_nhieu(ds, ten_, doi_region=None):
        lay = Image.new("RGBa", (W_C, H_C), (0, 0, 0, 0))
        for a in ds:
            aa = dict(a)
            if doi_region:
                aa["region"] = doi_region
            im = G.part_goc(aa)
            uv, tr = G.luoi(aa)
            l1 = Image.new("RGBa", (W_C, H_C), (0, 0, 0, 0))
            _tris(l1, im.convert("RGBa"), to_px(np.array(a["xy"], float).reshape(-1, 2)), uv, tr)
            lay = Image.alpha_composite(lay.convert("RGBA"), l1.convert("RGBA")).convert("RGBa")
        lay = lay.convert("RGBA")
        bb = lay.getbbox()
        lay.crop(bb).save(os.path.join(ra, ten_ + ".png"))
        DATJ[ten_] = dict(hop=[bb[0], bb[1], bb[2], bb[3]], nguon="da gốc")

    for ten_, ss in GOC_NGUON.items():
        ve_nhieu([by0[s] for s in ss], ten_)
    ve_nhieu([by0["P_yanjing01"]], "mat_nham", doi_region="P_yanjing02")
    # lưỡi: vẽ ở dáng gốc (att_goc) trong khung concept
    D = json.load(open(os.path.join(G.scan(), "att_goc.json"), encoding="utf-8"))
    a_l = [a for a in D["atts"] if a["slot"] == "P_shetou"][0]
    G.nap("att_goc.json")
    ve_nhieu([a_l], "luoi")
    json.dump(DATJ, open(os.path.join(ra, "dat.json"), "w"), indent=1)
    print(ra, sorted(DATJ))


if __name__ == "__main__":
    if sys.argv[1:2] == ["goc"]:
        goc()
    else:
        main(sys.argv[1:])
