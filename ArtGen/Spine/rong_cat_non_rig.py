# -*- coding: utf-8 -*-
"""Sa Long DẠNG 1 (dạng non; mã rong_cat_non; tướng ải 15 đảo Thổ, id game ho_khoan; dạng 2 = rong_cat_1 trên rig 3424): hình của mình
chạy trên ĐÚNG rig của con gốc monster_3529 (thằn lằn rồng gai bốn chân, game tham khảo). Ghi chú: inbox/rong_cat_non_ghichu.md. Cách
làm như than_lan_cat_2_rig.py:
- XƯƠNG: đủ xương của họ (FK; 4 IK của họ đã được runtime nướng vào `l` của mẫu khung sample_goc.json), thêm `move` (cú lao), `day` (đáy
  thân), `tam` (tâm thân), `mieng` (đầu vuốt trước gần: chỗ phóng lưỡi cát), `vuot_xa` (đầu vuốt trước xa), `pl_a/b/c` (ba phiến lưng).
  Mười một xương của họ để inherit = 2 (NoRotationOrReflection: chuỗi cổ đầu bone4 → bone5 → bone23 → bone6, chuỗi đuôi bone19 → bone20
  → bone21 → bone22 → bone40, gai đuôi bone31, bone32): CUỐI mỗi khung bù lần lượt từ cha xuống con (`bu_ke_thua`).
- MẢNH: rong_cat_non_manh.py (năm tờ Magnific cắt thẳng trên concept duyệt) → inbox/rong_cat_non/manh/. Mỗi mảnh là lưới phủ hình, mỗi
  đỉnh biến dạng như điểm tương ứng trên HỢP lưới các part của họ (trong_so_goc) + làm mịn trọng số (lam_muot). Thân gộp shenti_1,
  shenti_2, bozi_1 (cổ uốn theo chuỗi cổ của họ); bốn chân gộp các khúc + vuốt của từng chân; đuôi theo weiba_2; đầu + mắt cứng trên
  bone6; ba phiến lưng cứng trên xương riêng (con của xương thân có trọng số lớn nhất ở gốc phiến). BỎ: shadow, mười tám vảy / gai
  `linpian_*` (chùm gai mào, gai lưng lớn của họ: concept chỉ có hai sừng ngắn trong mảnh đầu và vài phiến nhỏ).
- CHUYỂN ĐỘNG (giống ý Sa Long dạng 2, nhẹ hơn, dáng non):
    idle   = MỀM: khung 0 idle_01 + sóng lệch pha (thở, cổ đầu trễ, đuôi trễ dần, phiến nhấp nhô) + trò: VẪY ĐUÔI tíu tít, nghiêng đầu
             tò mò, chớp mắt;
    walk   = run_01 + phiến nhấp nhô; hit = hit_01 + phiến bật;
    attack = skill_01_01 (ngửa lấy đà, vồ chém vuốt 0,40) + `move` lao tới;
    cast   = skill_01_03 (giơ vuốt gần, quét chém xuống 0,40) + giữ dáng: hai lưỡi cát (VFX) phóng ở chem1 0,40, chem2 0,47;
    skill  = skill_03 (thu người, chồm đứng thẳng giơ vuốt gồng 0,60–1,40, giáng xuống nện đất 1,60) + giữ dáng nện rung: cột sa thạch
             (VFX) trồi ở cot1 1,76, cot2 1,96 = trúng;
    appear = rơi từ trên xuống đáp phịch, ngẩng đầu gầm (dáng skill_01_02), về đứng;
    die    = die_01 + mờ.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/rong_cat_non_rig.py      → inbox/rong_cat_non/rig/
    py -3 -I ArtGen/Spine/rong_cat_non_rig.py soi <clip> <giây,giây,...|n=12|t0:t1:n> [tỉ lệ]   → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/rong_cat_non_rig.py kiem                                            đo góc nhảy, bước dời
    py -3 -I ArtGen/Spine/rong_cat_non_rig.py diem                                            bảng vị trí xương cho VFX game
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

G = D2.dat_non("rong_cat")                                    # đặt trạng thái hoa_ho về con 3529 SAU mọi import
TEN_RIG = "rong_cat_non"
D_PX = float(os.environ.get("RCN_DPX", "0.62"))             # pixel ảnh atlas cho mỗi đơn vị rig
MANH = os.path.join(G.BASE, "manh")
RA = os.environ.get("RCN_RA") or os.path.join(G.BASE, "rig")
TAN = 0.45
FPS = 30.0
W_C, H_C = 1536, 1024
IMPACT = {"attack": (0.06, 0.35, 0.09), "cast": (0.06, 0.32, 0.08), "skill": (0.12, 0.70, 0.16, "#fff3d240")}

TAY_GAN = ["shou_1", "shou_2", "shou_3", "zhuazi_1", "zhuazi_2", "zhuazi_3"]
TAY_XA = ["shou_4", "shou_5", "shou_6", "zhuazi_10", "zhuazi_11", "zhuazi_12"]
CHAN_GAN = ["tui_1", "tui_2", "tui_3", "zhuazi_4", "zhuazi_5", "zhuazi_6"]
CHAN_XA = ["tui_4", "tui_5", "tui_6", "zhuazi_7", "zhuazi_8", "zhuazi_9"]
THAN = ["shenti_2", "shenti_1", "bozi_1"]
# slot của mình (thứ tự vẽ, sau → trước): (slot = tên mảnh, [hình], nguồn gắn: list slot của họ ở idle 0 | ("cung", xương))
SLOT = [
    ("tay_xa", ["tay_xa"], TAY_XA),
    ("chan_xa", ["chan_xa"], CHAN_XA),
    ("duoi", ["duoi"], ["weiba_2"]),
    ("than", ["than"], THAN),
    ("pc", ["pc"], ("cung", "pl_c")),
    ("pb", ["pb"], ("cung", "pl_b")),
    ("pa", ["pa"], ("cung", "pl_a")),
    ("chan_gan", ["chan_gan"], CHAN_GAN),
    ("tay_gan", ["tay_gan"], TAY_GAN),
    # người dùng 2026-11-17 (dáng gầm): "đầu và thân bị ghép hở, sao bạn không tách hàm ra để há mồm được". Hàm dưới (T7: hàm + răng dưới +
    # lòng miệng thuộc hàm) cứng trên xương `ham` (bản lề góc miệng), vẽ SAU đầu; đầu không hàm dưới (T6, giữ hàng răng trên) bám LƯỚI:
    # mặt, mõm, sừng, mắt cứng theo bone6, gáy + phiến má dưới (phía sau góc miệng) hoà dần sang trọng số hợp lưới tou_1 + bozi_1 của họ
    # (cùng trọng số với đỉnh cổ trong mảnh thân) → đầu, cổ uốn cùng nhau, không hở khi ngẩng / cúi.
    ("ham", ["ham"], ("cung", "ham")),
    ("dau", ["dau_tren"], ("hoa", ["tou_1", "bozi_1"], "bone6")),
    ("mat", ["mat", "mat_nham"], ("cung", "bone6")),
]
# vùng đầu hoà sang trọng số cổ (px concept): phía sau góc miệng (x < 900) và thấp (y > 450: dưới đáy phiến mang tai, để phiến cứng
# theo đầu, không bị kéo xiên thành sợi lúc lao tới), đậm dần xuống dưới / ra sau
HOA_X, HOA_Y = (930.0, 860.0), (500.0, 560.0)


_KC_DAU = {}


def _kc_dau(ten):
    """khoảng cách (px concept) tới hình bóng một mảnh (dau_tren / ham), 0 trong hình."""
    if ten not in _KC_DAU:
        import cv2
        hop = json.load(open(os.path.join(MANH, "dat.json"), encoding="utf-8"))[ten]["hop"]
        a = np.array(Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA"))[:, :, 3] > 40
        m = np.zeros((1024, 1536), np.uint8)
        m[hop[1]:hop[1] + a.shape[0], hop[0]:hop[0] + a.shape[1]] = a
        _KC_DAU[ten] = cv2.distanceTransform((m == 0).astype(np.uint8), cv2.DIST_L2, 5)
    return _KC_DAU[ten]


KEO_XA = {"dau_tren": 75.0, "ham": 32.0}


def _keo_co(PX):
    """mức bám xương đầu của đỉnh cổ / họng trong mảnh thân (px concept): 0,85 trong hình bóng đầu, về 0 cách đầu 75 px; quanh hàm
    dưới chỉ 32 px (hàm nằm thấp sát ngực: kéo rộng thì ngực, đỉnh vai chân trước xa bị lôi theo đầu, lộ vai xa — soi walk).
    Đo theo khoảng cách tới đầu (tức dọc cổ) cho gáy và họng cùng một thước để cổ giãn đều như ống khi lao tới / ngẩng / cúi:
    nét viền lưng, nâu, vạch họng, kem họng cùng giãn, không xiên lệch nhau, không hở khe nền ở gáy."""
    xi = np.clip(np.round(PX[:, 0]).astype(int), 0, 1535)
    yi = np.clip(np.round(PX[:, 1]).astype(int), 0, 1023)
    g = np.zeros(len(PX))
    for ten, xa in KEO_XA.items():
        g = np.maximum(g, np.clip(1.0 - _kc_dau(ten)[yi, xi] / xa, 0, 1))
    return 0.85 * g * g * (3 - 2 * g)


KEO = {"than": ("bone6", _keo_co)}
KE_THUA_2 = ("bone4", "bone5", "bone23", "bone6", "bone19", "bone20", "bone21", "bone22", "bone31", "bone32", "bone40")   # cha trước con
CO = ("bone4", "bone5", "bone23", "bone6")
DUOI = ("bone19", "bone20", "bone21", "bone22", "bone40")
PHIEN = ("pl_a", "pl_b", "pl_c")
MUOT = {"than": 10, "chan_gan": 8, "chan_xa": 8, "tay_gan": 8, "tay_xa": 8, "duoi": 6}


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
    """gộp lưới của nhiều hình của họ (idle 0) thành một: đỉnh, tam giác, trọng số {tên xương: w}."""
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
    điểm gần nhất trên cạnh + khoảng lệch). Trả hàng (xương, x, y, w) theo ma trận Wi."""
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


def gan_manh(sk, slot, ten_anh, a0s, ten, Wi, mot_xuong=None, hoa=None):
    """hoa = xương cứng: lưới bám hợp lưới a0s nhưng phần ngoài vùng HOA_X / HOA_Y cứng theo xương đó (mặt, mắt), trong vùng hoà dần sang
    trọng số hợp lưới (gáy, má dưới nối cổ), rồi làm mịn 4 vòng."""
    im, (x0, y0, x1, y1), kq = anh_manh(ten_anh)
    if ten_anh not in sk.images:
        sk.anh(ten_anh, im)
    im = sk.images[ten_anh]
    _, to_rig, _ = tf()
    if mot_xuong is None:
        L = luoi.luoi_vung(im, buoc_vien=9.0, buoc_trong=14.0, vien=2, ten=f"{slot}/{ten_anh}", in_tk=False)
    else:
        L = luoi.luoi_o(im.width, im.height, 2, 2, ten=slot)
    PX = np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1)
    V = to_rig(PX)
    if mot_xuong is None and hoa is not None:
        goc = trong_so_goc(V, a0s, ten, Wi)
        fx_ = np.clip((HOA_X[0] - PX[:, 0]) / (HOA_X[0] - HOA_X[1]), 0, 1)
        fy_ = np.clip((PX[:, 1] - HOA_Y[0]) / (HOA_Y[1] - HOA_Y[0]), 0, 1)
        f = (fx_ * fx_ * (3 - 2 * fx_)) * (fy_ * fy_ * (3 - 2 * fy_))
        rows = []
        for i, r in enumerate(goc):
            w = {hoa: 1.0 - f[i]}
            for bn, _, _, ww in r:
                w[bn] = w.get(bn, 0.0) + f[i] * ww
            rows.append([(bn, 0.0, 0.0, ww) for bn, ww in w.items() if ww > 1e-4])
        rows = lam_muot(rows, V, L.tris, Wi, 4)
    elif mot_xuong is None:
        rows = trong_so_goc(V, a0s, ten, Wi)
        if MUOT.get(slot, 0) > 0:
            rows = lam_muot(rows, V, L.tris, Wi, MUOT[slot])
        if slot in KEO:
            # đỉnh cổ + họng (khuất sau đầu / sát dưới hàm) bám dần theo xương đầu: khi đầu ngẩng, cúi mạnh họng kéo theo hàm, không hở
            # khe nền dưới cằm (soi skill 0,85–1,20, appear 0,85, walk). Hoà SAU khi làm mịn, trọng số tính lại kiểu LBS.
            bk, fkeo = KEO[slot]
            f = fkeo(PX)
            moi = []
            for i, r in enumerate(rows):
                w = {bn: (1.0 - f[i]) * ww for bn, _, _, ww in r}
                w[bk] = w.get(bk, 0.0) + f[i]
                hang = []
                for bn, ww in w.items():
                    if ww < 1e-3:
                        continue
                    lp = np.linalg.solve(Wi[bn], np.array([V[i, 0], V[i, 1], 1.0]))
                    hang.append((bn, float(lp[0]), float(lp[1]), ww))
                t2 = sum(q[3] for q in hang) or 1.0
                moi.append([(a_, b_, c_, d_ / t2) for a_, b_, c_, d_ in hang])
            rows = lam_muot(moi, V, L.tris, Wi, 3)
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
    Vb = np.concatenate([np.array(by0[s]["xy"], float).reshape(-1, 2) for s in THAN])
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

    def them(ten_x, cha, p_rig, rot_tg=0.0):
        """xương thêm, con của `cha`, đặt ở điểm thế giới idle 0 p_rig, trục x nghiêng rot_tg (độ, thế giới) ở idle 0."""
        sk.xuong(ten_x, cha, 0.0, 0.0)
        Ml = np.linalg.solve(Wi[cha], np.array([p_rig[0], p_rig[1], 1.0]))
        bx = sk.bones[sk.bi[ten_x]]
        bx["x"], bx["y"] = float(Ml[0]), float(Ml[1])
        bx["rot"] = -_goc(Wi[cha]) + rot_tg

    # đầu vuốt trước gần (chỗ phóng lưỡi cát) / xa: đáy giữa hộp vuốt của họ
    _, _, to_px = tf()
    hop = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))["hop"]
    for ten_x, cha, sl in (("mieng", "bone2", ("zhuazi_1", "zhuazi_2", "zhuazi_3")), ("vuot_xa", "bone44", ("zhuazi_10", "zhuazi_11", "zhuazi_12"))):
        bxs = np.array([hop[s] for s in sl], float)
        px = np.array([[(bxs[:, 0].min() + bxs[:, 2].max()) / 2, bxs[:, 3].max() - 8]])
        them(ten_x, cha, to_rig(px)[0])
    # ba phiến lưng: xương con của xương thân có trọng số lớn nhất ở gốc phiến (đáy giữa hộp phiến), trục x chĩa lên
    body_a0 = [by0[s] for s in THAN]
    cha_phien = {}
    for ten_x, ph in (("pl_a", "pa"), ("pl_b", "pb"), ("pl_c", "pc")):
        x0, y0, x1, y1 = DATJ[ph]["hop"]
        goc_px = np.array([[(x0 + x1) / 2, y1 - 10]], float)
        p = to_rig(goc_px)[0]
        r = trong_so_goc(np.array([p]), body_a0, ten, Wi)[0]
        cha = max(r, key=lambda q: q[3])[0]
        cha_phien[ten_x] = cha
        them(ten_x, cha, p, 90.0)
    # hàm dưới: bản lề ở góc miệng = đầu trái của mảnh hàm (cột trái nhất có hình, giữa chiều cao của cột đó), trục x nằm ngang ở idle 0
    hm = np.asarray(Image.open(os.path.join(MANH, "ham.png")).convert("RGBA"))[..., 3] > 128
    hx0, hy0 = DATJ["ham"]["hop"][:2]
    cot = np.flatnonzero(hm.any(0))[:6]
    ys_ = np.flatnonzero(hm[:, cot].any(1))
    ban_le = np.array([[hx0 + cot.mean() + 6.0, hy0 + ys_.mean()]])
    them("ham", "bone6", to_rig(ban_le)[0])
    sk.W0 = sk.the_gioi()
    Wb = dict(Wi)
    for x in ("mieng", "vuot_xa", "ham") + PHIEN:
        b0 = sk.bones[sk.bi[x]]
        Wb[x] = Wi[b0["parent"]] @ khung.mat(b0["x"], b0["y"], b0["rot"])
    tong = [0, 0]
    for s, hinhs, nguon in SLOT:
        sk.slot(s, "move", hinhs[0])
        for h in hinhs:
            if isinstance(nguon, tuple) and nguon[0] == "hoa":
                L = gan_manh(sk, s, h, [by0[x] for x in nguon[1]], ten, Wi, hoa=nguon[2])
            elif isinstance(nguon, tuple):
                L = gan_manh(sk, s, h, None, ten, Wb, mot_xuong=(nguon[1], Wb[nguon[1]]))
            else:
                L = gan_manh(sk, s, h, [by0[x] for x in nguon], ten, Wi)
            tong[0] += L.n
            tong[1] += len(L.tris)
    for e, m in (("trung", "khung trúng"), ("lao", "attack: bật lao tới (VFX bụi sau chân)"),
                 ("chem1", "cast: lưỡi cát 1 rời vuốt"), ("chem2", "cast: lưỡi cát 2 rời vuốt"),
                 ("gong", "skill: chồm đứng gồng giơ vuốt (VFX cát hút về vuốt)"), ("nen", "skill: giáng xuống nện đất (VFX vòng bụi, vết nứt)"),
                 ("cot1", "skill: cột sa thạch 1 trồi"), ("cot2", "skill: cột sa thạch 2 trồi (= trúng)"),
                 ("dap", "appear: đáp đất (VFX bụi)"), ("gam", "appear: ngẩng đầu gầm"), ("vay", "idle: vẫy đuôi tíu tít"),
                 ("nga", "die: ngã chạm đất (VFX bụi)")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; đáy y = {y_day:.1f}, tâm thân "
          f"({tam[0]:.1f}, {tam[1]:.1f}); phiến bám {cha_phien}")
    return sk, dict(IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], y_day=y_day, tam=tam, S=S, Wi=Wi)


# ---------------------------------------------------------------- chuyển động của họ
def chuyen_dong(info):
    S, ten, goc0 = info["S"], info["ten"], info["goc0"]
    out = {}
    i_mat = info["slots"].index("yanjing_0")
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
        mat = ["mat_nham" if F["n"][i_mat] == "yanjing_0" else "mat" for F in fr]
        out[clip] = (float(v["dur"]), res, len(fr), mat)
    return out


# ---------------------------------------------------------------- mốc giờ
T_ATK, LAO, D_ATTACK = 0.40, 0.48, 1.00                  # attack: vồ chém trúng; lao tới (× chiều cao) ở khung trúng; dài
T_CHEM1, T_CHEM2, D_CAST = 0.40, 0.47, 1.15              # cast: hai lưỡi cát rời vuốt (lúc quét); dài
T_GONG, T_NEN, T_COT1, T_COT2, D_SKILL = 0.60, 1.60, 1.76, 1.96, 2.30   # skill
T_TRUNG_SKILL = T_COT2
T_ROI_A, T_DAP_A, T_GAM_A, D_APPEAR = 0.10, 0.40, 0.72, 1.60
T_VAY0, T_VAY1 = 2.20, 3.30                              # idle: vẫy đuôi + nghiêng đầu


def lam_clip(sk, info, cao=420.0):
    CD = chuyen_dong(info)
    y_day = info["y_day"]

    def goc_tong(P, x):
        """góc thế giới của x tính bằng TỔNG góc riêng dọc chuỗi cha (không gói ±180°: liền mạch theo thời gian)."""
        s = 0.0
        while x:
            b = sk.bones[sk.bi[x]]
            s += b.get("rot", 0.0) + P.t.get(x, khung.ZERO)[2]
            x = b["parent"]
        return s

    def bu_ke_thua(P):
        """xương inherit = 2: góc thế giới = góc riêng (không ăn góc cha). Bù lần lượt từ cha xuống con (chuỗi cổ, chuỗi đuôi). Góc cha lấy
        đúng từ ma trận (_goc) nhưng mở gói về gần tổng góc chuỗi cha: atan2 gói ±180° làm góc riêng nhảy 360° giữa hai khung khi đuôi đi
        qua 180° (walk 0,60), khoá nướng nội suy xuyên qua cú nhảy đó → đuôi lật một khung."""
        for b in KE_THUA_2:
            W = sk.the_gioi(P)
            cha = sk.bones[sk.bi[b]]["parent"]
            c = _goc(W[cha])
            s = goc_tong(P, cha)
            c += 360.0 * round((s - c) / 360.0)
            P.rot(b, -c)

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
        """một dáng để hoà (pha): góc đưa về (−180°, 180°]."""
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

    def phien(P, t, bien=1.0, chu_ky=2.0):
        """ba phiến lưng nhấp nhô so le (phiến trước trước, phiến sau trễ)."""
        for j, b in enumerate(PHIEN):
            P.rot(b, bien * (2.0 + 0.4 * j) * song_(t, chu_ky, 0.07 * j))

    HA = 32.0                                                     # góc há tối đa của hàm dưới (độ)

    def ha(P, w):
        """há miệng mức w (0..1+): hàm dưới quay xuống quanh bản lề góc miệng."""
        if abs(w) > 1e-4:
            P.rot("ham", -HA * w)

    def duoi_song(P, t, bien=1.0, chu_ky=4.0, tre0=0.12):
        for j, b in enumerate(DUOI):
            P.rot(b, bien * (1.5 + 1.0 * j) * song_(t, chu_ky, tre0 + 0.10 * j))

    # ------------------------------------------------ idle: MỀM, sóng lệch pha + trò vẫy đuôi, nghiêng đầu tò mò
    def f_idle(t, P):
        dat(P, "idle_01", 0.0)
        th = song_(t, 2.0)
        P.scale("shenti_2", 1.0, 1.0 + 0.02 * th)                 # ngực nở / xẹp
        P.move("day", 0.0, -2.0 * th)
        P.rot("bone4", 0.8 * song_(t, 2.0, 0.05))
        P.rot("bone5", 0.8 * song_(t, 2.0, 0.08))
        P.rot("bone6", 1.4 * song_(t, 2.0, 0.12))
        phien(P, t, 1.0, 2.0)
        duoi_song(P, t, 1.0, 4.0)
        if T_VAY0 < t < T_VAY1 + 0.3:
            vay = hoat.cv(t, [(T_VAY0, 0.0), (T_VAY0 + 0.15, 1.0, "out"), (T_VAY1 - 0.2, 1.0), (T_VAY1 + 0.2, 0.0, "io")])
            for j, b in enumerate(DUOI):                              # đuôi vẫy tíu tít (4 Hz), ngọn trễ, biên độ lớn dần ra ngọn
                P.rot(b, vay * (5.0 + 3.0 * j) * math.sin(2 * math.pi * 4.0 * (t - T_VAY0 - 0.04 * j)))
            ng = hoat.cv(t, [(T_VAY0 + 0.1, 0.0), (T_VAY0 + 0.45, 1.0, "io"), (T_VAY1 - 0.15, 1.0), (T_VAY1 + 0.25, 0.0, "io")])
            P.rot("bone6", 9.0 * ng)                                  # nghiêng đầu tò mò
            P.rot("bone23", 3.0 * ng)
            P.move("day", 0.0, 4.0 * abs(math.sin(2 * math.pi * 2.0 * (t - T_VAY0))) * vay)   # nhún nhảy theo nhịp vẫy
            for j, b in enumerate(PHIEN):
                P.rot(b, 2.5 * vay * math.sin(2 * math.pi * 4.0 * (t - T_VAY0 - 0.05 - 0.03 * j)))
        if T_VAY0 + 0.60 < t < T_VAY0 + 0.76 or 0.9 < t < 1.04:
            P.att["mat"] = "mat_nham"
        if 1.20 < t < 1.95:                                          # ngáp nhỏ một lần: ngẩng nhẹ, há, khép
            ng_ = hoat.cv(t, [(1.20, 0.0), (1.48, 1.0, "out"), (1.66, 1.0), (1.95, 0.0, "io")])
            ha(P, 0.55 * ng_)
            P.rot("bone6", 4.0 * ng_)

    def f_walk(t, P):
        dat(P, "run_01", t, True)
        phien(P, t, 0.8, CD["run_01"][0])

    def f_hit(t, P):
        dat(P, "hit_01", t)
        k = math.exp(-max(0.0, t - 0.07) / 0.12)
        ha(P, 0.35 * k * min(1.0, t / 0.07))
        for b in PHIEN:
            P.rot(b, -7.0 * k * math.sin(min(1.0, t / 0.07) * math.pi * 0.5))

    # ------------------------------------------------ attack: ngửa lấy đà, vồ chém vuốt, lao tới
    def f_attack(t, P):
        dat(P, "skill_01_01", t)
        lao = hoat.cv(t, [(0.0, 0.0), (0.28, -0.04, "io"), (T_ATK, LAO, "in"), (0.64, LAO), (0.95, 0.0, "io")])
        P.move("move", cao * lao, 0.0)
        ha(P, hoat.cv(t, [(0.0, 0.0), (0.12, 0.2, "io"), (T_ATK - 0.06, 0.95, "out"), (T_ATK, 0.15, "in"), (T_ATK + 0.12, 0.3, "out"),
                          (0.88, 0.0, "io")]))
        k = math.exp(-((t - (T_ATK + 0.02)) / 0.05) ** 2)
        P.scale("day", 1 + 0.07 * k, 1 - 0.06 * k)
        phien(P, t, 0.7)
        if t > T_ATK:
            r = math.exp(-(t - T_ATK) / 0.10) * math.sin((t - T_ATK) * 2 * math.pi / 0.12)
            for j, b in enumerate(PHIEN):
                P.rot(b, (5.0 + j) * r)

    # ------------------------------------------------ cast: giơ vuốt gần, quét chém xuống, giữ dáng (hai lưỡi cát VFX)
    M_CAST = [(0.0, 0.0), (T_CHEM1, 0.40), (0.82, 0.62, "out"), (D_CAST, 1.0, "io")]

    def f_cast(t, P):
        dat(P, "skill_01_03", tmap(t, M_CAST))
        ha(P, hoat.cv(t, [(0.0, 0.0), (0.30, 0.15, "io"), (T_CHEM1, 0.6, "out"), (0.70, 0.45), (D_CAST - 0.05, 0.0, "io")]))
        k = math.exp(-((t - (T_CHEM1 + 0.02)) / 0.05) ** 2)
        P.scale("day", 1 + 0.06 * k, 1 - 0.05 * k)
        if T_CHEM1 < t < 0.80:                                      # giữ dáng quét: hai dáng lệch đổi nhau, nhỏ dần
            r = hoat.rung(t, T_CHEM1, 0.80, 2) * (1.0 - (t - T_CHEM1) / 0.4)
            P.rot("bone6", 1.6 * r)
        phien(P, t, 0.6)
        if t > T_CHEM1:
            r = math.exp(-(t - T_CHEM1) / 0.10) * math.sin((t - T_CHEM1) * 2 * math.pi / 0.12)
            for j, b in enumerate(PHIEN):
                P.rot(b, (4.0 + j) * r)

    # ------------------------------------------------ skill: thu người, chồm đứng gồng, giáng xuống nện, giữ dáng nện rung
    M_SKILL = [(0.0, 0.0), (T_NEN, 1.60), (2.02, 1.66, "out"), (D_SKILL, 1.8333, "io")]

    def f_skill(t, P):
        dat(P, "skill_03", tmap(t, M_SKILL))
        ha(P, hoat.cv(t, [(0.0, 0.0), (0.50, 0.1, "io"), (0.72, 1.0, "out"), (1.38, 0.9), (T_NEN - 0.04, 0.1, "in"),
                          (T_COT2, 0.55, "out"), (2.04, 0.45), (D_SKILL - 0.04, 0.0, "io")]))
        if 0.72 < t < 1.38:                                         # gầm: hàm rung
            P.rot("ham", -3.0 * hoat.rung(t, 0.72, 1.38, 2))
        if T_GONG < t < 1.42:                                       # gồng: hai dáng lệch 2° đổi nhau
            r = hoat.rung(t, T_GONG + 0.1, 1.42, 2)
            P.rot("bone6", 2.0 * r)
            P.rot("bone13", 1.5 * r)
        # lúc chồm đứng clip gốc ngửa đầu tới ~90° (mặt chĩa thẳng lên, đọc như đầu bị ngửa ra sau): bớt còn ~55°, mặt chéo lên trời gầm
        ngua = hoat.cv(t, [(0.50, 0.0), (0.68, 1.0, "out"), (1.36, 1.0), (1.55, 0.0, "io")])
        P.rot("bone6", -35.0 * ngua)
        P.rot("bone23", -8.0 * ngua)
        # clip gốc để đầu ngửa lên lúc giáng xuống: cúi đầu theo cú nện (đầu, cổ của họ là xương inherit 2: góc tuyệt đối)
        cui = hoat.cv(t, [(1.38, 0.0), (T_NEN, 1.0, "in"), (2.02, 0.75), (D_SKILL - 0.04, 0.0, "io")])
        P.rot("bone6", -30.0 * cui)
        P.rot("bone23", -12.0 * cui)
        P.rot("bone5", -6.0 * cui)
        if t > T_NEN:                                                # chạm đất: bẹp rồi nảy, phiến lạch cạch
            b = math.exp(-(t - T_NEN) / 0.08) * math.sin((t - T_NEN) * 2 * math.pi / 0.22)
            P.scale("day", 1 + 0.10 * b, 1 - 0.12 * b)
            for j, b_ in enumerate(PHIEN):
                P.rot(b_, 6.0 * math.exp(-(t - T_NEN) / 0.12) * math.sin((t - T_NEN - 0.02 * j) * 2 * math.pi / 0.12))
        for tc in (T_COT1, T_COT2):                                  # mỗi cột trồi: rung nhẹ
            if tc < t < tc + 0.12:
                P.move("day", 0.0, 2.5 * hoat.rung(t, tc, tc + 0.12, 2))
        phien(P, t, 0.5)

    # ------------------------------------------------ appear: rơi từ trên xuống, đáp phịch, ngẩng đầu gầm, về đứng
    P_GAM = dang("skill_01_02", 0.55)                               # dáng ngẩng đầu lên trời
    P_NHAY = dang("skill_03", 0.75)                                 # dáng chồm co tay (lúc rơi)

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
            pha(P, P_NHAY, 0.7 * (1.0 - ease(u, "in")))
            return
        b = math.exp(-(t - T_DAP_A) / 0.09) * math.sin((t - T_DAP_A) * 2 * math.pi / 0.24)
        P.scale("day", 1 + 0.14 * b, 1 - 0.16 * b)
        gam = hoat.cv(t, [(T_DAP_A, 0.0), (T_DAP_A + 0.10, 0.0), (T_GAM_A, 1.0, "out"), (1.16, 1.0), (D_APPEAR - 0.06, 0.0, "io")])
        pha(P, P_GAM, gam)
        ha(P, 1.05 * gam)
        if T_GAM_A < t < 1.16:
            P.rot("ham", -3.0 * hoat.rung(t, T_GAM_A, 1.16, 2))
        P.rot("bone6", -62.0 * gam)                                 # dáng gốc ngửa đầu 92°: bớt còn ~45°, mặt chéo lên trời gầm
        P.rot("bone23", -14.0 * gam)
        if T_GAM_A < t < 1.16:
            r = hoat.rung(t, T_GAM_A, 1.16, 2)
            P.rot("bone6", 2.0 * r)
        for j, b_ in enumerate(PHIEN):                              # phiến lạch cạch lúc chạm đất, dựng lúc gầm
            P.rot(b_, 6.0 * gam + 5.0 * math.exp(-(t - T_DAP_A) / 0.1) * math.sin((t - T_DAP_A - 0.02 * j) * 2 * math.pi / 0.12))
        duoi_song(P, t, 1.5 * gam, 0.6, 0.0)

    # ------------------------------------------------ die: die_01 + mờ
    D_DIE = CD["die_01"][0]

    def f_die(t, P):
        dat(P, "die_01", t)
        ha(P, hoat.cv(t, [(0.0, 0.0), (0.12, 0.6, "out"), (0.60, 0.5), (0.80, 0.35, "io")]))
        dam(P, float(np.clip(1.0 - (t - D_DIE) / (TAN - 0.1), 0.0, 1.0)))

    clips = [
        Clip("appear", D_APPEAR, boc(f_appear), ev=[(T_DAP_A, "dap", ""), (T_GAM_A, "gam", "")]),
        Clip("idle", 4.0, boc(f_idle), loop=True, ev=[(T_VAY0 + 0.05, "vay", "")]),
        Clip("walk", CD["run_01"][0], boc(f_walk), loop=True),
        Clip("attack", D_ATTACK, boc(f_attack), ev=[(0.30, "lao", ""), (T_ATK, "trung", "")], trung=T_ATK),
        Clip("cast", D_CAST, boc(f_cast), ev=[(T_CHEM1, "chem1", ""), (T_CHEM2, "chem2", ""), (T_CHEM1, "trung", "")], trung=T_CHEM1),
        Clip("skill", D_SKILL, boc(f_skill), ev=[(T_GONG, "gong", ""), (T_NEN, "nen", ""), (T_COT1, "cot1", ""), (T_COT2, "cot2", ""),
                                                  (T_TRUNG_SKILL, "trung", "")], trung=T_TRUNG_SKILL),
        Clip("hit", CD["hit_01"][0], boc(f_hit)),
        Clip("die", D_DIE + TAN, boc(f_die), ev=[(0.70, "nga", "")]),
    ]
    return clips


def dung_het(far_xy=None):
    """dựng đủ rig + clip (cho bản xem trước tho5_fx_rong_cat_non.py): trả (sk, info, clips, cao)."""
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0) - info["y_day"]
    clips = lam_clip(sk, info, cao)
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
                    if da > 35.0:
                        xau.append(f"{i / 30:.2f}s {b} xoay {da:.0f}°")
            for s, b in (("than", "shenti_2"), ("dau", "bone6"), ("duoi", "bone22"), ("tay_gan", "bone2"), ("tay_xa", "bone44"),
                         ("chan_gan", "bone17"), ("chan_xa", "bone43")):
                for i in range(1, len(fr)):
                    d = float(np.hypot(*(Wl[i][b][:2, 2] - Wl[i - 1][b][:2, 2])))
                    if d > 0.22 * cao:
                        xau.append(f"{i / 30:.2f}s {s} dời {d / cao:.2f} cao/khung")
            print(f"{c.ten}: {len(fr)} khung" + ("" if not xau else " | " + "; ".join(xau[:14]) + (" ..." if len(xau) > 14 else "")))
        return
    if a and a[0] == "tu_soi":
        # TỜ SOI tổng: concept duyệt cạnh idle 0, rồi mỗi dáng cực trị của mọi clip phóng to năm chỗ nối (đầu–cổ, hàm, vai, hông, gốc đuôi)
        from PIL import ImageFont
        try:
            fnt = ImageFont.truetype("arial.ttf", 18)
        except Exception:
            fnt = None
        frs = {c.ten: hoat.nuong(sk, c) for c in clips}
        R = 0.20 * cao
        CHO = [("dau-co", lambda W: 0.5 * (W["bone5"][:2, 2] + W["bone6"][:2, 2])), ("ham", lambda W: W["ham"][:2, 2]),
               ("vai", lambda W: W["bone65"][:2, 2]), ("hong", lambda W: W["bone18"][:2, 2]), ("goc duoi", lambda W: W["bone19"][:2, 2])]
        DANG = [("idle", 0.0), ("idle", 1.55), ("idle", 2.75), ("walk", 0.27), ("walk", 0.6), ("attack", 0.30), ("attack", 0.36),
                ("attack", 0.40), ("attack", 0.55), ("cast", 0.30), ("cast", 0.42), ("cast", 0.7), ("skill", 0.40), ("skill", 0.85),
                ("skill", 1.20), ("skill", 1.62), ("skill", 1.96), ("appear", 0.45), ("appear", 0.85), ("appear", 1.0), ("hit", 0.10),
                ("die", 0.30), ("die", 0.60), ("die", 1.0)]
        sc = 1.0
        o_w = int(2 * R * sc)
        hang = []
        Ccon = Image.open(os.path.join(G.TAI, "L1_duyet.png")).convert("RGB")
        Bx = soi._union([ve0.bao(idle0)], 0.04)
        im0 = ve0.ve(idle0, Bx, 0.62, bg=(150, 150, 150), ss=2).convert("RGB")
        Cc = Ccon.resize((int(Ccon.width * im0.height / Ccon.height * 0.9), int(im0.height * 0.9)))
        h0 = Image.new("RGB", (Cc.width + im0.width + 20, im0.height + 26), (150, 150, 150))
        h0.paste(Cc, (0, 26))
        h0.paste(im0, (Cc.width + 20, 26))
        ImageDraw.Draw(h0).text((6, 4), "concept duyet | idle 0 (rig)", fill=(255, 255, 255), font=fnt)
        hang.append(h0)
        for c, t in DANG:
            fr = frs[c]
            P = fr[min(len(fr) - 1, int(round(t * 30)))]
            W = sk.the_gioi(P)
            row = Image.new("RGB", (5 * (o_w + 6) + 150, o_w), (150, 150, 150))
            ImageDraw.Draw(row).text((6, 6), f"{c} {t:.2f}", fill=(255, 255, 255), font=fnt)
            for j, (ten_c, f) in enumerate(CHO):
                p = f(W)
                im = ve0.ve(P, (p[0] - R, p[1] - R, p[0] + R, p[1] + R), sc, bg=(150, 150, 150), ss=2).convert("RGB")
                im = im.resize((o_w, o_w))
                ImageDraw.Draw(im).text((4, 2), ten_c, fill=(255, 255, 0), font=fnt)
                row.paste(im, (150 + j * (o_w + 6), 0))
            hang.append(row)
        Wt = max(h.width for h in hang)
        out = Image.new("RGB", (Wt, sum(h.height + 6 for h in hang)), (110, 110, 110))
        y = 0
        for h in hang:
            out.paste(h, (0, y))
            y += h.height + 6
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, "_tu_soi.jpg")
        out.save(pth, quality=86)
        print(pth, out.size)
        return
    if a and a[0] == "diem":
        HS = cao
        x0 = (ve0.bao(idle0)[0] + ve0.bao(idle0)[2]) / 2
        for c, xs, ts in (("cast", ("mieng",), [0.30, T_CHEM1, T_CHEM2, 0.55]), ("attack", ("mieng", "vuot_xa", "bone6"), [T_ATK]),
                          ("skill", ("mieng", "vuot_xa"), list(np.arange(0.6, 1.71, 0.1)) + [T_COT1, T_COT2])):
            cl = [x for x in clips if x.ten == c][0]
            fr = hoat.nuong(sk, cl)
            for xx in xs:
                out = []
                for t in ts:
                    W = sk.the_gioi(fr[min(len(fr) - 1, int(round(t * 30)))])
                    p = W[xx][:2, 2]
                    out.append(f"{t:.2f}: ({(p[0] - x0) / HS:.3f}, {(p[1] - info['y_day']) / HS:.3f})")
                print(f"{c}.{xx}: " + "; ".join(out))
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
            ImageDraw.Draw(im).text((6, 4), f"{ts[i]:.2f}", fill=(255, 255, 255))
            if out is None:
                out = Image.new("RGB", (im.width * cot, im.height * hang), (150, 150, 150))
            out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
        os.makedirs(RA, exist_ok=True)
        pth = os.path.join(RA, f"soi_{a[1]}.png")
        out.save(pth)
        print(pth, out.size)
        return
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de="Sa Long dạng 1 (rong_cat_non): tướng ải 15 đảo Thổ, dạng non", dang=1, so_dang=2,
                  dung_yen=("cast", "skill"), ma_goc=None, khop_idle=0.2, cao=cao, impact=IMPACT,
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.3, tran_mb=0.5, span=3.6)


if __name__ == "__main__":
    main(sys.argv[1:])
