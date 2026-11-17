# -*- coding: utf-8 -*-
"""Quái bùn (quai_bun; tướng 8 đảo Thổ, ải 50, suất ho_kim_cuong): hình của mình chạy trên ĐÚNG rig của con gốc monster_3668 (quái nhầy
gù tay co giãn, game tham khảo). Ghi chú: inbox/quai_bun_ghichu.md. Mảnh: quai_bun_manh.py → inbox/quai_bun_1/manh/.

- XƯƠNG: đủ xương của họ (2 IK, 1 transform, 5 path đã được runtime nướng vào `l` của mẫu khung sample_goc.json), thêm `move` (cha của
  `all`), `far` (đích đòn ở xa, game dời tới đối thủ), `nam_ngam` (con của far: nắm đấm bùn khổng lồ trồi dưới chân đối thủ ở cast),
  `mieng` (lòng miệng thường, con của bone6), `mieng_to` (lòng hàm khổng lồ skill_04, con của bone63).
  TAY CO GIÃN: tám xương path `all2..all2h` của họ (cha gốc all3) treo dưới tám xương `fly_tay0..7` (con của root); hai xương nắm đấm
  `all2h2/all2h3` (inherit NoScale ở rig họ) treo dưới `fly_tay7`. Mỗi khung biến đổi riêng của chúng tính từ ma trận THẾ GIỚI mẫu khung
  (đúng tuyệt đối, kể cả NoScale). Ở attack, `fly_tay_k` đặt ở w_k · far với w_k = phần quãng của xương k từ vai tới far: game
  (AolaActor.FarAtomik) dời mỗi fly theo đúng w_k × (đối thủ thật − far) → cả cánh tay giãn đều, nắm đấm tới đúng đối thủ.
- MẢNH: (a) mảnh concept (than, vai_gan, tay_gan, tay_xa_tren, tay_xa_duoi, dau, ham, long_mieng, mat) là lưới phủ hình, mỗi đỉnh biến dạng
  như điểm tương ứng trên HỢP lưới các part của họ ở idle 0 (trong_so_goc) + làm mịn; (b) mảnh theo khung part (lòng bàn tay + 16 đốt ngón,
  9 xúc tu, tay co giãn, hàm khổng lồ) dùng NGUYÊN lưới, uv, trọng số của họ (gan_nguyen).
- HIỆN / ẨN: mỗi slot của mình theo một slot "lái" của họ (trường `n` của mẫu khung): skill_02_* tắt tay xa thường, bật tay co giãn;
  skill_04 tắt đầu thường, bật hàm khổng lồ. skill_02_1 đổi thứ tự vẽ (cẳng + nắm tay xa ra SAU thân lúc giơ tay): bản sao `@sau`.
- CLIP: appear = appear_01 (cột bùn vọt lên rồi bập xuống thành hình) + gầm (dáng show_01); idle = idle_01 (2 chu kỳ nền 1,33 s) + chớp
  mắt + bong bóng bùn; walk = run_01; attack = skill_02_1 (vươn tay bùn tới đối thủ); cast = skill_03 (đấm cắm tay xuống đất, nắm đấm khổng
  lồ trồi dưới chân đối thủ); skill = skill_04 (đầu phình thành hàm khổng lồ, phun bùn đá: VFX); hit = hit_01; die = die_01 + chảy tan.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/quai_bun_rig.py     → inbox/quai_bun_1/rig/
    py -3 -I ArtGen/Spine/quai_bun_rig.py soi <clip> <giây,...|n=12|t0:t1:n> [tỉ lệ]       → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/quai_bun_rig.py kiem                                           đo góc nhảy, bước dời
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
from hoa_ho_rig import tmap, _goc, ease  # noqa: E402
import quai_bun  # noqa: E402,F401
import tho5  # noqa: E402

G = tho5.dat("quai_bun")                                     # đặt trạng thái hoa_ho về con 3668 SAU mọi import
TEN_RIG = "quai_bun"
TIEU_DE = "Bùn Ngoạm (quai_bun): tướng 8 đảo Thổ, ải 50, dạng 2"
D_PX = float(os.environ.get("QB_DPX", "0.39"))               # pixel ảnh atlas cho mỗi đơn vị rig
MANH = os.path.join(G.BASE, "manh")
PART = os.path.join(MANH, "part_can") if os.path.isdir(os.path.join(MANH, "part_can")) else os.path.join(MANH, "part")
RA = os.environ.get("QB_RA") or os.path.join(G.BASE, "rig")
# DẠNG 1 "Bùn Ngoạm Nhi" (QB_DANG=non; người dùng 2026-11-17: "làm dạng 1", chọn cùng rig 3668, concept A): cùng xương / lưới / clip, nhân tỉ lệ
# xương sau khi dựng (inbox/quai_bun_non/mau/ti_le.json), mảnh lấy ở inbox/quai_bun_non/manh (đầu, hàm dưới, mắt, quả bóng mới; còn lại chép
# nguyên của dạng 2); ảnh part theo khung gốc (PART) dùng chung với dạng 2. Ghi chú inbox/quai_bun_non_ghichu.md.
NON = os.environ.get("QB_DANG", "") == "non"
H_CAT_NON = 100.0                # dạng non: hạ mặt nạ đất ở appear / skill / die (hàm to thụt sâu hơn)
K_TAY_CO = 0.68                  # dạng non: tay co giãn (chuỗi fly) mảnh lại / nhỏ lại như tay xa (bone2 0,8 × bone19 0,85)
K_BONG, K_CUC, K_NAM = (0.80, 0.82, 0.70) if NON else (1.0, 1.0, 1.0)   # quả bóng, cục đất appear, nắm đấm khổng lồ
if NON:
    TEN_RIG = "quai_bun_non"
    TIEU_DE = "Bùn Ngoạm Nhi (quai_bun_non): tướng 8 đảo Thổ, ải 50, dạng 1"
    MANH = os.path.join(HERE, "inbox", "quai_bun_non", "manh")
    RA = os.environ.get("QB_RA") or os.path.join(HERE, "inbox", "quai_bun_non", "rig")
    TI_NON = json.load(open(os.path.join(HERE, "inbox", "quai_bun_non", "mau", "ti_le.json")))
TAN = 0.5
Y_CAT = 110.0
Y_HOA = (700.0, 890.0)          # px concept: thân bám vũng bùn 0 % ở y0, 100 % ở y1
FPS = 30.0
W_C, H_C = 1536, 1024
IMPACT = {"attack": (0.07, 0.40, 0.10), "cast": (0.10, 0.60, 0.14), "skill": (0.14, 0.85, 0.18, "#ffe6b040")}

CHAIN = ["all2", "all2b", "all2c", "all2d", "all2e", "all2f", "all2g", "all2h"]
NAM = ["all2h2", "all2h3"]                                    # hai xương nắm đấm tay co giãn (NoScale ở rig họ)
REPARENT = {b: f"fly_tay{k}" for k, b in enumerate(CHAIN)}
REPARENT.update({b: "fly_tay7" for b in NAM})
NGON_L = [f"P_shouL3_{k}" for k in range(8, 0, -1)]
NGON_R = [f"P_shouR3_{k}" for k in range(8, 0, -1)]
HAM_TO = ["P_tou_1_06", "P_tou_1_05", "P_tou_1_04", "P_tou_1_03", "P_tou_1_02", "P_tou_1_01", "P_yanjing_2", "P_yanjing_1"]

# slot của mình (thứ tự vẽ, sau → trước): (tên slot, kiểu, nguồn, slot lái của họ)
#   kiểu "goc": nguyên lưới của họ (mọi hình của slot nguồn trong att_goc); "cc": mảnh concept bám hợp lưới các slot nguồn (idle 0);
#   "cung": mảnh cứng một xương; "cat": mặt nạ đất cho tay co giãn
N_GAI = 22                       # số gai chiêu cuối (người dùng 2026-11-17: "cho nhiều gai hơn")
SLOT = ([("cat_dat", "cat", None, None)]
        + [(s, "goc", s, s) for s in ("G_shoudabi", "G_shoubi", "G_shouzhang")]
        + [("P_shouL1_1", "goc", "P_shouL1_1", "P_shouL1_1"),
           ("tay_xa_tren", "cc", ["P_shouL1"], "P_shouL1"),
           ("tay_xa_duoi@sau", "cc", ["P_shouL2"], "P_shouL2"),
           ("P_shouL3@sau", "goc", "P_shouL3", "P_shouL3")]
        + [(s + "@sau", "goc", s, s) for s in NGON_L]
        + [("P_shenti2_4", "goc", "P_shenti2_4", "P_shenti2_4"), ("P_shenti2_3", "goc", "P_shenti2_3", "P_shenti2_3"),
           ("than", "cc", ["P_shenti2"], "P_shenti2", "than"),
           ("P_shenti2_2", "goc", "P_shenti2_2", "P_shenti2_2"), ("P_shenti2_1", "goc", "P_shenti2_1", "P_shenti2_1"),
           ("tay_xa_duoi", "cc", ["P_shouL2"], "P_shouL2"),
           ("long_mieng", "cc", ["P_tou_2_07", "P_tou_2_04"], "P_tou_2_07"),
           ("ham", "cc", ["P_tou_2_05"], "P_tou_2_05"),
           ("dau", "cc", ["P_tou_2_02", "P_tou_2_03", "P_tou_2_01", "P_tou_2_06"], "P_tou_2_02"),
           ("mat", "cung", "bone6", "P_yanjing_6"),
           ("P_shouL3", "goc", "P_shouL3", "P_shouL3")]
        + [(s, "goc", s, s) for s in NGON_L]
        + [("P_shouR1_1", "goc", "P_shouR1_1", "P_shouR1_1"), ("P_shouR1_2", "goc", "P_shouR1_2", "P_shouR1_2"),
           ("vai_gan", "cc", ["P_shouR1"], "P_shouR1"),
           ("P_shouR2_2", "goc", "P_shouR2_2", "P_shouR2_2"), ("P_shouR2_1", "goc", "P_shouR2_1", "P_shouR2_1"),
           ("tay_gan", "cc", ["P_shouR2"], "P_shouR2"),
           ("P_shouR3", "goc", "P_shouR3", "P_shouR3")]
        + [(s, "goc", s, s) for s in NGON_R]
        + [(s, "goc", s, s) for s in HAM_TO]
        + [(f"gai{k}", "gai", k, None) for k in range(N_GAI)]
        + [("bong_mat", "bong", "bong_mat", None), ("bong_dat", "bong", "bong_dat", None)]
        + [("nam_ngam", "cung", "nam_ngam", None)])
# chiêu cuối (người dùng 2026-11-17): nuốt đối thủ, phồng thành QUẢ BÓNG mặt căng, gai đất đâm xuyên thân; appear: cục đất tròn rơi, nảy, bung
U_B = 1.6                        # đơn vị rig cho mỗi px tờ M_B1 (quả bóng, cục đất, gai: cùng tỉ lệ nét)
BONG_PX = (336.0, 564.0, 298.0)  # tâm + bán kính quả bóng mặt căng trên tờ M_B1 (px)
CUC_PX = (851.0, 558.0, 185.0)   # tâm + bán kính cục đất trơn
GAI_GOC_PX = {0: (1088.0, 346.0), 1: (1101.0, 541.0), 2: (1101.0, 725.0)}   # gốc (giữa đáy) từng gai trên tờ
# gai: (góc độ, kiểu ảnh gai 0/1/2, độ dài), theo thứ tự đâm ra. Đợt 1: mười gai dài đâm từng chiếc (cả bóng giật theo); đợt 2: mười hai gai
# ngắn hơn xen giữa đâm dồn dập → chi chít
GAI1 = [(70, 0), (8, 1), (132, 0), (100, 2), (38, 0), (165, 1), (-18, 2), (55, 1), (150, 0), (118, 2)]
GAI2 = [(-32, 2), (22, 1), (141, 2), (85, 1), (178, 0), (47, 2), (109, 1), (-4, 0), (158, 2), (62, 1), (194, 2), (125, 1)]
GAI = ([(g, k, 1.0) for g, k in GAI1]
       + [(g, k, L) for (g, k), L in zip(GAI2, (0.80, 0.86, 0.76, 0.95, 0.70, 0.82, 0.90, 0.72, 0.86, 0.80, 0.72, 0.92))])
assert len(GAI) == N_GAI
GAI_TRONG = 0.35                 # gốc gai nằm trong bóng ở 0,35 bán kính
TU_THAN = []                     # slot của thân tướng (mọi slot trừ bóng, gai, mặt nạ, nắm đấm khổng lồ): điền trong dung()
SAU = {"tay_xa_duoi@sau", "P_shouL3@sau"} | {s + "@sau" for s in NGON_L}
TRUOC = set()
MUOT = {"than": 20, "vung_bun": 12, "than_lot": 8, "vai_gan": 8, "tay_gan": 8, "tay_xa_tren": 8, "tay_xa_duoi": 8, "ham": 6, "long_mieng": 6, "dau": 4}


# ---------------------------------------------------------------- nạp
def nap():
    scan = G.scan()
    D = json.load(open(os.path.join(scan, "att_goc.json"), encoding="utf-8"))
    D0 = json.load(open(os.path.join(scan, "att_idle0.json"), encoding="utf-8"))
    DH = json.load(open(os.path.join(scan, "att_ham.json"), encoding="utf-8"))
    I = json.load(open(os.path.join(scan, "info.json"), encoding="utf-8"))
    S = json.load(open(os.path.join(scan, "sample_goc.json"), encoding="utf-8"))
    return D, D0, DH, I, S


def mats(Dj):
    return {b["name"]: np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]]) for b in Dj["bones"]}


def tf():
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    to_rig = lambda P: np.stack([cx + (P[:, 0] - W_C / 2) / s, cy - (P[:, 1] - H_C / 2) / s], 1)  # noqa: E731
    to_px = lambda V: np.stack([W_C / 2 + (V[:, 0] - cx) * s, H_C / 2 - (V[:, 1] - cy) * s], 1)  # noqa: E731
    return s, to_rig, to_px


def thu(g, k):
    return anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * k)), max(2, round(g.height * k))), Image.LANCZOS).convert("RGBA"))


# ---------------------------------------------------------------- gắn mảnh concept (như rong_cat_non_rig)
def hop_luoi(a0s, ten):
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
    """mỗi điểm V (thế giới idle 0) biến dạng như điểm tương ứng trên HỢP lưới a0s (toạ độ trọng tâm; ngoài lưới: điểm gần nhất trên cạnh +
    khoảng lệch). Lưới đứng SAU trong a0s thắng chỗ chồng (vũng bùn đè lên thân). Trả hàng (xương, x, y, w) theo ma trận Wi."""
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


def lam_muot(rows, V, tris, Wi, vong):
    """làm mịn trọng số trên lưới của mình `vong` lần (giữ 50 % của chính nó), ≤ 4 xương, gắn kiểu LBS."""
    n = len(rows)
    ke = [set() for _ in range(n)]
    for a, b, c in np.asarray(tris).reshape(-1, 3):
        ke[a] |= {b, c}
        ke[b] |= {a, c}
        ke[c] |= {a, b}
    w = [{} for _ in range(n)]
    for i, r in enumerate(rows):
        for bn, _, _, ww in r:
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


HOA_Y = {}          # mảnh: (tên mảnh nguồn đã gắn, y px concept bám 0 % nguồn, y px bám 100 %)
CC_FINAL = {}       # mảnh concept đã gắn: (V thế giới idle 0, tam giác, hàng trọng số)


def ts_noi_suy(V, Vs, tris, rows):
    """trọng số {xương: w} tại mỗi điểm V nội suy trọng tâm trên lưới (Vs, tris, rows) của một mảnh đã gắn; ngoài lưới: đỉnh gần nhất."""
    A, B_, C = Vs[tris[:, 0]], Vs[tris[:, 1]], Vs[tris[:, 2]]
    v0, v1 = B_ - A, C - A
    den = v0[:, 0] * v1[:, 1] - v0[:, 1] * v1[:, 0]
    den = np.where(np.abs(den) < 1e-9, 1e-9, den)
    W = [{bn: ww for bn, _, _, ww in r} for r in rows]
    out = []
    for p in V:
        v2 = p - A
        b1 = (v2[:, 0] * v1[:, 1] - v2[:, 1] * v1[:, 0]) / den
        b2 = (v0[:, 0] * v2[:, 1] - v0[:, 1] * v2[:, 0]) / den
        b0 = 1 - b1 - b2
        ok = np.flatnonzero((b0 >= -1e-4) & (b1 >= -1e-4) & (b2 >= -1e-4))
        if len(ok):
            i = int(ok[0])
            acc = {}
            for vi, bw in zip(tris[i], (b0[i], b1[i], b2[i])):
                for bn, ww in W[vi].items():
                    acc[bn] = acc.get(bn, 0.0) + float(bw) * ww
        else:
            acc = dict(W[int(np.argmin(np.hypot(*(Vs - p).T)))])
        tot = sum(acc.values()) or 1.0
        out.append({k: v / tot for k, v in acc.items()})
    return out


def gan_concept(sk, slot, ten_anh, a0s, ten, Wi, mot_xuong=None):
    DATJ = json.load(open(os.path.join(MANH, "dat.json"), encoding="utf-8"))
    s_px, to_rig, _ = tf()
    kq = D_PX / s_px
    if ten_anh not in sk.images:
        sk.anh(ten_anh, thu(Image.open(os.path.join(MANH, ten_anh + ".png")).convert("RGBA"), kq))
    im = sk.images[ten_anh]
    x0, y0 = DATJ[ten_anh]["hop"][:2]
    if mot_xuong is None:
        L = luoi.luoi_vung(im, buoc_vien=8.0, buoc_trong=13.0, vien=2, ten=f"{slot}/{ten_anh}", in_tk=False)
    else:
        L = luoi.luoi_o(im.width, im.height, 2, 2, ten=slot)
    PX = np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1)
    V = to_rig(PX)
    base = slot.split("@")[0]
    if mot_xuong is None:
        rows = trong_so_goc(V, a0s, ten, Wi)
        if MUOT.get(base, 0) > 0:
            rows = lam_muot(rows, V, L.tris, Wi, MUOT[base])
        if base in HOA_Y:
            # dải trên của mảnh lấy ĐÚNG trọng số cuối của một mảnh khác đã gắn (vũng bùn: sát mép trên theo thân `than`, nội suy trên
            # lưới của nó) rồi hoà sang trọng số của chính mảnh này: hai mảnh chồng ở chỗ nối biến dạng như nhau, không hở
            nguon2, y0_, y1_ = HOA_Y[base][:3]               # bám nguồn 0 % ở y0_, 100 % ở y1_ (px concept)
            if isinstance(nguon2, str):                      # mảnh đã gắn: nội suy trên lưới cuối của nó
                w2 = ts_noi_suy(V, *CC_FINAL[nguon2])
            else:                                            # hợp lưới gốc: trọng số đã làm mịn cùng số vòng
                r2 = lam_muot(trong_so_goc(V, nguon2, ten, Wi), V, L.tris, Wi, MUOT.get(base, 0))
                w2 = [{bn: ww for bn, _, _, ww in r} for r in r2]
            f = np.clip((PX[:, 1] - y0_) / (y1_ - y0_), 0, 1)
            f = f * f * (3 - 2 * f)
            if len(HOA_Y[base]) > 3:                         # chỉ phía phải x0 → x1 (px concept)
                xa_, xb_ = HOA_Y[base][3]
                g = np.clip((PX[:, 0] - xa_) / (xb_ - xa_), 0, 1)
                f = f * g * g * (3 - 2 * g)
            moi = []
            for i in range(len(rows)):
                w = {}
                for bn, _, _, ww in rows[i]:
                    w[bn] = w.get(bn, 0.0) + (1 - f[i]) * ww
                for bn, ww in w2[i].items():
                    w[bn] = w.get(bn, 0.0) + f[i] * ww
                hang = []
                for bn, ww in w.items():
                    if ww < 1e-4:
                        continue
                    lp = np.linalg.solve(Wi[bn], np.array([V[i, 0], V[i, 1], 1.0]))
                    hang.append((bn, float(lp[0]), float(lp[1]), ww))
                t2 = sum(q[3] for q in hang) or 1.0
                moi.append([(a_, b_, c_, d_ / t2) for a_, b_, c_, d_ in hang])
            rows = moi
        CC_FINAL[base] = (V, np.asarray(L.tris), rows)
    else:
        b, Mb = mot_xuong
        rows = [[(b, *[float(v) for v in np.linalg.solve(Mb, np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
    Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
    sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=Vs)
    sk.atts[slot][ten_anh]["verts"] = rows
    return L


def mat_do(att, im):
    """px ảnh của mình cho mỗi đơn vị rig của một lưới gốc (diện tích uv × ảnh / diện tích thế giới)."""
    uv = np.array(att["uv"], float).reshape(-1, 2) * np.array([im.width, im.height])
    V = np.array(att["xy"], float).reshape(-1, 2)
    tr = np.array(att["tris"]).reshape(-1, 3)

    def dt(P):
        a, b, c = P[tr[:, 0]], P[tr[:, 1]], P[tr[:, 2]]
        return np.abs((b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0])).sum() / 2
    return math.sqrt(dt(uv) / max(dt(V), 1e-6))


def gan_nguyen(sk, slot, att, ten, Wc):
    """nguyên lưới của họ (đỉnh, tam giác, uv, trọng số) với ảnh của mình (part/<vùng>.png, cùng khung ảnh vùng × RES)."""
    reg = att["region"]
    an = "p_" + reg
    if an not in sk.images:
        g = Image.open(os.path.join(PART, reg + ".png")).convert("RGBA")
        if reg in ("P_yanjing_1", "G_shoudabi"):         # lòng khung mắt / khe thủng của bắp tay: GPT tô trắng, của họ là trong suốt
            import cv2
            a = np.asarray(g).copy()
            trang = a[..., :3].min(2) > 205
            if reg == "G_shoudabi":                      # cả viền mực quanh khe (nới 4 px) cũng bỏ
                trang = cv2.dilate(trang.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool) & (a[..., 3] > 0)
            a[..., 3] = np.where(trang, 0, a[..., 3])
            g = Image.fromarray(a, "RGBA")
        k = D_PX / mat_do(att, g)
        sk.anh(an, thu(g, min(1.0, k)))
    im = sk.images[an]
    L = luoi.Luoi(np.array(att["uv"], float).reshape(-1, 2) * np.array([im.width, im.height]), np.array(att["tris"]).reshape(-1, 3),
                  att["hull"], att["hull"], im.width, im.height, ten=slot)
    V = np.array(att["xy"], float).reshape(-1, 2)
    hinh = att.get("name") or reg
    sk.luoi_gan(slot, an, L, trongso.cung(L.n, "move"), the_gioi=V, ten=hinh)
    rows = []
    for p, ws in zip(V, att["w"]):
        row = [(ten[k], *[float(v) for v in (np.linalg.inv(Wc[ten[k]]) @ np.array([p[0], p[1], 1.0]))[:2]], float(w)) for k, w in ws if w > 0.002]
        tot = sum(r[3] for r in row) or 1.0
        rows.append([(n, x, y, w / tot) for n, x, y, w in row])
    sk.atts[slot][hinh]["verts"] = rows
    return L, hinh


# ---------------------------------------------------------------- dựng
FAR_T = ("skill_02_1", 0.60)          # dáng gốc của far = chỗ nắm đấm co giãn ở giây này (tay duỗi ngang hết cỡ)


def dung():
    D, D0, DH, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    Wc = mats(D)
    Wi = mats(D0)
    Wh = mats(DH)
    by0 = {a["slot"]: a for a in D0["atts"] if a.get("region")}
    goc_atts = {}
    for a in D["atts"]:
        if a.get("region"):
            goc_atts.setdefault(a["slot"], []).append(a)
    P_all = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in D0["atts"] if a.get("region") and a["slot"] != "shadow"])
    y_day = float(P_all[:, 1].min())
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("dat_cat", "move")                                 # xương của mặt nạ đất (appear nâng lên sát mặt đất)
    for k in range(len(CHAIN)):
        sk.xuong(f"fly_tay{k}", "root")
    goc0 = {}
    for b in IB:
        if b["name"] in ("root", "shadow"):
            continue
        g = [b["x"], b["y"], b["rot"], b["sx"], b["sy"]]
        goc0[b["name"]] = g
        cha = ten[b["parent"]]
        if b["name"] in REPARENT:                           # biến đổi riêng = ma trận thế giới dáng gốc (cha là fly ở gốc toạ độ)
            M = Wc[b["name"]]
            gx = math.degrees(math.atan2(M[1, 0], M[0, 0]))
            sx = math.hypot(M[0, 0], M[1, 0])
            sy = (M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]) / sx
            goc0[b["name"]] = [M[0, 2], M[1, 2], gx, sx, sy]
            sk.xuong(b["name"], REPARENT[b["name"]], M[0, 2], M[1, 2], goc=gx, dai=b["len"], sx=sx, sy=sy)
        elif cha == "root":
            sk.xuong(b["name"], "move", g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
        else:
            sk.xuong(b["name"], cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
    # far: chỗ nắm đấm co giãn lúc duỗi ngang hết cỡ (mẫu khung skill_02_1 @ 0,60)
    fr = S[FAR_T[0]]["frames"][int(round(FAR_T[1] * FPS))]
    fx, fy = fr["b"][ten.index("all2h3")][:2]
    vai = fr["b"][ten.index("all2")][:2]
    sk.xuong("far", "root", float(fx), float(fy))
    sk.xuong("nam_ngam", "far", 0.0, float(y_day - fy))
    # quả bóng: tâm ở giữa thân (x của bụng), đáy chạm đất; sáu xương phồng quanh tâm; mười xương gai từ tâm chĩa ra
    _, to_rig0, _ = tf()
    xb = float(to_rig0(np.array([[880.0, 600.0]]))[0, 0])
    rb = BONG_PX[2] * U_B
    sk.xuong("bong", "move", xb, float(y_day + rb))
    for j in range(6):
        a = math.radians(60 * j)
        sk.xuong(f"bong_r{j}", "bong", 0.62 * rb * math.cos(a), 0.62 * rb * math.sin(a), goc=60.0 * j)
    for k, e_g in enumerate(GAI):
        sk.xuong(f"gai{k}", "bong", 0.0, 0.0, goc=float(e_g[0]))
    rc = CUC_PX[2] * U_B
    sk.xuong("cuc", "move", xb, float(y_day + rc))
    sk.W0 = sk.the_gioi()

    def them(ten_x, cha, p_rig, Wm, rot_tg=0.0):
        sk.xuong(ten_x, cha, 0.0, 0.0)
        Ml = np.linalg.solve(Wm[cha], np.array([p_rig[0], p_rig[1], 1.0]))
        bx = sk.bones[sk.bi[ten_x]]
        bx["x"], bx["y"] = float(Ml[0]), float(Ml[1])
        bx["rot"] = -_goc(Wm[cha]) + rot_tg

    # lòng miệng thường (giữa mảnh long_mieng, idle 0) và lòng hàm khổng lồ (giữa P_tou_1_06 ở skill_04 @ 1,1)
    DATJ = json.load(open(os.path.join(MANH, "dat.json"), encoding="utf-8"))
    s_px, to_rig, _ = tf()
    x0, y0, x1, y1 = DATJ["long_mieng"]["hop"]
    them("mieng", "bone6", to_rig(np.array([[(x0 + x1) / 2, (y0 + y1) / 2]]))[0], Wi)
    a06 = next(a for a in DH["atts"] if a["slot"] == "P_tou_1_06")
    them("mieng_to", "bone63", np.array(a06["xy"], float).reshape(-1, 2).mean(0), Wh)
    sk.W0 = sk.the_gioi()
    Wb = dict(Wi)
    for x in ("far", "nam_ngam"):
        Wb[x] = sk.W0[x]
    # dải trên vũng bùn đi theo thân (nối liền khi thân nhấc lên) chỉ ở phía PHẢI góc lõm (x > 640 px); phía trái (lưỡi vũng bùn, hai viên
    # sỏi) đứng yên theo xương vũng bùn: kéo cả phía trái theo thân thì sỏi bị nghiền ở skill_04 (thử 2026-11-17)
    # thân MỘT mảnh liền, hoà theo CHIỀU CAO: trên theo thân P_shenti2, dưới theo các xương vũng bùn (P_shenti1_1..3) + cột thân P_shenti1;
    # không có ranh trái – phải (ranh đó gập răng cưa khi thân phình đè cột ở skill_04). Bản ba lớp (than_lot / than_sau / vung_bun) bỏ:
    # vẫn hở góc lõm ở vài dáng (người dùng chụp skill 2026-11-17: "phần dưới thân này bị rách lỗi rồi")
    HOA_Y["than"] = ([by0[x] for x in ("P_shenti1", "P_shenti1_3", "P_shenti1_2", "P_shenti1_1")], Y_HOA[0], Y_HOA[1])
    tong = [0, 0]
    hinh_cua = {}
    for e_ in SLOT:
        s, kieu, nguon = e_[:3]
        anh_ten = e_[4] if len(e_) > 4 else s.split("@")[0]
        if kieu == "cat":
            sk.slot(s, "dat_cat")
            continue
        if kieu == "goc":
            atts = goc_atts[nguon]
            sk.slot(s, "move", None)
            hs = []
            for a in atts:
                L, h = gan_nguyen(sk, s, a, ten, Wc)
                hs.append(h)
                tong[0] += L.n
                tong[1] += len(L.tris)
            mac = next((a.get("name") or a["region"] for a in atts if a.get("cur")), None)
            sk._slot(s)["att"] = mac
            hinh_cua[s] = hs
        elif kieu == "cc":
            sk.slot(s, "move", anh_ten)
            L = gan_concept(sk, s, anh_ten, [by0[x] for x in nguon], ten, Wi)
            tong[0] += L.n
            tong[1] += len(L.tris)
        elif s == "mat":
            sk.slot(s, "move", "mat")
            for h in ("mat", "mat_nham"):
                L = gan_concept(sk, s, h, None, ten, Wi, mot_xuong=("bone6", Wi["bone6"]))
        elif kieu == "gai":
            g_, kieu_anh = GAI[nguon][:2]
            an = f"gai_{kieu_anh}"
            if an not in sk.images:
                sk.anh(an, thu(Image.open(os.path.join(MANH, an + ".png")).convert("RGBA"), D_PX * U_B))
            sk.slot(s, f"gai{nguon}", None)
            hop = json.load(open(os.path.join(MANH, "dat.json"), encoding="utf-8"))[an]["hop"]
            gx, gy = GAI_GOC_PX[kieu_anh]
            neo = ((gx - hop[0]) / (hop[2] - hop[0]), (gy - hop[1]) / (hop[3] - hop[1]))
            cbx, cby = sk.W0["bong"][:2, 2]
            a = math.radians(g_)
            r0 = GAI_TRONG * BONG_PX[2] * U_B
            sk.manh(s, an, khung.Dat(cbx + r0 * math.cos(a), cby + r0 * math.sin(a), goc=float(g_), ti=1.0 / D_PX, neo=neo))
        elif kieu == "bong":
            hop = json.load(open(os.path.join(MANH, "dat.json"), encoding="utf-8"))[nguon]["hop"]
            cx_, cy_, r_ = BONG_PX if nguon == "bong_mat" else CUC_PX
            if nguon not in sk.images:
                sk.anh(nguon, thu(Image.open(os.path.join(MANH, nguon + ".png")).convert("RGBA"), D_PX * U_B))
            im = sk.images[nguon]
            xuong_ = "bong" if nguon == "bong_mat" else "cuc"
            cbx, cby = sk.W0[xuong_][:2, 2]
            sk.slot(s, xuong_, None)
            if nguon == "bong_dat":
                neo = ((cx_ - hop[0]) / (hop[2] - hop[0]), (cy_ - hop[1]) / (hop[3] - hop[1]))
                sk.manh(s, nguon, khung.Dat(cbx, cby, ti=1.0 / D_PX, neo=neo))
            else:
                # lưới phủ bóng: đỉnh bám tâm + hai xương phồng gần nhất theo góc (càng ra rìa càng theo xương phồng)
                L = luoi.luoi_vung(im, buoc_vien=8.0, buoc_trong=13.0, vien=2, ten=s, in_tk=False)
                kq = D_PX * U_B
                PXs = np.stack([hop[0] + L.pts[:, 0] / kq, hop[1] + L.pts[:, 1] / kq], 1)
                Vb = np.stack([cbx + (PXs[:, 0] - cx_) * U_B, cby - (PXs[:, 1] - cy_) * U_B], 1)
                ts = []
                for v in Vb:
                    d = v - np.array([cbx, cby])
                    r = float(np.hypot(*d)) / (r_ * U_B)
                    ph = math.degrees(math.atan2(d[1], d[0])) % 360.0
                    j0 = int(ph // 60) % 6
                    fr = (ph - 60 * (ph // 60)) / 60.0
                    wr = 0.9 * float(np.clip((r - 0.25) / 0.75, 0, 1)) ** 1.5
                    w = {"bong": 1.0 - wr}
                    if wr > 1e-4:
                        w[f"bong_r{j0}"] = wr * (1 - fr)
                        k1 = f"bong_r{(j0 + 1) % 6}"
                        w[k1] = w.get(k1, 0.0) + wr * fr
                    ts.append({k_: v_ for k_, v_ in w.items() if v_ > 1e-5})
                sk.luoi_gan(s, nguon, L, ts, the_gioi=Vb)
        elif s == "nam_ngam":
            # nắm đấm khổng lồ: ảnh nắm đấm tay co giãn của mình, xoay cho nắm đấm chĩa lên trời, đáy ở xương nam_ngam (mặt đất dưới đối thủ)
            g0 = Image.open(os.path.join(PART, "G_shouzhang.png")).convert("RGBA")
            k = D_PX / mat_do(goc_atts["G_shouzhang"][0], g0)            # ảnh vùng của họ: đốt tay chĩa lên, cổ tay bùn ở dưới
            sk.anh("nam_to", thu(g0, k))
            sk.slot(s, "nam_ngam", None)
            nx, ny = sk.W0["nam_ngam"][:2, 2]
            sk.manh(s, "nam_to", khung.Dat(nx, ny, ti=3.0 / D_PX, neo=(0.5, 0.96)))
    # mặt nạ đất: tay co giãn (ba slot G_*) chỉ hiện phía trên mặt đất (cắm xuống đất ở cast)
    # MỘT mặt nạ đất phủ mọi slot (runtime .atomik: mặt nạ luôn bật, lồi): giấu phần dưới mặt đất (cột bùn chưa trồi ở appear, tay cắm
    # xuống đất ở cast); mép thấp hơn đáy vũng bùn idle Y_CAT đơn vị để giọt bùn, nắm đấm chạm đất không bị xén
    cuoi = sk.slots[-1]["name"]
    sk.cat("cat_dat", cuoi, [(-6000.0, y_day - Y_CAT), (9000.0, y_day - Y_CAT), (9000.0, 9000.0), (-6000.0, 9000.0)])
    TU_THAN[:] = [q["name"] for q in sk.slots if not (q["name"].startswith(("gai", "bong_", "cat_dat")) or q["name"] == "nam_ngam")]
    for e, m in (("lao", "skill: nhảy lao tới đối thủ"), ("ngoam", "skill: ngoạm trúng (game giấu đối thủ: đã bị nuốt)"),
                 ("ve", "skill: nhảy lùi về chỗ"), ("phong", "skill: phồng thành quả bóng (VFX phụt bùn)"),
                 ("giay", "skill: đối thủ quẫy trong bụng"), ("dam", "skill: gai đất đâm xuyên thân"), ("rut", "skill: gai rút"),
                 ("hien", "skill: thôi làm bóng, tướng hiện lại còn ngậm đối thủ (VFX phụt bùn)"), ("oe", "skill: ọe, sắp nhổ"),
                 ("nho", "skill: NHỔ đối thủ ra (game phóng đối thủ từ xương mieng_to bay về chỗ)"), ("roi", "appear: cục đất rơi"), ("nay", "appear: cục đất chạm đất nảy"),
                 ("bung", "appear: cục đất bung ra thành tướng (VFX toé đất)"),
                 ("trung", "khung trúng"), ("vuon", "attack: tay bùn phóng ra (VFX vệt bùn)"), ("cam", "cast: tay cắm xuống bùn (VFX toé bùn)"),
                 ("troi", "cast: nắm đấm khổng lồ trồi dưới chân đối thủ"), ("hut", "skill: hút đất đá vào miệng"),
                 ("ha", "skill: đầu phình thành hàm khổng lồ"), ("phun", "skill: phun dòng bùn đá"), ("khep", "skill: khép hàm"),
                 ("dap", "appear: bập xuống đất (VFX toé bùn)"), ("gam", "appear: gầm"), ("bong", "idle: bong bóng bùn vỡ trên lưng"),
                 ("chay", "die: chảy sụp thành vũng")):
        sk.su_kien(e, m)
    if NON:
        # dạng non: nhân tỉ lệ dáng gốc (xương con thừa hưởng; điểm gắn lưu theo hệ xương nên mảnh co / phình theo). Quả bóng, cục đất co quanh
        # tâm rồi hạ xuống cho đáy vẫn chạm đất; nắm đấm khổng lồ co quanh chân (xương nam_ngam ở mặt đất).
        ti = dict(TI_NON)
        ti["nam_ngam"] = K_NAM
        ti["bone10"] = ti["bone22"] = 0.78                 # hai bàn tay (cổ tay → ngón đá): nắm sỏi nhỏ như concept dạng 1
        for nm, k in ti.items():
            b = sk.bones[sk.bi[nm]]
            b["sx"] *= k
            b["sy"] *= k
        for nm, k, r_ in (("bong", K_BONG, BONG_PX[2] * U_B), ("cuc", K_CUC, CUC_PX[2] * U_B)):
            b = sk.bones[sk.bi[nm]]
            b["sx"] *= k
            b["sy"] *= k
            b["y"] -= (1.0 - k) * r_
        sk.W0 = sk.the_gioi()
        print("dạng non: tỉ lệ", ti, f"bóng {K_BONG}, cục đất {K_CUC}")
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; đáy y = {y_day:.1f}; far ({fx:.0f}, {fy:.0f}); "
          f"vai tay co giãn ({vai[0]:.0f}, {vai[1]:.0f})")
    return sk, dict(IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], y_day=y_day, S=S, far=(float(fx), float(fy)),
                    y_all=float(sk.W0["all"][1, 2]),
                    hinh_cua=hinh_cua)


# ---------------------------------------------------------------- chuyển động của họ
def chuyen_dong(info):
    S, ten, goc0 = info["S"], info["ten"], info["goc0"]
    sl_ho = info["slots"]
    out = {}
    for clip, v in S.items():
        fr = v["frames"]
        L = np.array([F["l"] for F in fr], float)
        Bw = np.array([F["b"] for F in fr], float)
        res = {}
        for i, n in enumerate(ten):
            if n not in goc0:
                continue
            g = goc0[n]
            if n in REPARENT:
                X = Bw[:, i, :]                              # thế giới: x, y, góc, sx, sy (fly ở gốc toạ độ; dời thêm lúc dựng clip)
            else:
                X = L[:, i, :5]
            A = np.stack([X[:, 2] - g[2], X[:, 0] - g[0], X[:, 1] - g[1], X[:, 3] / (g[3] or 1.0), X[:, 4] / (g[4] or 1.0)], 1)
            A[:, 0] = np.degrees(np.unwrap(np.radians(A[:, 0])))
            A[:, 0] -= 360.0 * round(A[0, 0] / 360.0)
            if np.abs(A - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[n] = A
        vis = [{sl_ho[k]: nm for k, nm in enumerate(F["n"])} for F in fr]
        sau = [F["o"].index(sl_ho.index("P_shouL2")) < F["o"].index(sl_ho.index("P_shenti2")) for F in fr]
        wpos = {b: Bw[:, ten.index(b), :2] for b in CHAIN + NAM}
        out[clip] = (float(v["dur"]), res, len(fr), vis, sau, wpos)
    return out


# ---------------------------------------------------------------- mốc giờ
M_ATK = [(0.0, 0.0), (0.40, 0.40), (0.50, 0.50), (0.78, 1.10), (0.98, 1.30), (1.30, 1.70)]   # attack: (giờ mình, giờ skill_02_1)
T_VUON, T_ATK, D_ATTACK = 0.42, 0.50, 1.30
M_CAST = [(0.0, 0.0), (0.60, 0.60), (1.15, 1.10), (1.70, 1.8333)]            # cast: (giờ mình, giờ skill_03)
T_CAM, T_TROI, T_TRUNG_C, T_LUN, D_CAST = 0.60, 0.74, 0.84, 1.04, 1.70
# skill: há hàm khổng lồ → hút → nuốt → quả bóng mặt căng, quẫy → gai đâm xuyên → gai rút → nhả, về dáng đứng
# skill: co rúm → LAO tới (há hàm khổng lồ giữa không trung) → chạm đích, NGOẠM (sập hàm, bẹp) → quả bóng mặt căng (bậc, phồng dần) →
# quẫy → gai đâm xuyên → gai rút → căng rồi bẹp → nhả (tướng hiện lại còn phồng, xẹp dần) → nhảy lùi về chỗ
# lượt sửa 3 (người dùng 2026-11-17): hàm há LỐ (phóng to + banh hai hàm) để nuốt gọn; gai hai đợt dày; thôi làm bóng thì ọe rồi NHỔ đối thủ
# ra, sức nhổ hất tướng bay lùi về chỗ
T_LAO0, T_HA, T_MO, T_DAP, T_NGOAM, T_DOI = 0.42, 0.56, 0.74, 0.86, 0.92, 0.99
T_GIAY, T_DAM, T_TRUNG_S, T_DAM2, T_RUT, T_NHA = 1.24, 1.78, 1.94, 2.16, 2.72, 3.00
T_OE, T_NHO, T_VE0, T_VE1, D_SKILL = 3.12, 3.44, 3.54, 3.90, 4.30
HA_TO, HA_NHO = 1.70, 1.50      # hàm khổng lồ phóng to lúc há ngoạm / lúc nhổ
HA_TREN, HA_DUOI = 36.0, 28.0   # banh thêm: hàm trên ngửa lên, hàm dưới trễ xuống (độ)
BAT_NHO = 0.07                  # tướng bật khỏi đất theo sức nhổ (× chiều cao)
LO_LUNG = 0.08                  # tướng còn lơ lửng lúc ngoạm (× chiều cao)
B_DOI = 1.00                    # cỡ quả bóng lúc vừa đổi (khớp hàm to vừa sập)
if NON:                         # đầu dạng non đã to 1,45 lần: hàm khổng lồ phóng ít hơn
    HA_TO, HA_NHO = 1.35, 1.25
D_LAO = 1.25                    # độ dời cú lao trong rig (× chiều cao); game co cho đỉnh lao = 72 % quãng tới đối thủ
# appear: cục đất rơi (0 → 0,36), chạm đất nảy, chạm lần hai 0,76, bung 0,82 thành tướng (appear_01 từ 0,42), gầm 1,65
T_NAY1, T_NAY2, T_BUNG, T_GAM_A, D_APPEAR = 0.36, 0.76, 0.84, 1.75, 2.60
T_A0 = 0.44                     # tướng bung ra ở dáng bẹp của appear_01
D_IDLE = 2.6667


def lam_clip(sk, info, cao=1000.0):
    CD = chuyen_dong(info)
    far0 = np.array(info["far"])
    if NON:
        # dạng non: chuỗi tay co giãn (gắn vào fly ở gốc toạ độ, chuyển động theo toạ độ THẾ GIỚI của con gốc) không theo tỉ lệ thân / tay
        # xa. Mỗi khung: điểm vai dời theo vai mới (bone19 của rig đã nhân tỉ lệ, cùng dáng gốc), co K_TAY_CO quanh vai; pha dần theo phần
        # quãng vai → far nên đầu nắm đấm vẫn tới đúng far (game lái far tới đối thủ). Tay mảnh / nắm đấm nhỏ: nhân tỉ lệ K_TAY_CO.
        ten_ = info["ten"]
        i19 = ten_.index("bone19")
        for goc_ten, (dur_, R_, n_, VIS_, SAU__, WP_) in CD.items():
            Bw = np.array([F["b"] for F in info["S"][goc_ten]["frames"]], float)
            A19 = Bw[:, i19, :2]
            for b in CHAIN + NAM:
                if b not in R_:
                    R_[b] = np.tile(np.array([0.0, 0.0, 0.0, 1.0, 1.0]), (n_, 1))
            for i in range(n_):
                P0 = khung.Pose()
                for b, Ar in R_.items():
                    if b in REPARENT:
                        continue
                    v = Ar[i]
                    P0.rot(b, float(v[0]))
                    P0.move(b, float(v[1]), float(v[2]))
                    P0.scale(b, float(v[3]), float(v[4]))
                B19 = sk.the_gioi(P0)["bone19"][:2, 2]
                S0 = WP_["all2"][i].copy()
                d = far0 - S0
                dd = max(float(np.dot(d, d)), 1e-6)
                for b in CHAIN + NAM:
                    p = WP_[b][i].copy()
                    w = float(np.clip(np.dot(p - S0, d) / dd, 0.0, 1.0))
                    q = B19 + K_TAY_CO * (p - A19[i])
                    dp = (1.0 - w) * (q - p)
                    R_[b][i, 1] += dp[0]
                    R_[b][i, 2] += dp[1]
                    R_[b][i, 3] *= K_TAY_CO
                    R_[b][i, 4] *= K_TAY_CO
                    WP_[b][i] = p + dp
    slot_cua = [(e_[0], e_[3]) for e_ in SLOT if e_[3]]
    anh_cua = {e_[0]: (e_[4] if len(e_) > 4 else e_[0].split("@")[0]) for e_ in SLOT}

    def dat(P, goc, tau, lap=False, chi=None, bo=None, k=1.0, w_fly=None, hien=True, truoc_g=False):
        """đặt dáng clip gốc `goc` ở giây tau (nội suy hai khung mẫu). w_fly(k, pos) → phần quãng tới far của xương chuỗi k (None = 0)."""
        dur, R, n, VIS, SAU_, WP = CD[goc]
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
        if w_fly is not None:                                    # xương chuỗi tay co giãn: fly ở w·far, con bù lại cho đúng thế giới
            pos = {b: WP[b][i0] * (1 - w) + WP[b][i1] * w for b in CHAIN + NAM}
            for kk, b in enumerate(CHAIN):
                wk = float(w_fly(kk, pos))
                if wk > 1e-4:
                    P.move(f"fly_tay{kk}", wk * far0[0], wk * far0[1])
                    P.move(b, -wk * far0[0], -wk * far0[1])
                    if b == "all2h":
                        for bn in NAM:
                            P.move(bn, -wk * far0[0], -wk * far0[1])
        if hien:
            j = min(n - 1, int(round(x)))
            V, sau = VIS[j], SAU_[j]
            for s, lai in slot_cua:
                nm = V.get(lai)
                if s in TRUOC:
                    nm = nm if truoc_g else None
                elif s.startswith("G_") and truoc_g:
                    nm = None
                elif s in SAU:
                    nm = nm if sau else None
                elif s.split("@")[0] + "@sau" in SAU and sau:
                    nm = None
                if s in ("than", "than_lot", "vung_bun", "tay_xa_tren", "tay_xa_duoi", "tay_xa_duoi@sau", "long_mieng", "ham", "dau", "vai_gan",
                         "tay_gan"):
                    nm = anh_cua[s] if nm else None
                elif s == "mat":
                    nm = P.att.get("mat", "mat") if nm else None
                elif nm and s in info["hinh_cua"] and nm not in info["hinh_cua"][s]:
                    nm = info["hinh_cua"][s][0]
                P.att[s] = nm

    def pha(P, Pb, w):
        if w <= 1e-4:
            return
        for b in set(P.t) | set(Pb.t):
            a_ = P._g(b)
            b_ = Pb.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            for q in range(5):
                a_[q] += (b_[q] - a_[q]) * w

    def dang(goc, tau, **kw):
        Q = khung.Pose()
        dat(Q, goc, tau, hien=False, **kw)
        for b, g in Q.t.items():
            g[2] = ((g[2] + 180.0) % 360.0) - 180.0
        return Q

    def dam(P, a):
        if a < 0.999:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])

    def song_(t, chu_ky, tre=0.0):
        return math.sin(2 * math.pi * (t - tre) / chu_ky)

    def w_vuon(kk, pos):
        """phần quãng từ vai (all2) tới far của xương chuỗi kk (chiếu lên đoạn vai → far)."""
        S0 = pos["all2"]
        d = far0 - S0
        return float(np.clip(np.dot(pos[CHAIN[kk]] - S0, d) / max(np.dot(d, d), 1e-6), 0.0, 1.0))

    # ------------------------------------------------ idle: hai chu kỳ nền idle_01 + chớp mắt + bong bóng bùn trên lưng (VFX)
    def f_idle(t, P):
        dat(P, "idle_01", t, True)
        if 1.02 < t < 1.16 or 2.30 < t < 2.40:
            P.att["mat"] = "mat_nham"
        # thạch bùn: thân nở xẹp nhẹ trễ pha so với nhịp thở của họ
        P.scale("bone2", 1.0 + 0.012 * song_(t, D_IDLE / 2, 0.2), 1.0 - 0.012 * song_(t, D_IDLE / 2, 0.2))

    def f_walk(t, P):
        dat(P, "run_01", t, True)

    def f_hit(t, P):
        dat(P, "hit_01", t)
        k = math.exp(-max(0.0, t - 0.06) / 0.12) * math.sin(min(1.0, t / 0.06) * math.pi * 0.5)
        P.scale("bone2", 1.0 + 0.05 * k, 1.0 - 0.06 * k)          # lún vào như thạch
        if t > 0.06:
            r = math.exp(-(t - 0.06) / 0.10) * math.sin((t - 0.06) * 2 * math.pi / 0.16)
            P.scale("bone2", 1.0 - 0.03 * r, 1.0 + 0.035 * r)

    # ------------------------------------------------ attack: nhún, rướn, TAY BÙN VƯƠN tới đối thủ (game lái), đấm, quẫy, co về
    def f_attack(t, P):
        tau = tmap(t, M_ATK)
        dat(P, "skill_02_1", tau, w_fly=w_vuon)
        # tay phóng ra không còn trong một khung: 0,42 → 0,50 các xương chuỗi đi từ vai ra (u: 0,25 → 1), nắm đấm hiện từ 0,42
        if T_VUON - 0.001 < t < T_ATK:
            u = 0.25 + 0.75 * (t - T_VUON) / (T_ATK - T_VUON)
            Q = khung.Pose()
            dat(Q, "skill_02_1", 0.50, w_fly=w_vuon, hien=False)
            W = sk.the_gioi(Q)
            S0 = W["all2"][:2, 2]
            for b in CHAIN + NAM:
                g = Q.t.get(b)
                if g is None:
                    continue
                p = W[b][:2, 2]
                q = S0 + (p - S0) * u
                P.t[b] = list(g)
                P.t[b][0] += q[0] - p[0]
                P.t[b][1] += q[1] - p[1]
            for kk in range(len(CHAIN)):
                f = f"fly_tay{kk}"
                if f in Q.t:
                    P.t[f] = list(Q.t[f])
            for s in ("G_shoudabi", "G_shoubi", "G_shouzhang"):
                P.att[s] = s
            for s in ["tay_xa_tren", "tay_xa_duoi", "tay_xa_duoi@sau", "P_shouL1_1", "P_shouL3", "P_shouL3@sau"] + NGON_L + [x + "@sau" for x in NGON_L]:
                P.att[s] = None
        k = math.exp(-((t - (T_ATK + 0.02)) / 0.05) ** 2)          # giật thân lúc đấm trúng
        P.scale("bone2", 1 + 0.05 * k, 1 - 0.04 * k)

    # ------------------------------------------------ cast: cắm tay xuống bùn, nắm đấm khổng lồ trồi dưới chân đối thủ
    def f_cast(t, P):
        dat(P, "skill_03", tmap(t, M_CAST))
        k = math.exp(-((t - (T_CAM + 0.02)) / 0.05) ** 2)
        P.scale("bone2", 1 + 0.06 * k, 1 - 0.05 * k)
        if T_TROI <= t <= T_LUN + 0.14:
            P.att["nam_ngam"] = "nam_to"
            if t < T_TRUNG_C:
                u = (t - T_TROI) / (T_TRUNG_C - T_TROI)
                sy = 1.18 * (1 - (1 - u) ** 3)
                sx = 0.75 + 0.25 * u
            elif t < T_LUN:
                b = math.exp(-(t - T_TRUNG_C) / 0.06) * math.sin((t - T_TRUNG_C) * 2 * math.pi / 0.14)
                sy, sx = 1.0 + 0.18 * b, 1.0 - 0.08 * b
                P.rot("nam_ngam", 4.0 * hoat.rung(t, T_TRUNG_C, T_LUN, 2) * (1 - (t - T_TRUNG_C) / (T_LUN - T_TRUNG_C)))
            else:
                u = (t - T_LUN) / 0.14
                sy, sx = max(0.001, 1.0 - u * u), 1.0 + 0.15 * u
            P.scale("nam_ngam", sx, sy)
        else:
            P.att["nam_ngam"] = None

    # ------------------------------------------------ skill: co rúm, ĐẦU PHÌNH THÀNH HÀM KHỔNG LỒ, phun bùn đá (VFX), khép
    def an_than(P, a):
        """độ đậm của cả thân tướng (0 = ẩn hẳn)."""
        for sl in TU_THAN:
            if a <= 0.0:
                P.att[sl] = None
            elif a < 0.999:
                P.alpha[sl] = a * P.alpha.get(sl, 1.0)

    def bong_hien(P, a, sx=1.0, sy=1.0, rot=0.0, dy=0.0):
        if a <= 0.0:
            P.att["bong_mat"] = None
            return
        P.att["bong_mat"] = "bong_mat"
        if a < 0.999:
            P.alpha["bong_mat"] = a
        P.scale("bong", sx, sy)
        if rot:
            P.rot("bong", rot)
        if dy:
            P.move("bong", 0.0, dy)

    def xung_(t, t0, dai=0.12):
        """xung 0 → 1 → 0 trong `dai` giây từ t0."""
        if not (t0 <= t <= t0 + dai):
            return 0.0
        return math.sin(math.pi * (t - t0) / dai)

    P_GAM = dang("show_01", 1.05)                                    # dáng há miệng dang tay (gầm / nhả)

    # ------------------------------------------------ skill: LAO TỚI, NGOẠM đối thủ, phồng thành quả bóng mặt căng, gai đâm xuyên, nhả, về
    # (người dùng 2026-11-17: "chiêu cuối phải là lao vào địch, ngoạm địch rồi mới biến thành quả bóng, làm mượt hơn nữa đi").
    # Game lao theo xương `move` (đỉnh cú lao = 72 % quãng tới đối thủ, khai lao=("skill",)); quả bóng ngồi ở chỗ đã lao tới.
    def chui_ham(P, w):
        """hàm khổng lồ chúi về phía trước (há hướng đối thủ)."""
        if w > 1e-4:
            P.rot("bone63", -25.0 * w)

    def sap_ham(P, w):
        """hàm khổng lồ sập lại nửa chừng (khép hẳn thì các mảnh vẽ cho dáng há chồng chéo): hàm trên xuống, hàm dưới lên, mõm dưới (bone65)
        hếch lên che dải họng cam sẫm (không thì dải đó gập thành một mẩu lòi giữa miệng: thử lưới góc 2026-11-17)."""
        if w > 1e-4:
            P.rot("bone67", -40.0 * w)
            P.rot("bone64", 24.0 * w)
            P.rot("bone65", 22.0 * w)

    def ham_lo(P, mo, to):
        """hàm khổng lồ há LỐ (người dùng 2026-11-17: "mồm nó phải há thật to cho lố vào để nuốt gọn đối thủ"): phóng cả hàm quanh gốc bone63
        (`to` lần), banh thêm hàm trên lên, hàm dưới xuống (`mo`)."""
        if abs(to - 1.0) > 1e-4:
            P.scale("bone63", to, to)
        if abs(mo) > 1e-4:
            P.rot("bone67", HA_TREN * mo)
            P.rot("bone64", -HA_DUOI * mo)

    def lao_move(P, t):
        D = D_LAO * cao
        lui = 0.05 * cao                                             # giật lùi khi nhổ
        if t < T_LAO0:                                               # lùi lấy đà
            x = -0.05 * cao * ease((t / T_LAO0), "io")
            y = 0.0
        elif t < T_DAP:                                              # nhảy vồ: cung thấp, nhanh dần; tới đích còn lơ lửng (hàm to không thụt đất)
            u = (t - T_LAO0) / (T_DAP - T_LAO0)
            x = -0.05 * cao + (D + 0.05 * cao) * ease(u, "io")
            y = 0.20 * cao * math.sin(math.pi * u) + LO_LUNG * cao * ease(u, "io")
        elif t < T_DOI:                                              # ngoạm giữa không trung rồi rơi bịch xuống (đổi thành bóng lúc chạm đất)
            u = (t - T_DAP) / (T_DOI - T_DAP)
            x, y = D, LO_LUNG * cao * (1.0 - u * u)
        elif t < T_VE0:
            x, y = D, 0.0
            if t > T_NHO:                                            # nhổ: giật lùi, bật khỏi đất (thân chúi tới không thụt đất)
                e_ = ease((t - T_NHO) / (T_VE0 - T_NHO), "out")
                x -= lui * e_
                y = BAT_NHO * cao * e_
        elif t < T_VE1:                                              # sức nhổ hất bay lùi về chỗ: vọt nhanh, cung thấp, chậm dần khi đáp
            u = (t - T_VE0) / (T_VE1 - T_VE0)
            x = (D - lui) * (1.0 - u) ** 2
            y = BAT_NHO * cao * (1.0 - u) + 0.13 * cao * math.sin(math.pi * u)
        else:
            x, y = 0.0, 0.0
        P.move("move", x, y)
        if abs(y) > 1e-4:                                            # mặt nạ đất (con của move) đứng yên ở mặt đất khi tướng bật lên
            P.move("dat_cat", 0.0, -y)

    def an_bong_gai(P):
        P.att["bong_mat"] = None
        for k in range(len(GAI)):
            P.att[f"gai{k}"] = None

    # dáng skill_04 khi nhổ: co rúm ngậm (0,30) → ọe → ngả lấy đà (0,46) → đổi sang hàm khổng lồ khi chúi tới (0,6) → há (1,0) → bay lùi: chạy
    # ngược skill_04 (hàm khép dần) → đổi về đầu thường ở đúng chỗ đổi của con gốc (0,6), ngay lúc đáp
    TAU_NHO = [(T_NHA, 0.30), (T_OE, 0.36), (T_NHO - 0.10, 0.46), (T_NHO - 0.03, 0.62), (T_NHO + 0.04, 0.86), (T_VE0, 1.0),
               (T_VE0 + 0.20, 0.82), (T_VE1 - 0.03, 0.61), (T_VE1 + 0.03, 0.54)]
    P_VE = dang("skill_04", 0.54)                                    # dáng lúc đáp, pha dần về idle

    def lao_ngoam(t, P):
        # co rúm → nhảy vồ, há hàm khổng lồ (đổi đầu ở 0,6 của skill_04) PHÓNG TO + BANH LỐ giữa không trung → chạm đích, sập hàm
        dat(P, "skill_04", tmap(t, [(0.0, 0.0), (T_LAO0, 0.44), (T_HA, 0.66), (T_DAP, 1.0), (T_DOI, 1.1)]))
        chui_ham(P, hoat.cv(t, [(T_HA, 0.0), (T_DAP - 0.04, 1.0, "out")]))
        to = hoat.cv(t, [(T_HA - 0.04, 0.0), (T_MO, 1.0, "out"), (T_DOI, 1.0)])
        mo = hoat.cv(t, [(T_HA - 0.04, 0.0), (T_MO, 1.0, "out"), (T_DAP - 0.05, 1.1, "io"), (T_NGOAM, 0.0, "in")])
        ham_lo(P, mo, 1.0 + (HA_TO - 1.0) * to)
        nga = hoat.cv(t, [(T_LAO0, 0.0), (T_LAO0 + 0.16, 1.0, "out"), (T_DAP, 0.6, "io")])
        P.rot("bone2", -9.0 * nga)                                # chúi người tới khi bay
        if T_LAO0 <= t < T_DAP:                                    # kéo dài thân theo đà bay
            s_ = 0.06 * math.sin(math.pi * (t - T_LAO0) / (T_DAP - T_LAO0))
            P.scale("bone2", 1.0 + s_, 1.0 - 0.6 * s_)
        sap = hoat.cv(t, [(T_DAP - 0.05, 0.0), (T_NGOAM, 1.0, "in")])
        sap_ham(P, sap)
        bep = hoat.cv(t, [(T_DAP - 0.02, 0.0), (T_NGOAM, 1.0, "in")])
        P.scale("bone2", 1.0 + 0.10 * bep, 1.0 - 0.13 * bep)     # ngoạm + đáp: bẹp xuống

    def bong_gai(t, P):
        # ực rồi phồng: bóng hiện cỡ B_DOI (≈ hàm vừa sập), vọt 1,14 → 0,96 → 1,0; quẫy (phồng từng góc, lắc, nảy)
        sc = hoat.cv(t, [(T_DOI, B_DOI), (T_DOI + 0.12, 1.14, "out"), (T_DOI + 0.26, 0.96, "io"), (T_DOI + 0.38, 1.0, "io")])
        rot, dy = 0.0, 0.0
        if T_GIAY < t < T_DAM:
            env = math.sin(math.pi * (t - T_GIAY) / (T_DAM - T_GIAY))
            rot = 3.5 * env * math.sin(2 * math.pi * 6.0 * (t - T_GIAY))
            dy = 16.0 * env * abs(math.sin(2 * math.pi * 3.0 * (t - T_GIAY)))
            for j, t0 in ((0, T_GIAY + 0.02), (2, T_GIAY + 0.14), (5, T_GIAY + 0.26), (1, T_GIAY + 0.38)):
                P.move(f"bong_r{j}", 80.0 * xung_(t, t0, 0.16), 0.0)
        # gai: đợt 1 từng chiếc dài đâm xuyên (0 → 1,15 → 1, cả bóng giật theo); đợt 2 dồn dập gai ngắn xen giữa; rút cùng lúc (hút vào)
        giat = 0.0
        n1 = len(GAI1)
        for k, (_, kieu, L) in enumerate(GAI):
            if k < n1:
                t0, wg = T_DAM + 0.035 * k, 1.0
            else:
                t0, wg = T_DAM2 + 0.022 * (k - n1), 0.55
            tr = T_RUT + 0.004 * (len(GAI) - 1 - k)
            if t < t0 or t > tr + 0.10:
                P.att[f"gai{k}"] = None
                P.scale(f"gai{k}", 0.001, 1.0)                       # gai ẩn giữ cỡ 0 (60 khung/giây không lộ khung nội suy)
                continue
            P.att[f"gai{k}"] = f"gai_{kieu}"
            g = hoat.cv(t, [(t0, 0.0), (t0 + 0.06, 1.15, "out"), (t0 + 0.12, 1.0, "io"), (tr, 1.0), (tr + 0.10, 0.0, "in")])
            P.scale(f"gai{k}", max(0.001, g * L), (0.85 + 0.15 * min(g, 1.0)) * (0.75 + 0.25 * L))
            if t < t0 + 0.25:
                giat += wg * math.exp(-(t - t0) / 0.05)
        if T_DAM <= t < T_RUT + 0.1:
            env = min(1.0, (t - T_DAM) / 0.05) * float(np.clip((T_RUT + 0.1 - t) / 0.3, 0, 1))
            rot += 2.0 * env * math.sin(2 * math.pi * 11.0 * (t - T_DAM))
        sc *= 1.0 + 0.03 * min(1.5, giat)
        # trước khi thôi làm bóng: phồng căng rồi bẹp ngang
        cang = hoat.cv(t, [(T_RUT + 0.1, 0.0), (T_NHA - 0.10, 1.0, "io"), (T_NHA, 0.0, "in")])
        b = hoat.cv(t, [(T_NHA - 0.10, 0.0), (T_NHA, 1.0, "in")])
        ep = hoat.cv(t, [(T_DOI, 1.0), (T_DOI + 0.13, 0.0, "out")])        # bóng vừa đổi còn bẹp ngang như hàm vừa sập, rồi nảy tròn
        sx = sc * (1 + 0.06 * cang) * (1 + 0.16 * b) * (1 + 0.20 * ep)
        sy = sc * (1 + 0.06 * cang) * (1 - 0.16 * b) * (1 - 0.18 * ep)
        bong_hien(P, 1.0, sx, sy, rot, dy - (1 - sy) * BONG_PX[2] * U_B * K_BONG)

    def f_skill(t, P):
        # Chỗ đổi hình (thân ↔ bóng): phần bị ẩn GIỮ NGUYÊN dáng lúc đổi. Runtime nội suy xương giữa hai khoá 30 khung/giây trong khi hình
        # chỉ đổi ở khoá sau, nên nếu xương phần bị ẩn nhảy sang dáng khác thì ở 60 khung/giây lộ một khung méo ngay trước lúc ẩn.
        lao_move(P, t)
        if t < T_DOI:
            lao_ngoam(t, P)
            an_bong_gai(P)
            for k in range(len(GAI)):
                P.scale(f"gai{k}", 0.001, 1.0)
            return
        if t < T_NHA:
            lao_ngoam(T_DOI - 1e-3, P)
            an_than(P, 0.0)
            bong_gai(t, P)
            return
        bong_gai(T_NHA - 1e-3, P)
        # tướng hiện lại (bậc) còn PHỒNG, đang ngậm đối thủ → ọe hai cái → ngả người lấy đà → chúi tới NHỔ: hàm khổng lồ há lố, thân xẹp
        # phụt → sức nhổ hất tướng bay lùi về chỗ (hàm khép dần, đổi về đầu thường lúc đáp) → đáp bẹp, nảy thạch, về dáng đứng
        an_bong_gai(P)
        if t < T_VE1 + 0.03:
            dat(P, "skill_04", tmap(t, TAU_NHO))
        else:
            dat(P, "idle_01", 0.0)
            pha(P, P_VE, hoat.cv(t, [(T_VE1 + 0.03, 1.0), (D_SKILL - 0.06, 0.0, "io")]))
        # phồng (ngậm) → xẹp phụt khi nhổ → nảy về 1,0
        ph = hoat.cv(t, [(T_NHA, 1.16), (T_NHA + 0.10, 1.10, "io"), (T_NHA + 0.20, 1.14, "io"), (T_NHO - 0.03, 1.14),
                         (T_NHO + 0.06, 0.93, "out"), (T_NHO + 0.20, 1.03, "io"), (T_VE0 + 0.16, 1.0, "io")])
        co_than(P, ph)
        k_ = math.exp(-(t - T_NHA) / 0.14) * math.sin((t - T_NHA) * 2 * math.pi / 0.28)
        P.scale("bone2", 1 + 0.07 * k_, 1 - 0.08 * k_)
        # cố ngậm: run bần bật (đối thủ quẫy trong bụng); ọe: hai cơn thót (thân vươn cao, đầu giật ngửa)
        if T_NHA + 0.04 < t < T_NHO - 0.04:
            r = hoat.rung(t, T_NHA + 0.04, T_NHO - 0.04, 4)
            P.move("bone2", 3.0 * r, 0.0)
            P.rot("bone6", 1.5 * r)
        h = xung_(t, T_OE, 0.14) + 0.85 * xung_(t, T_OE + 0.16, 0.14)
        if h > 0:
            P.scale("bone2", 1 - 0.08 * h, 1 + 0.14 * h)
            P.rot("bone2", 5.0 * h)
        # ngả lấy đà → chúi tới nhổ
        nga_sau = hoat.cv(t, [(T_OE + 0.30, 0.0), (T_NHO - 0.05, 1.0, "io"), (T_NHO + 0.01, 0.0, "in")])
        day_toi = hoat.cv(t, [(T_NHO - 0.05, 0.0), (T_NHO + 0.01, 1.0, "out"), (T_VE0, 0.7, "io"), (T_VE0 + 0.12, 0.0, "io")])
        P.rot("bone2", 9.0 * nga_sau - 8.0 * day_toi)
        if nga_sau > 0:
            P.scale("bone2", 1 - 0.05 * nga_sau, 1 + 0.07 * nga_sau)
        # hàm khổng lồ khi nhổ: chúi về đối thủ, phóng to, banh lố, rung (dòng nhổ), khép dần khi bay lùi
        if T_NHO - 0.06 < t < T_VE1 + 0.03:
            chui_ham(P, hoat.cv(t, [(T_NHO - 0.06, 0.0), (T_NHO, 1.0, "out"), (T_VE0, 0.8), (T_VE1 - 0.04, 0.0, "io")]))
            to = hoat.cv(t, [(T_NHO - 0.04, 0.0), (T_NHO + 0.04, 1.0, "out"), (T_VE0 + 0.05, 1.0), (T_VE1 - 0.04, 0.0, "io")])
            mo = hoat.cv(t, [(T_NHO - 0.04, 0.0), (T_NHO + 0.03, 1.1, "out"), (T_NHO + 0.10, 0.9, "io"), (T_VE0, 1.0, "io"),
                             (T_VE1 - 0.04, 0.0, "io")])
            ham_lo(P, mo, 1.0 + (HA_NHO - 1.0) * to)
            if T_NHO < t < T_VE0 + 0.06:
                r = hoat.rung(t, T_NHO, T_VE0 + 0.06, 3)
                P.rot("bone63", 2.5 * r)
        # bay lùi: ngả ra sau; đáp: bẹp rồi nảy thạch
        if T_VE0 < t < T_VE1:
            u = (t - T_VE0) / (T_VE1 - T_VE0)
            P.rot("bone2", 8.0 * math.sin(math.pi * u))
        bd = xung_(t, T_VE1 - 0.03, 0.18)
        if bd > 0:
            P.scale("bone2", 1 + 0.10 * bd, 1 - 0.12 * bd)
        if t > T_VE1 + 0.15:
            k2 = math.exp(-(t - T_VE1 - 0.15) / 0.12) * math.sin((t - T_VE1 - 0.15) * 2 * math.pi / 0.26)
            P.scale("bone2", 1 + 0.05 * k2, 1 - 0.06 * k2)

    def co_than(P, s):
        """co / phồng cả thân tướng quanh điểm trên mặt đất dưới tâm quả bóng (xương all là gốc thân)."""
        if abs(s - 1.0) < 1e-4:
            return
        ax, ay = sk.W0["all"][:2, 2]
        px_, py_ = sk.W0["bong"][0, 2], info["y_day"]
        P.scale("all", s, s)
        P.move("all", (1 - s) * (px_ - ax), (1 - s) * (py_ - ay))

    # ------------------------------------------------ appear: cục đất tròn rơi từ trên, nảy, BUNG ra: cục đất phình rồi tan, tướng nở dần từ
    # trong ra (nảy đàn hồi) thay vì đổi bậc (người dùng 2026-11-17: "đoạn bung ra trong appear nhìn chưa mượt")
    def f_appear(t, P):
        rc = CUC_PX[2] * U_B * K_CUC
        if t < T_BUNG:
            dat(P, "appear_01", T_A0, hien=False)
            an_than(P, 0.0)
        else:
            dat(P, "appear_01", min(1.0, T_A0 + 0.9 * (t - T_BUNG)))
            # tướng nở từ 0,42 → 1,08 → 0,97 → 1,0 quanh mặt đất dưới tâm cục đất: 0,08 s đầu nằm khuất sau cục đất đang phình (còn
            # đặc), cục đất tan trong 2 khung thì tướng đã gần đủ cỡ, nảy đàn hồi tiếp
            s = hoat.cv(t, [(T_BUNG, 0.42), (T_BUNG + 0.08, 0.86, "out"), (T_BUNG + 0.17, 1.08, "out"), (T_BUNG + 0.30, 0.97, "io"),
                            (T_BUNG + 0.42, 1.0, "io")])
            co_than(P, s)
            k_ = math.exp(-(t - T_BUNG - 0.17) / 0.12) * math.sin(max(0.0, t - T_BUNG - 0.17) * 2 * math.pi / 0.26)
            P.scale("bone2", 1 + 0.06 * k_, 1 - 0.07 * k_)
        P.att["bong_dat"] = "bong_dat" if t < T_BUNG + 0.14 else None
        if t < T_NAY1:                                                  # rơi tự do, xoay nhẹ
            u = t / T_NAY1
            P.move("cuc", 0.0, 0.8 * cao * (1 - u * u))
            P.rot("cuc", -35.0 * (1 - u))
            P.alpha["bong_dat"] = min(1.0, t / 0.12)
        elif t < T_NAY2:
            h = 0.18 * cao
            tm = (T_NAY1 + T_NAY2) / 2 + 0.03
            if t < tm:
                u = (t - T_NAY1) / (tm - T_NAY1)
                y_ = h * (1 - (1 - u) ** 2)
            else:
                u = (t - tm) / (T_NAY2 - tm)
                y_ = h * (1 - u * u)
            bep = xung_(t, T_NAY1, 0.12)
            P.scale("cuc", 1 + 0.25 * bep, 1 - 0.28 * bep)
            P.move("cuc", 0.0, y_ - 0.28 * bep * rc)
        elif t < T_BUNG + 0.14:
            bep = hoat.cv(t, [(T_NAY2, 0.0), (T_BUNG, 1.0, "out")])        # chạm lần hai: bẹp, gồng
            sx, sy = 1 + 0.26 * bep, 1 - 0.30 * bep
            if t >= T_BUNG:                                             # bung: phình tròn to (còn đặc, che tướng đang nở) rồi tan nhanh
                u = min(1.0, (t - T_BUNG) / 0.08)
                ph = 1.0 - (1.0 - u) ** 2
                sx, sy = sx + (1.55 - sx) * ph, sy + (1.65 - sy) * ph
                if t > T_BUNG + 0.08:
                    v = min(1.0, (t - T_BUNG - 0.08) / 0.035)
                    sx, sy = sx * (1 + 0.12 * v), sy * (1 + 0.12 * v)
                    P.alpha["bong_dat"] = max(0.0, 1.0 - v)
            P.scale("cuc", sx, sy)
            P.move("cuc", 0.0, -(1 - sy) * rc)
        if T_GAM_A - 0.25 < t:
            gam = hoat.cv(t, [(T_GAM_A - 0.25, 0.0), (T_GAM_A, 1.0, "out"), (T_GAM_A + 0.40, 1.0), (D_APPEAR - 0.04, 0.0, "io")])
            pha(P, P_GAM, gam)
            if T_GAM_A < t < T_GAM_A + 0.40:
                r = hoat.rung(t, T_GAM_A, T_GAM_A + 0.40, 2)
                P.rot("bone6", 1.8 * r)
                P.move("bone2", 2.0 * r, 0.0)

    # ------------------------------------------------ die: die_01 + chảy tan thành vũng rồi thấm xuống
    D_DIE = CD["die_01"][0]

    def f_die(t, P):
        dat(P, "die_01", min(t, D_DIE))
        u = float(np.clip((t - 0.55) / (D_DIE + TAN - 0.55), 0, 1))
        sy = 1.0 - 0.55 * u * u                                     # co dẹt quanh MẶT ĐẤT (gốc xương all nằm dưới đáy hình)
        P.scale("all", 1.0 + 0.25 * u, sy)
        P.move("all", 0.0, (1.0 - sy) * (info["y_day"] - info["y_all"]))
        dam(P, float(np.clip(1.0 - (t - D_DIE) / TAN, 0.0, 1.0)))

    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=[(0.02, "roi", ""), (T_NAY1, "nay", ""), (T_NAY2, "nay", ""), (T_BUNG, "bung", ""),
                                                (T_GAM_A, "gam", "")]),
        Clip("idle", D_IDLE, f_idle, loop=True, ev=[(1.90, "bong", "")]),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", D_ATTACK, f_attack, ev=[(T_VUON, "vuon", ""), (T_ATK, "trung", "")], trung=T_ATK),
        Clip("cast", D_CAST, f_cast, ev=[(T_CAM, "cam", ""), (T_TROI, "troi", ""), (T_TRUNG_C, "trung", "")], trung=T_TRUNG_C),
        Clip("skill", D_SKILL, f_skill, ev=[(T_LAO0, "lao", ""), (T_HA, "ha", ""), (T_NGOAM, "ngoam", ""), (T_DOI, "phong", ""),
                                            (T_GIAY, "giay", ""), (T_DAM, "dam", ""), (T_TRUNG_S, "trung", ""), (T_DAM2, "dam", ""),
                                            (T_RUT, "rut", ""), (T_NHA, "hien", ""), (T_OE, "oe", ""), (T_NHO + 0.03, "nho", ""),
                                            (T_VE0, "ve", "")], trung=T_TRUNG_S),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", D_DIE + TAN, f_die, ev=[(0.55, "chay", "")]),
    ]
    if NON:
        # dạng non đầu to 1,45 lần: hàm dưới lúc gầm (appear), hàm khổng lồ lúc nhổ (skill), hàm lúc chảy sụp (die) thụt sâu hơn mép mặt nạ
        # đất (đo 2026-11-17: −46 / −80 / −41 đơn vị). Ba clip này không cắm gì xuống đất nên hạ mặt nạ thêm H_CAT_NON (cast giữ nguyên).
        def ha_cat(fn):
            def g(t, P):
                fn(t, P)
                P.move("dat_cat", 0.0, -H_CAT_NON)
            return g
        for c in clips:
            if c.ten in ("appear", "skill", "die"):
                c.fn = ha_cat(c.fn)
    return clips


def dung_het():
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0) - info["y_day"]
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
            Wl = [sk.the_gioi(P) for P in fr]
            for i in range(1, len(fr)):
                for b in sk.bi:
                    ga, gb = _goc(Wl[i - 1][b]), _goc(Wl[i][b])
                    da = abs((gb - ga + 180.0) % 360.0 - 180.0)
                    if da > 40.0:
                        xau.append(f"{i / 30:.2f}s {b} xoay {da:.0f}°")
            print(f"{c.ten}: {len(fr)} khung" + ("" if not xau else " | " + "; ".join(xau[:16]) + (" ..." if len(xau) > 16 else "")))
        return
    if a and a[0] == "day":
        for c in clips:
            fr = hoat.nuong(sk, c)
            lo = []
            for i, P in enumerate(fr):
                items, _ = ve0.skin(P)
                ys = [V[:, 1].min() for nm, _, V, _, _, al, _, _ in items if al > 0.01 and not nm.startswith(("G_", "nam_ngam"))]
                if ys:
                    lo.append((min(ys) - info["y_day"], i / 30))
            m = min(lo)
            print(f"{c.ten}: đáy thấp nhất {m[0]:.0f} đơn vị so với đáy idle (giây {m[1]:.2f})")
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
        if len(a) > 4:
            Bx = tuple(float(v) for v in a[4].split(","))
        sc = float(a[3]) if len(a) > 3 else 0.3
        cot = min(len(Ps), 6)
        hang = (len(Ps) + cot - 1) // cot
        out = None
        for i, P in enumerate(Ps):
            im = ve0.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
            ImageDraw.Draw(im).text((6, 4), f"{ts[i]:.2f}", fill=(255, 255, 255))
            if out is None:
                out = Image.new("RGB", (im.width * cot, im.height * hang), (150, 150, 150))
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de=TIEU_DE, dang=1, so_dang=1,
                  dung_yen=("attack", "cast"), lao=("skill",), far=("attack", "cast"), mieng="mieng_to", ma_goc=None, khop_idle=0.2, cao=cao,
                  impact=IMPACT, tol={"rotate": 0.15, "translate": 0.3, "scale": 0.003}, dich_mb=0.4, tran_mb=0.5, span=3.6)
    # trang xem: xuat lấy khung GIỮA mỗi clip làm khung nhìn → cú lao, quả bóng và gai của skill (sau giữa clip) bị xén. Dựng lại trang
    # với khung nhìn ôm mọi khung (mỗi 5 khung) của mọi clip.
    bs = []
    for c in clips:
        for i, P in enumerate(hoat.nuong(sk, c)):
            if i % 5 == 0 and any(x[5] > 0.02 for x in ve0.skin(P)[0]):
                bs.append(ve0.bao(P))
    B = soi._union(bs, 0.06)
    tk = json.load(open(os.path.join(RA, "bao_cao.json"), encoding="utf-8"))
    nk = tk.get("khoa", 0)
    info_ = (f"{tk['xuong']} xương · {tk['slot']} slot · {tk['dinh']} đỉnh · {tk['tam_giac']} tam giác · {len(tk['clip'])} clip · {nk} khoá · "
             f".atomik {tk['atomik_kb'] / 1024:.2f} MB")
    xuat.trang_xem(RA, TEN_RIG, TIEU_DE, [c.ten for c in clips],
                   ((B[0] + B[2]) / 2, (B[1] + B[3]) / 2, B[2] - B[0], B[3] - B[1]), info_)
    print("trang xem: khung nhìn", [round(v) for v in B])


if __name__ == "__main__":
    main(sys.argv[1:])
