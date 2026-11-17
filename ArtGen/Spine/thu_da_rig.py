# -*- coding: utf-8 -*-
"""Cóc tê giác pha lê (thu_da; tướng 3 đảo Thổ, ải 10): hình của mình chạy trên ĐÚNG rig của con gốc monster_3525. Ghi chú:
inbox/thu_da_ghichu.md. Cách làm như quang_sat_rig.py (skill pokiclash-spine-rig mục 00):
- XƯƠNG: đủ mọi xương của họ (bốn chân có IK: mẫu khung `l` của runtime đã nướng IK vào biến đổi riêng), thêm `move` (cú lao; game nắn
  quãng ở clip khai lao), `day` (đáy thân, ở mặt đất: bẹp / phình, nhảy), `tam` (tâm thân: lật, nghiêng; cha của `bone`), `bong` (quả cầu
  cuộn tròn, ở tâm thân), `mieng` (chỗ nhả tảng đá của chiêu mana, trục x chĩa hướng phun).
- MẢNH: ảnh của mình "đúng chỗ, đúng cỡ" (thu_da_manh.py → inbox/thu_da_1/manh/, px concept, qua phép căn concept → con gốc); mỗi slot là lưới
  phủ hình, mỗi đỉnh biến dạng ĐÚNG như điểm tương ứng trên lưới cùng slot của họ (trong_so_goc: trọng số + điểm gắn riêng từng xương; điểm
  ngoài lưới kéo theo cạnh gần nhất). Sừng mũi là mảnh thêm cứng trên xương đầu (bone12). Bỏ (ẩn) face21, face1, mt2, beijiao2, eyes3..5,
  shadow; slot xz (quả cầu mờ của họ) thay bằng quả cầu của mình trên xương `bong`.
- CHUYỂN ĐỘNG (tho5_anim.py, người dùng duyệt "làm đi" 2026-11-17):
    idle   = idle_01 (ba nhịp thở 1,33 s) + túi họng phập phồng + trò riêng: nhấc chân trước gần DẬM xuống, khịt mũi;
    walk   = run_01; hit = hit_01 (mắt nhắm như họ);
    attack = skill_01_1: chồm nửa thân trước, nhích tới, GIÁNG SỪNG / cằm xuống đất (trúng ~0,47 s);
    cast   = skill_02_1 kéo dài: há hàm, tụ (VFX hút đá vào miệng), PHUN TẢNG ĐÁ (sự kiện phun, đạn do VFX từ `mieng`), giật đầu;
    skill  = cuộn tròn (skill_03 đầu) → QUẢ CẦU xoay tại chỗ gồng → lăn bật tới đối thủ (khai lao: game nắn quãng) NỆN → nảy về → bung ra
             đáp đất (skill_03 đoạn cuối);
    appear = quả cầu lăn vào từ phía sau, nảy một lần, bung ra đáp đất (skill_03 đoạn cuối);
    die    = die_01 đầu (giật, nhắm mắt) → LẬT NGỬA, pha lê rụng rơi xuống đất, bốn chân đạp vài cái → mờ.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/thu_da_rig.py        → inbox/thu_da_1/rig/
    py -3 -I ArtGen/Spine/thu_da_rig.py soi <clip> <giây,giây,...|n=12|t0:t1:n> [tỉ lệ]    → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/thu_da_rig.py kiem                                              đo góc nhảy, bước dời giữa hai khung
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "mo_xe"))
from quai import anh, khung, hoat, xuat, soi, luoi, trongso  # noqa: E402
from quai.hoat import Clip  # noqa: E402
import thu_da_manh as MN  # noqa: E402
from hoa_ho_rig import ease, tmap, _goc  # noqa: E402

G = MN.G
TEN_RIG = "thu_da_1"
D_PX = float(os.environ.get("TD_DPX", "0.62"))          # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~730 đơn vị)
MANH = MN.MANH
RA = os.environ.get("TD_RA") or os.path.join(G.BASE, "rig")
TAN = 0.40
FPS = 30.0
IMPACT = {"attack": (0.08, 0.5, 0.12), "cast": (0.09, 0.55, 0.12), "skill": (0.18, 1.0, 0.24, "#fff6c94d")}

# slot của họ (thứ tự vẽ idle, sau → trước) mình dùng; mảnh thêm chèn theo SAU_SLOT
BO = {"shadow", "face21", "face1", "mt2", "beijiao2", "eyes3", "eyes4", "eyes5", "xz"}
SAU_SLOT = {"sung": "head1"}                                  # sừng mũi vẽ ngay sau đầu
XUONG_THEM = {"sung": "bone12"}                              # mảnh thêm cứng trên xương này
PHA_LE = ("beijiao4", "hair1", "jiao3", "beijiao3", "jiao1", "beijiao1", "jiao2")
PL_XUONG = {"beijiao4": "bone28", "hair1": "bone27", "jiao3": "bone26", "beijiao3": "bone32", "jiao1": "bone31", "beijiao1": "bone29",
            "jiao2": "bone30"}                                # xương gai của họ (slot của mình bám move, lưới bám xương này 100 %)
CHAN = {"lh": ("bone4", "bone5", "bone6", "bone7"), "rh": ("bone8", "bone9", "bone10", "bone11"),
        "ll": ("bone15", "bone16", "bone17", "bone18"), "rl": ("bone19", "bone20", "bone21", "bone22")}


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


def anh_manh(ten):
    """ảnh mảnh của mình thu về D_PX px / đơn vị + hộp (px concept) + hệ số thu (px atlas / px concept)."""
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    T = MN.tf()
    g = Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA")
    kq = D_PX * T["a"] / T["s"]
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), DATJ[ten]["hop"], kq


def trong_so_goc(V, a0, ten, Wi):
    """(như quang_sat_rig.trong_so_goc) mỗi điểm V biến dạng như điểm tương ứng trên lưới a0 của họ."""
    Q = np.array(a0["xy"], float).reshape(-1, 2)
    tr = np.array(a0["tris"]).reshape(-1, 3)
    if a0.get("w"):
        Wg = [{ten[k]: w for k, w in ws if w > 0.002} for ws in a0["w"]]
    else:                                                    # lưới một xương không trọng số
        bn = ten[a0["bone"]] if isinstance(a0["bone"], int) else a0["bone"]
        Wg = [{bn: 1.0}] * len(Q)
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
            i = int(ok[0])
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


PHA_TRONG_SO = {}            # slot → (mảnh kia, bán kính pha (đơn vị), mức pha tối đa, lưới của họ của mảnh kia); điền trong dung()
DA_GIAC = {}                 # mảnh → đa giác hình bóng (thế giới idle 0)
# NHÓM CÙNG BỀ MẶT: mọi mảnh trong nhóm dùng CHUNG một trường trọng số theo vị trí (pha các lưới của họ theo khoảng cách tới từng mảnh), nên
# chỗ hai mảnh chồng nhau biến dạng y hệt nhau: chỉ thấy một đường viền, không dải hở, không viền đôi (người dùng chê ở tatu 2026-11-17).
# Hàm (mt1) đứng riêng để há; bụng sát hàm pha thêm về hàm (PHA_TRONG_SO).
NHOM_TRON = [("head1", "1chest", "hip1"), ("chest3", "chest1", "body1"), ("lhand3", "lhand1", "lhand2"), ("rhand2", "rhand1", "rhand3"),
             ("lleg1", "lleg2"), ("rleg1", "rleg2")]
A0_NHOM = {}                 # mảnh → lưới của họ cùng slot (idle 0)
SIGMA = 18.0                 # độ rộng vùng pha giữa hai mảnh kề (đơn vị rig)


def truong_chung(V, nhom, ten, Wi):
    """trọng số của điểm V = Σ φ_k(V) · (trọng số theo lưới của họ của mảnh k), φ_k = exp(−(d_k / SIGMA)²) chuẩn hoá, d_k = khoảng cách
    tới hình bóng mảnh k (0 nếu ở trong). Chỉ phụ thuộc vị trí → hai mảnh chồng nhau ở cùng điểm có cùng trọng số."""
    R = {k: trong_so_goc(V, A0_NHOM[k], ten, Wi) for k in nhom}
    poly = {k: DA_GIAC[k].reshape(-1, 1, 2).astype(np.float32) for k in nhom}
    out = []
    for i, p in enumerate(V):
        d = {k: max(0.0, -cv2.pointPolygonTest(poly[k], (float(p[0]), float(p[1])), True)) for k in nhom}
        ph = {k: math.exp(-(d[k] / SIGMA) ** 2) for k in nhom}
        tot_ph = sum(ph.values())
        if tot_ph < 1e-9:                                   # xa mọi mảnh (không xảy ra): lấy mảnh gần nhất
            kmin = min(d, key=d.get)
            ph = {k: 1.0 if k == kmin else 0.0 for k in nhom}
            tot_ph = 1.0
        acc = {}
        for k in nhom:
            f = ph[k] / tot_ph
            if f < 1e-4:
                continue
            for n, x, y, w in R[k][i]:
                e = acc.setdefault(n, [0.0, 0.0, 0.0])
                e[0] += w * f
                e[1] += w * f * x
                e[2] += w * f * y
        tot = sum(e[0] for e in acc.values()) or 1.0
        out.append([(n, e[1] / e[0], e[2] / e[0], e[0] / tot) for n, e in acc.items() if e[0] > 1e-6])
    return out


def da_giac_manh(ten):
    """đường bao hình bóng của mảnh (px concept → thế giới idle 0)."""
    import cv2
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    x0, y0, _, _ = DATJ[ten]["hop"]
    al = np.asarray(Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA"))[..., 3] > 100
    cs, _ = cv2.findContours(al.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea).reshape(-1, 2).astype(float) + np.array([x0, y0])
    return MN.tf()["c2w"](c)


def gan_manh(sk, slot, ten_anh, a0, ten, Wi, xuong_cung=None, dat_lai=None, w_the_gioi=False):
    """mảnh của mình thành lưới đặt đúng chỗ (px concept → thế giới qua phép căn). a0: hình của họ cùng slot (lưới nhiều xương → lưới phủ hình
    + trong_so_goc); xuong_cung: mảnh thêm cứng trên một xương. dat_lai: (tâm thế giới, cỡ thế giới) đặt mảnh không có trên concept vào chỗ
    part gốc (lòng miệng, quả cầu)."""
    im, (x0, y0, x1, y1), kq = anh_manh(ten_anh)
    if ten_anh not in sk.images:
        sk.anh(ten_anh, im)
    im = sk.images[ten_anh]
    T = MN.tf()
    nhieu = xuong_cung is None and bool(a0.get("tris"))
    L = luoi.luoi_vung(im, buoc_vien=9.0, buoc_trong=15.0, vien=2, ten=slot, in_tk=False) if nhieu else luoi.luoi_o(im.width, im.height, 2, 2,
                                                                                                                   ten=slot)
    if dat_lai is not None:
        c, rong = dat_lai[0], dat_lai[1]
        kx = rong / im.width
        ky = (dat_lai[2] / im.height) if len(dat_lai) > 2 else kx
        V = np.stack([c[0] + (L.pts[:, 0] - im.width / 2) * kx, c[1] - (L.pts[:, 1] - im.height / 2) * ky], 1)
    else:
        Px = np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1)
        V = T["c2w"](Px)
    if nhieu:
        nhom = next((g for g in NHOM_TRON if slot in g and all(k in DA_GIAC and k in A0_NHOM for k in g)), None)
        rows = truong_chung(V, nhom, ten, Wi) if nhom else trong_so_goc(V, a0, ten, Wi)
        if slot in PHA_TRONG_SO and PHA_TRONG_SO[slot][0] in DA_GIAC:
            # đỉnh gần mảnh kia (đầu) pha dần trọng số của lưới mảnh đó: chỗ nối đi theo đầu, khỏi lộ mép lưng khi đầu gật
            khac, R, fmax, a_khac = PHA_TRONG_SO[slot][0], PHA_TRONG_SO[slot][1], PHA_TRONG_SO[slot][2], PHA_TRONG_SO[slot][3]
            poly = DA_GIAC[khac].reshape(-1, 1, 2).astype(np.float32)
            rows_k = trong_so_goc(V, a_khac, ten, Wi)
            out = []
            for p, r0, r1 in zip(V, rows, rows_k):
                d = cv2.pointPolygonTest(poly, (float(p[0]), float(p[1])), True)       # >0 trong mảnh kia
                f = fmax * float(np.clip(1.0 - (-d) / R, 0.0, 1.0)) if d < 0 else fmax
                acc = {}
                for (n, x, y, w), k in [(q, 1 - f) for q in r0] + [(q, f) for q in r1]:
                    if w * k <= 1e-6:
                        continue
                    e = acc.setdefault(n, [0.0, 0.0, 0.0])
                    e[0] += w * k
                    e[1] += w * k * x
                    e[2] += w * k * y
                tot = sum(e[0] for e in acc.values()) or 1.0
                out.append([(n, e[1] / e[0], e[2] / e[0], e[0] / tot) for n, e in acc.items()])
            rows = out
    else:
        b = xuong_cung or (ten[a0["bone"]] if isinstance(a0["bone"], int) else a0["bone"])
        Mb = sk.W0[b] if (dat_lai is not None and not w_the_gioi) or b not in Wi else Wi[b]   # đặt theo dáng gốc → ma trận dáng gốc
        rows = [[(b, *[float(v) for v in np.linalg.solve(Mb, np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
    Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
    sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=Vs)
    sk.atts[slot][ten_anh]["verts"] = rows
    return L, V


def sang_idle0(a, Wc, Wi, ten):
    """hình của họ ghi ở dáng gốc (att_goc) → toạ độ ở dáng idle 0: mỗi đỉnh = Σ w · Wi[b] · Wc[b]⁻¹ · p."""
    Q = np.array(a["xy"], float).reshape(-1, 2)
    out = []
    if not a.get("w"):                                        # lưới một xương không trọng số: cả hình theo xương đó
        n = ten[a["bone"]] if isinstance(a["bone"], int) else a["bone"]
        M = Wi[n] @ np.linalg.inv(Wc[n])
        b = dict(a)
        b["xy"] = [float(v) for q in (M @ np.c_[Q, np.ones(len(Q))].T).T[:, :2] for v in q]
        return b
    for p, ws in zip(Q, a["w"]):
        acc = np.zeros(2)
        tot = 0.0
        for k, w in ws:
            n = ten[k]
            acc += w * (Wi[n] @ np.linalg.solve(Wc[n], np.array([p[0], p[1], 1.0])))[:2]
            tot += w
        out.append(acc / (tot or 1.0))
    b = dict(a)
    b["xy"] = [float(v) for q in out for v in q]
    return b


# ---------------------------------------------------------------- dựng
def dung():
    D, D0, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    Wi = mats(D0)
    by0 = {a["slot"]: a for a in D0["atts"]}
    byg = {}
    for a in D["atts"]:
        byg.setdefault(a["slot"], []).append(a)
    tat = np.concatenate([np.array(a["xy"], float).reshape(-1, 2) for a in D0["atts"] if a["slot"] not in BO and a.get("xy")])
    y_day = float(tat[:, 1].min())
    Vb = np.concatenate([np.array(by0[s]["xy"], float).reshape(-1, 2) for s in ("1chest", "head1", "body1")])
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
    sk.xuong("bong", "day", 0.0, float(tam[1] - y_day))
    # ---- slot theo thứ tự vẽ của họ
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    for g in NHOM_TRON:
        for k in g:
            if k in DATJ:
                DA_GIAC[k] = da_giac_manh(k)
                A0_NHOM[k] = by0[k]
    if "mt1" in DATJ:                                            # bụng / ngực sát hàm đi theo hàm (khỏi hở vạch sáng ở mép dưới hàm)
        DA_GIAC["mt1"] = da_giac_manh("mt1")
        for s_ in ("chest1", "chest3", "body1"):
            PHA_TRONG_SO[s_] = ("mt1", 50.0, 1.0, by0["mt1"])
    thu_tu = [s["name"] for s in sorted(I["slots"], key=lambda q: [a["order"] for a in D0["atts"] if a["slot"] == q["name"]][:1] or [99])]
    thu_tu = [s["name"] for s in I["slots"]]                     # thứ tự slot trong info = thứ tự vẽ mặc định
    tong = [0, 0]
    dat_slot = []
    for s in thu_tu:
        if s in BO:
            continue
        if s == "eyes1":                                         # mắt nhắm: ẩn sẵn, clip bật như họ; bám ĐÚNG lưới mắt mở (eyes2) để
            sk.slot("eyes1", "move", "eyes1", an=True)           # trùng khít mắt mở ở mọi dáng (eyes1 của họ bám 100 % bone34, eyes2 thì nửa)
            gan_manh(sk, "eyes1", "eyes1", by0["eyes2"], ten, Wi)
            continue
        if s not in DATJ:
            print(f"  (thiếu mảnh) {s}: bỏ")
            continue
        a0 = by0.get(s) or next(a for a in byg[s])
        sk.slot(s, "move", s)
        if s == "shetou":                                        # lòng miệng: cứng trên đầu, nấp sau đầu + hàm, lấp khe khi hàm há
            T = MN.tf()
            hx0, hy0, hx1, hy1 = DATJ["mt1"]["hop"]
            Pj = T["c2w"](np.array([[hx0, hy0], [hx1, hy1]], float))
            jw, jh = float(Pj[1, 0] - Pj[0, 0]), float(Pj[0, 1] - Pj[1, 1])
            # phủ từ mép sau hàm (lùi 4 %) tới gần mõm (96 %), từ trên mép răng 0,2 hàm xuống 0,45 hàm
            c = np.array([Pj[0, 0] + 0.43 * jw, Pj[0, 1] - 0.125 * jh])
            L, V = gan_manh(sk, s, s, {}, ten, Wi, xuong_cung="bone12", dat_lai=(c, 1.06 * jw, 0.65 * jh), w_the_gioi=True)
            # nửa trên bám đầu, nửa dưới bám hàm (theo lưới hàm của họ), giữa pha dần: lòng miệng giãn theo độ há, không lộ nền
            yt, yb = float(V[:, 1].max()), float(V[:, 1].min())
            r_dau = [[("bone12", *[float(v) for v in np.linalg.solve(Wi["bone12"], np.array([q[0], q[1], 1.0]))[:2]], 1.0)] for q in V]
            r_ham = trong_so_goc(V, by0["mt1"], ten, Wi)
            rows = []
            for q, ra, rb in zip(V, r_dau, r_ham):
                u = (yt - q[1]) / max(1e-6, yt - yb)
                f = float(np.clip((u - 0.30) / 0.45, 0.0, 1.0))
                f = f * f * (3 - 2 * f)
                acc = {}
                for (n, x, y, w), k in [(e, 1 - f) for e in ra] + [(e, f) for e in rb]:
                    if w * k <= 1e-6:
                        continue
                    e_ = acc.setdefault(n, [0.0, 0.0, 0.0])
                    e_[0] += w * k
                    e_[1] += w * k * x
                    e_[2] += w * k * y
                tot = sum(e_[0] for e_ in acc.values()) or 1.0
                rows.append([(n, e_[1] / e_[0], e_[2] / e_[0], e_[0] / tot) for n, e_ in acc.items()])
            Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
            sk.luoi_gan(s, s, L, trongso.cung(L.n, "move"), the_gioi=Vs)
            sk.atts[s][s]["verts"] = rows
        else:
            L, V = gan_manh(sk, s, s, a0, ten, Wi)
        tong[0] += L.n
        tong[1] += len(L.tris)
        dat_slot.append(s)
        for them, sau in SAU_SLOT.items():
            if sau == s and them in DATJ:
                sk.slot(them, "move", them)
                L, V = gan_manh(sk, them, them, {}, ten, Wi, xuong_cung=XUONG_THEM[them])
                tong[0] += L.n
                tong[1] += len(L.tris)
    # quả cầu cuộn tròn: cứng trên xương bong, cỡ bằng quả cầu của họ (slot xz), tâm ở tâm thân
    if "xz" in DATJ:
        axz = next(a for a in byg["xz"])
        Q = np.array(axz["xy"], float).reshape(-1, 2)
        rong = float(max(Q[:, 0].max() - Q[:, 0].min(), Q[:, 1].max() - Q[:, 1].min()))
        sk.slot("xz", "move", "xz", an=True)
        gan_manh(sk, "xz", "xz", {}, ten, Wi, xuong_cung="bong", dat_lai=(sk.W0["bong"][:2, 2], rong * 0.92))
    # chỗ nhả tảng đá: mép trước hàm (giữa hai hàm), con của đầu
    hm = np.array(sk.atts["mt1"]["mt1"]["V"])
    hd = np.array(sk.atts["head1"]["head1"]["V"])
    x_m = float(hm[:, 0].max()) - 0.10 * float(hm[:, 0].max() - hm[:, 0].min())
    y_m = float(hm[:, 1].max()) + 6.0
    sk.xuong("mieng", "bone12", x_m, y_m, goc=12.0, the_gioi=True)
    for e, m in (("trung", "khung trúng"), ("tu", "cast: bắt đầu tụ tảng đá trong miệng (VFX hút đá, bụi)"),
                 ("phun", "cast: phun tảng đá (đạn do VFX từ xương mieng)"), ("cuon", "skill: cuộn tròn thành quả cầu"),
                 ("xoay", "skill: quả cầu xoay tại chỗ, bụi tóe sau"), ("lao", "skill: quả cầu lao đi"),
                 ("cham_dat", "chạm đất (bụi tròn)"), ("bung", "bung ra khỏi dạng cầu"), ("dam", "idle: dậm chân trước (bụi)"),
                 ("khit", "idle: khịt hai luồng bụi ở mũi"), ("lat", "die: lật ngửa"), ("rung_pl", "die: pha lê rụng")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; đáy y = {y_day:.1f}, tâm ({tam[0]:.1f}, "
          f"{tam[1]:.1f}); mieng ({x_m:.0f}, {y_m:.0f})")
    top = float(np.array(sk.atts["1chest"]["1chest"]["V"])[:, 1].max())
    return sk, dict(IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], y_day=y_day, tam=tam, S=S, Wi=Wi, top=top)


# ---------------------------------------------------------------- chuyển động của họ
def chuyen_dong(info):
    S, ten, goc0 = info["S"], info["ten"], info["goc0"]
    sl = info["slots"]
    ie1 = sl.index("eyes1")
    out = {}
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
        nham = [bool(F["n"][ie1]) for F in fr]
        out[clip] = (float(v["dur"]), res, len(fr), nham)
    return out


# ---------------------------------------------------------------- mốc giờ
D_IDLE = 4.0                                           # ba nhịp thở 1,333 s của idle_01 (khung 4,0 s trùng khung 0)
T_KHIT = 3.05                                          # idle: khịt mũi (vòng thứ hai)
D_ATTACK, T_GIANG = 1.15, 0.50
D_CAST, T_TU, T_PHUN = 1.50, 0.12, 0.92
T_CUON, T_LAO, T_NEN, T_VE, T_BUNG, D_SKILL = 0.32, 0.86, 1.20, 1.64, 1.70, 2.50
LAO = 0.95                                             # đỉnh lao (× chiều cao) ở khung nện; game nắn quãng
T_TOI, T_BUNG_A, D_APPEAR = 0.70, 0.86, 1.75
T_LAT0, T_LAT1, T_RUNG, T_DAP0, T_DAP1 = 0.36, 0.78, 0.42, 0.82, 1.28
D_DIE = 1.32 + TAN


def lam_clip(sk, info, cao=730.0):
    CD = chuyen_dong(info)
    tam = info["tam"]
    y_day = info["y_day"]
    slot_than = [s["name"] for s in sk.slots if s["name"] not in ("xz", "eyes1")]

    def dat(P, goc, tau, lap=False, mat=True, chi=None, bo=(), chuan=False):
        dur, R, n, NH = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            if (chi is not None and b not in chi) or b in bo:
                continue
            v = A[i0] * (1 - w) + A[i1] * w
            r = float(v[0])
            if chuan:
                r -= 360.0 * round(r / 360.0)
            if abs(r) > 1e-4:
                P.rot(b, r)
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]), float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(v[3]), float(v[4]))
        if mat:
            P.alpha["eyes1"] = 1.0 if NH[min(n - 1, int(round(x)))] else 0.0

    def dam(P, a, chi=None):
        if a < 0.999:
            for s in sk.slots:
                if chi is None or s["name"] in chi:
                    P.alpha[s["name"]] = a * P.alpha.get(s["name"], s["alpha"])

    def dang_cau(P, cau):
        """cau = True: ẩn thân, hiện quả cầu."""
        for s in slot_than:
            P.alpha[s] = 0.0 if cau else P.alpha.get(s, 1.0)
        P.alpha["eyes1"] = 0.0 if cau else P.alpha.get("eyes1", 0.0)
        P.alpha["xz"] = 1.0 if cau else 0.0

    LIEN = {"t": -1.0}                                          # góc riêng lần trước của từng xương (clip nướng tuần tự theo giờ)

    def dat_tg(P, b, xy, goc_tg, t=None):
        W = sk.the_gioi(P)
        cha = sk.bones[sk.bi[b]]["parent"]
        Wp = W[cha]
        lp = np.linalg.solve(Wp, np.array([xy[0], xy[1], 1.0]))
        b0 = sk.bones[sk.bi[b]]
        g = P._g(b)
        g[0] = float(lp[0]) - b0["x"]
        g[1] = float(lp[1]) - b0["y"]
        dr = goc_tg - _goc(Wp) - b0["rot"]
        if t is not None:
            if t < LIEN["t"] - 1e-6:                             # nướng lại từ đầu
                for k in [k for k in LIEN if k != "t"]:
                    del LIEN[k]
            LIEN["t"] = t
            ref = LIEN.get(b, g[2])
            dr = ref + ((dr - ref + 180.0) % 360.0 - 180.0)     # liền với khung trước (quay nhiều vòng được, không nhảy 360°)
            LIEN[b] = dr
            g[2] = dr
            return
        cur = _goc(W[b]) - _goc(Wp) - b0["rot"]
        g[2] = cur + ((dr - cur + 180.0) % 360.0 - 180.0)

    # ------------------------------------------------ idle

    def f_idle(t, P):
        """idle MỀM (người dùng chê idle giật ở tatu): dáng nền = idle_01 khung 0 đứng yên; chồng các sóng sin nhỏ chu kỳ 2 s, lệch pha
        (thân dẫn → đầu trễ 0,1 s → hàm, túi họng 0,22 s → pha lê trễ 0,15–0,35 s); trò nhỏ ở vòng thứ hai: KHỊT MŨI (đầu ngẩng 3° êm,
        chớp mắt) + túi họng phồng to hơn một nhịp."""
        dat(P, "idle_01", 0.0)
        CK = 2.0
        s_ = lambda tre: math.sin(2 * math.pi * (t - tre) / CK)
        P.scale("day", 1.0 - 0.008 * s_(0.0), 1.0 + 0.018 * s_(0.0))          # thở: phình dọc 1,8 %, co ngang 0,8 %, chân không trượt
        P.rot("bone3", 0.6 * s_(0.05))                                      # ngực
        P.rot("bone14", -0.5 * s_(0.08))                                    # lưng ngược chiều ngực
        P.rot("bone12", 1.0 * s_(0.10))                                     # đầu trễ 0,1 s
        P.rot("bone40", -0.7 * s_(0.20))                                    # hàm hé theo nhịp thở
        phong = 1.0 + 0.6 * hoat.cv(t, [(2.30, 0.0), (2.75, 1.0, "io"), (3.35, 1.0), (3.85, 0.0, "io")])
        P.scale("bone23", 1.0 + 0.015 * phong * (0.5 + 0.5 * s_(0.22)), 1.0 + 0.03 * phong * (0.5 + 0.5 * s_(0.22)))   # túi họng
        for k, b in enumerate(("bone28", "bone27", "bone26", "bone32", "bone31", "bone29", "bone30")):   # pha lê lắc nhẹ, mỗi viên một pha
            P.rot(b, (1.4 - 0.1 * k) * s_(0.15 + 0.035 * k))
        # trò nhỏ: khịt mũi ở vòng thứ hai
        kk = hoat.cv(t, [(T_KHIT - 0.30, 0.0), (T_KHIT, 1.0, "io"), (T_KHIT + 0.35, 0.0, "io")])
        P.rot("bone12", 3.0 * kk)
        P.rot("bone40", -1.2 * kk)
        if T_KHIT - 0.05 < t < T_KHIT + 0.08:
            P.alpha["eyes1"] = 1.0

    def f_walk(t, P):
        dat(P, "run_01", t, True)

    def f_hit(t, P):
        dat(P, "hit_01", t)

    # ------------------------------------------------ attack: chồm, nhích tới, giáng sừng
    def f_attack(t, P):
        tau = tmap(t, [(0.0, 0.0), (0.40, 0.36, "io"), (T_GIANG, 0.47, "in"), (0.72, 0.62, "out"), (D_ATTACK, 1.067, "io")])
        dat(P, "skill_01_1", tau)
        lao = hoat.cv(t, [(0.0, 0.0), (0.36, -0.03, "io"), (T_GIANG, 0.20, "in"), (0.70, 0.20), (D_ATTACK - 0.06, 0.0, "io")])
        P.move("move", cao * lao, 0.0)
        k = math.exp(-((t - (T_GIANG + 0.03)) / 0.05) ** 2)
        P.scale("day", 1 + 0.10 * k, 1 - 0.09 * k)
        if T_GIANG - 0.02 < t < T_GIANG + 0.10:
            P.alpha["eyes1"] = 1.0

    # ------------------------------------------------ cast: há hàm tụ, phun tảng đá
    def f_cast(t, P):
        tau = tmap(t, [(0.0, 0.0), (0.60, 0.53, "io"), (T_PHUN - 0.05, 0.66, "lin"), (T_PHUN, 0.74, "in"), (1.10, 0.86, "out"),
                       (D_CAST, 1.2, "io")])
        dat(P, "skill_02_1", tau)
        # tụ: đầu ngửa thêm, rung hai dáng lúc giữ; phun: đầu giật tới, thân lùi
        ngua = hoat.cv(t, [(0.0, 0.0), (0.60, 1.0, "io"), (T_PHUN - 0.06, 1.0), (T_PHUN, -0.6, "in"), (1.10, 0.0, "out")])
        P.rot("bone12", 6.0 * ngua)
        P.rot("bone12", 1.2 * hoat.rung(t, 0.62, T_PHUN - 0.06, 2))
        lui = hoat.cv(t, [(T_PHUN - 0.02, 0.0), (T_PHUN + 0.06, 1.0, "out"), (1.2, 0.0, "io")])
        P.move("move", -0.05 * cao * lui, 0.0)
        P.rot("tam", 3.0 * lui)
        k = math.exp(-((t - (T_PHUN + 0.03)) / 0.05) ** 2)
        P.scale("day", 1 - 0.06 * k, 1 + 0.06 * k)

    # ------------------------------------------------ skill: cuộn tròn → quả cầu xoay gồng → lăn nện → nảy về → bung ra
    D3 = CD["skill_03"][0]
    r_cau = 0.5 * float(np.ptp(np.array(sk.atts["xz"]["xz"]["V"])[:, 1])) if "xz" in sk.atts and "xz" in sk.atts["xz"] else 0.3 * cao
    h_tam = float(tam[1] - y_day)

    def cau_goc(t0, t1, vong, kieu="in", t=0.0):
        return -360.0 * vong * ease((t - t0) / max(1e-6, t1 - t0), kieu)

    def f_skill(t, P):
        if t < T_CUON:                                           # co mình (đầu skill_03)
            dat(P, "skill_03", t * (0.30 / T_CUON), chuan=True)
            return
        if t < T_BUNG:
            dat(P, "skill_03", 0.30 if t < T_CUON + 1.5 / FPS else 1.00, chuan=True, mat=False)
            dang_cau(P, True)
            # độ cao tâm quả cầu so với tâm thân: quả cầu nằm chạm đất
            y0 = r_cau - h_tam
            goc = 0.0
            if t < T_LAO:                                        # xoay tại chỗ, nhanh dần, nhún
                u = (t - T_CUON) / (T_LAO - T_CUON)
                goc = -360.0 * 2.0 * u * u
                nh = 0.06 * math.sin(2 * math.pi * (t - T_CUON) / 0.11) * u
                P.scale("day", 1 + nh, 1 - nh)
                P.move("move", -0.03 * cao * ease(u), 0.0)
                pop = hoat.cv(t, [(T_CUON, 0.7), (T_CUON + 0.06, 1.12, "out"), (T_CUON + 0.14, 1.0, "io")])
                P.scale("bong", pop, pop)
                P.move("bong", 0.0, y0)
            elif t < T_NEN:                                      # lao vồng tới đối thủ
                u = (t - T_LAO) / (T_NEN - T_LAO)
                goc = -720.0 - 360.0 * 2.2 * u
                x = -0.03 + (LAO + 0.03) * ease(u, "in")
                P.move("move", cao * x, 0.0)
                P.move("bong", 0.0, y0 + 0.30 * cao * math.sin(math.pi * u))
            else:                                                # nện → nảy vồng về chỗ cũ
                u = (t - T_NEN) / (T_VE - T_NEN)
                goc = -720.0 - 792.0 - 360.0 * 1.2 * ease(u, "out")
                P.move("move", cao * LAO * (1 - ease(u, "io")), 0.0)
                P.move("bong", 0.0, y0 + 0.42 * cao * math.sin(math.pi * u))
                b = math.exp(-(t - T_NEN) / 0.05)
                P.scale("day", 1 + 0.16 * b, 1 - 0.16 * b)
                if t > T_VE - 0.02:
                    b2 = math.exp(-(t - T_VE) / 0.05)
                    P.scale("day", 1 + 0.12 * b2, 1 - 0.12 * b2)
            P.rot("bong", goc)
            return
        # bung ra đáp đất: đoạn cuối skill_03 (thân xoay nốt vòng cuối trên không rồi đáp)
        tau = 1.00 + (t - T_BUNG) / (D_SKILL - T_BUNG) * (D3 - 1.00)
        dat(P, "skill_03", tau, chuan=True)
        if t < T_BUNG + 0.06:                                    # quả cầu tan vào thân (2 khung)
            P.alpha["xz"] = 1.0 - (t - T_BUNG) / 0.06
            P.move("bong", 0.0, r_cau - h_tam)

    # ------------------------------------------------ appear: quả cầu lăn vào, nảy, bung ra
    def f_appear(t, P):
        if t < T_BUNG_A:
            dat(P, "skill_03", 1.00, chuan=True, mat=False)
            dang_cau(P, True)
            P.alpha["xz"] = min(1.0, t / 0.12)
            u = min(1.0, t / T_TOI)
            x = -0.85 * (1 - ease(u, "out"))
            P.move("move", cao * x, 0.0)
            goc = 360.0 * 0.85 * cao * (1 - ease(u, "out")) / (2 * math.pi * r_cau)    # lăn không trượt (lăn sang phải: quay ngược chiều kim)
            y = r_cau - h_tam
            if t > T_TOI - 0.22:                                 # nảy một lần cuối đường lăn
                v = (t - (T_TOI - 0.22)) / 0.22
                y += 0.10 * cao * math.sin(math.pi * min(1.0, v))
            P.move("bong", 0.0, y)
            P.rot("bong", goc)
            if t > T_TOI:
                b = math.exp(-(t - T_TOI) / 0.05) * math.cos((t - T_TOI) * 2 * math.pi / 0.16)
                P.scale("day", 1 + 0.12 * b, 1 - 0.12 * b)
            return
        tau = 1.00 + (t - T_BUNG_A) / (D_APPEAR - T_BUNG_A) * (D3 - 1.00)
        dat(P, "skill_03", tau, chuan=True)
        if t < T_BUNG_A + 0.06:
            P.alpha["xz"] = 1.0 - (t - T_BUNG_A) / 0.06
            P.move("bong", 0.0, r_cau - h_tam)

    # ------------------------------------------------ die: giật, nhắm mắt → lật ngửa, pha lê rụng → đạp chân → mờ
    top = info["top"]
    d_top = top - float(tam[1])                                 # tâm → lưng (không kể pha lê)
    d_bot = h_tam                                               # tâm → đáy chân
    rung_pl = {}

    def than_die(t, P):
        dat(P, "die_01", min(t, T_LAT0) * (0.45 / T_LAT0))
        P.alpha["eyes1"] = 1.0 if t > 0.10 else P.alpha.get("eyes1", 0.0)
        if t > T_LAT0:
            u = ease((t - T_LAT0) / (T_LAT1 - T_LAT0), "io")
            th = 172.0 * u
            P.rot("tam", th)
            y = (d_top - d_bot) * (1 - math.cos(math.radians(th))) / 2 + 0.12 * cao * math.sin(math.pi * min(1.0, (t - T_LAT0) /
                                                                                                             (T_LAT1 - T_LAT0)))
            P.move("day", -0.10 * cao * u, y)
            if t > T_LAT1:                                       # chạm đất ngửa: nảy
                b = math.exp(-(t - T_LAT1) / 0.07) * math.sin((t - T_LAT1) * 2 * math.pi / 0.2)
                P.scale("day", 1 + 0.07 * b, 1 - 0.07 * b)
        if T_DAP0 < t < T_DAP1 + 0.2:                            # bốn chân đạp, tắt dần, mỗi chân một pha
            for k, (ch, bs) in enumerate(CHAN.items()):
                a = 16.0 * math.exp(-(t - T_DAP0) / 0.28) * math.sin((t - T_DAP0) * 2 * math.pi / 0.14 + 1.3 * k)
                P.rot(bs[1], a)
                P.rot(bs[2], -0.8 * a)

    def f_die(t, P):
        than_die(t, P)
        if t > T_RUNG:                                           # pha lê rơi: bay ra khỏi lưng, rơi xuống đất, nảy một lần, nằm
            if not rung_pl:
                P0 = khung.Pose()
                than_die(T_RUNG, P0)
                W = sk.the_gioi(P0)
                for i, s in enumerate(PHA_LE):
                    if s not in sk.si:
                        continue
                    b = PL_XUONG[s]
                    V = np.array(sk.atts[s][s]["V"])
                    c0 = V.mean(0)
                    c = (W[b] @ np.linalg.solve(sk.W0[b], np.array([c0[0], c0[1], 1.0])))[:2]
                    rung_pl[s] = (b, W[b][:2, 2].copy(), _goc(W[b]), c, (-1) ** i * (0.15 + 0.05 * i) * cao, 0.35 * cao,
                                  (-1) ** (i + 1) * (260.0 + 40 * i), float(np.ptp(V[:, 1])) * 0.35)
            dtt = t - T_RUNG
            for s, (b, p0, a0, c0, vx, vy, w, nua) in rung_pl.items():
                g = 2.6 * cao
                y = c0[1] + vy * dtt - 0.5 * g * dtt * dtt
                y_dat = nua
                x = c0[0] + vx * dtt
                ang = a0 + w * dtt
                if y < y_dat:                                    # chạm đất: nằm yên (đã nảy bằng vận tốc nhỏ)
                    t_ch = (vy + math.sqrt(max(0.0, vy * vy + 2 * g * (c0[1] - y_dat)))) / g
                    x = c0[0] + vx * t_ch + 0.15 * vx * min(dtt - t_ch, 0.2)
                    du = dtt - t_ch
                    y = y_dat + 0.06 * cao * max(0.0, math.sin(math.pi * min(1.0, du / 0.18)))
                    ang = a0 + w * t_ch + 0.2 * w * min(du, 0.18)
                dl = np.array([x, y]) - c0
                dat_tg(P, b, p0 + dl, ang, t=t)
        dam(P, float(np.clip(1.0 - (t - (D_DIE - TAN)) / (TAN - 0.05), 0.0, 1.0)))

    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=[(T_TOI, "cham_dat", ""), (T_BUNG_A, "bung", ""), (T_BUNG_A + 0.24, "cham_dat", "")]),
        Clip("idle", D_IDLE, f_idle, loop=True, ev=[(T_KHIT, "khit", "")]),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", D_ATTACK, f_attack, ev=[(T_GIANG, "trung", "")], trung=T_GIANG),
        Clip("cast", D_CAST, f_cast, ev=[(T_TU, "tu", ""), (T_PHUN, "phun", "")], trung=T_PHUN),
        Clip("skill", D_SKILL, f_skill, ev=[(T_CUON, "cuon", ""), (T_CUON + 0.04, "xoay", ""), (T_LAO, "lao", ""), (T_NEN, "trung", ""),
                                             (T_VE, "cham_dat", ""), (T_BUNG, "bung", ""), (T_BUNG + 0.26, "cham_dat", "")], trung=T_NEN),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", D_DIE, f_die, ev=[(T_LAT0, "lat", ""), (T_RUNG, "rung_pl", ""), (T_LAT1, "cham_dat", "")]),
    ]
    return clips


def main(a):
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0)
    clips = lam_clip(sk, info, cao)
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
                    if da > 35.0 and b != "bong":
                        xau.append(f"{i / 30:.2f}s {b} xoay {da:.0f}°")
            Wl = [sk.the_gioi(P) for P in fr]
            for s, b in (("head1", "bone12"), ("1chest", "bone14"), ("lhand2", "bone7"), ("rhand3", "bone11"), ("xz", "bong")):
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
        Bx = soi._union([ve0.bao(P) for P in Ps], 0.04)
        sc = float(a[3]) if len(a) > 3 else 0.35
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
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de="Cóc tê giác pha lê (thu_da_1): tướng 3 đảo Thổ", dang=1, so_dang=1,
                  dung_yen=("cast",), lao=("skill",), ma_goc=None, khop_idle=0.2, cao=cao, impact=IMPACT,
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.3, tran_mb=0.5, span=3.6)


if __name__ == "__main__":
    main(sys.argv[1:])
