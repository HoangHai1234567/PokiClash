# -*- coding: utf-8 -*-
"""Vượn núi đá bốn tay (quy_nui; tướng 5 đảo Thổ, ải 20, mạnh nhất trong năm con đầu): hình của mình chạy trên ĐÚNG rig của con gốc
monster_3612 (golem bốn tay nhìn thẳng; game tham khảo). Ghi chú: inbox/quy_nui_ghichu.md. Cách làm như quang_sat_rig.py:
- XƯƠNG: đủ xương của họ (81; bỏ shadow và 8 xương đích IK: IK của họ đã được runtime nướng vào biến đổi riêng `l` của mẫu khung), thêm
  `move` (sân nắn quãng lao tới), `mieng` (điểm phát VFX: chỗ hai nắm đấm nện đất ở cast, tâm tảng đá ở skill).
- MẢNH: ảnh của mình "đúng chỗ, đúng cỡ" trên concept (quy_nui_manh.py → inbox/quy_nui_1/manh/), concept căn lên con gốc bằng co + dời
  (mau/can.json); mỗi mảnh là lưới phủ hình, mỗi đỉnh biến dạng ĐÚNG như điểm tương ứng trên NHÓM lưới gốc (gan_goc trên lưới gộp các slot
  của họ: trọng số + điểm gắn riêng từng xương). BỎ đuôi weiba1/2 + jiapian, bốn dải piaodai*.
- CHUYỂN ĐỘNG (đề xuất tho5_anim.py, người dùng "làm đi" 2026-11-17):
    appear = nhảy từ trên cao xuống (dáng bay của skill_03), đáp quỳ nện hai nắm đấm (dáng đáp skill_03), đứng dậy, ĐẤM NGỰC bốn tay so le,
             ngửa gầm (dáng dang tay của skill_02);
    idle   = idle_01 (4 s) + ngón tay phụ co duỗi lệch pha + tay phụ phải (nửa phải tranh) GÃI ĐẦU 2,35 → 3,35 s;
    walk   = run_01; hit = hit_01; die = die_01 + tan;
    attack = liên hoàn ba nhịp rút từ skill_01 (đấm, đấm, hai tay phụ đập), khung trúng ở nhịp 3;
    cast   = skill_02 kéo dài: giơ hai nắm đấm quá đầu, gồng, NỆN đất (sóng chấn là VFX);
    skill  = hai tay phụ giơ lên ôm một tảng đá khổng lồ đang lớn dần (VFX; tay ôm đúng mép tảng, ngón quặp), hai nắm đấm nện đất hai
             nhịp gồng (skill_02), cả con ngả ra rồi tung tảng đá tới trước (đường bay do code), về.
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quy_nui_rig.py goc_tam                         bộ mảnh TẠM bằng da gốc → inbox/quy_nui_1/manh_goc/
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/quy_nui_rig.py    → inbox/quy_nui_1/rig/
    py -3 -I ArtGen/Spine/quy_nui_rig.py soi <clip> <giây,...|n=12|t0:t1:n> [tỉ lệ]   → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/quy_nui_rig.py kiem                            đo góc nhảy / bước dời từng clip
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
import tho5  # noqa: E402
from hoa_ho_rig import ease, tmap, _goc  # noqa: E402

G = tho5.dat("quy_nui")
TEN_RIG = "quy_nui_1"
D_PX = float(os.environ.get("QN_DPX", "0.45"))       # pixel ảnh atlas cho mỗi đơn vị rig (con cao ~1070 đơn vị)
GOC = os.environ.get("QN_GOC") == "1"
MANH = os.path.join(G.BASE, "manh_goc" if GOC else "manh")
RA = os.environ.get("QN_RA") or os.path.join(G.BASE, "rig_goc" if GOC else "rig")
TAN = 0.45
FPS = 30.0
IMPACT = {"attack": (0.12, 0.65, 0.14), "cast": (0.14, 0.8, 0.15), "skill": (0.20, 1.2, 0.18, "#fff3d08c")}
BO_XUONG = {"shadow", "R1", "R2", "L1", "L2", "SL1", "SL2", "SR1", "SR2"}

# mảnh của mình (thứ tự vẽ sau → trước) → slot gốc dùng làm lưới gắn
MANH_GOC = [
    ("ngon_L1", None), ("ngon_L2", None), ("ngon_L3", None), ("duoi_L", ["jixieshouL2"]), ("tren_L", ["jixieshouL1"]),
    ("ngon_R1", None), ("ngon_R2", None), ("ngon_R3", None), ("duoi_R", ["jixieshouR2"]), ("tren_R", ["jixieshouR1"]),
    ("vai_L", ["shouL1_2"]), ("canh_L", ["shouL2", "shouL3_2", "shouL1_3"]), ("dam_L", ["shouL3_1"]),
    ("chan_L", ["tuiL1", "tuiL2", "tuiL3"]), ("chan_R", ["tuiR1", "tuiR2", "tuiR3"]), ("kho", ["weiqun"]),
    ("than", ["shenti2", "xiongjia1", "xiongjia2", "shenti3"]),    # KHÔNG gộp bozi1/2: xương cổ bone62–64 giãn mạnh → lưới gập thành dải rách trên đầu
    ("vai_R", ["shouR1_2"]), ("canh_R", ["shouR2", "shouR3_2"]), ("dau", ["tou"]), ("dam_R", ["shouR3_1"]),
]
NGON_GOC = {"L": [["shouzhiL1_1", "shouzhiL1_2"], ["shouzhiL2_1", "shouzhiL2_2"], ["shouzhiL3_1", "shouzhiL3_2"]],
            "R": [["shouzhiR1_1", "shouzhiR1_2"], ["shouzhiR2_1", "shouzhiR2_2"], ["shouzhiR3_1", "shouzhiR3_2"]]}
# xương của các chi (theo NGƯỜI XEM: R = nửa trái tranh)
TAY_TRUOC = {"R": ("bone20", "bone21", "bone22"), "L": ("bone16", "bone17", "bone18")}      # vai, cẳng, nắm đấm
TAY_PHU = {"R": ("bone34", "bone35", "bone36"), "L": ("bone24", "bone25", "bone26")}         # bắp, cẳng, lòng bàn tay
NGON = {"R": ("bone37", "bone38", "bone39", "bone40", "bone41", "bone42"), "L": ("bone27", "bone28", "bone29", "bone30", "bone31", "bone32")}
CHAN = {"R": ("bone2", "bone3", "bone4"), "L": ("bone5", "bone6", "bone7")}
DAU = (150.0, 280.0)                   # đỉnh sọ (dưới vương miện) theo xương đầu bone14, đo trên hình tou ở idle 0
NGUC = (88.0, -55.0)                   # giữa ngực theo xương ngực bone12


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
    """px concept → toạ độ rig (qua phép căn co k + dời của mau/can.json rồi phép đổi của goc_ca_con)."""
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    c = json.load(open(os.path.join(G.MAU, "can.json")))
    s, cx, cy, k, tx, ty = j["s"], j["cx"], j["cy"], c["k"], c["tx"], c["ty"]
    to_rig = lambda P: np.stack([cx + (k * P[:, 0] + tx - 768) / s, cy - (k * P[:, 1] + ty - 512) / s], 1)
    to_px = lambda V: np.stack([((V[:, 0] - cx) * s + 768 - tx) / k, ((cy - V[:, 1]) * s + 512 - ty) / k], 1)
    return s / k, to_rig, to_px                         # px concept mỗi đơn vị rig


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


def gop_att(atts):
    """gộp nhiều hình lưới của họ thành một (đỉnh, tam giác, trọng số nối tiếp) để gan_goc trên cả nhóm."""
    xy, tris, w = [], [], []
    n = 0
    for a in atts:
        Q = np.array(a["xy"], float).reshape(-1, 2)
        xy.append(Q)
        tris.append(np.array(a["tris"]).reshape(-1, 3) + n)
        w += a["w"]
        n += len(Q)
    return {"xy": np.concatenate(xy).ravel().tolist(), "tris": np.concatenate(tris).ravel().tolist(), "w": w}


def trong_so_goc(V, a0, ten, Wi):
    """như quang_sat_rig.trong_so_goc: mỗi điểm biến dạng như điểm tương ứng trên lưới (gộp) của họ."""
    Q = np.array(a0["xy"], float).reshape(-1, 2)
    tr = np.array(a0["tris"]).reshape(-1, 3)
    Wg = [{ten[k]: w for k, w in ws if w > 0.002} for ws in a0["w"]]
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
            i = int(ok[-1])                              # hình gộp: tam giác của hình vẽ SAU CÙNG (trên cùng) thắng
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


# mảnh gắn trên lưới GỘP nhiều khúc của họ: trọng số đổi đột ngột ở ranh hai khúc → gập là nứt (chân gối, ngón đốt, thân hông). Làm trơn
# trọng số theo lưới của mình (số vòng) rồi gắn kiểu thường (điểm gắn = nghịch ma trận dáng gốc).
MUOT = {"chan_R": 10, "chan_L": 10, "than": 6, "canh_R": 4, "canh_L": 4, "duoi_R": 6, "duoi_L": 6}
MUOT_NGON = 5


def lam_tron_ts(L, rows, vong):
    n = L.n
    ke = [set() for _ in range(n)]
    for a, b, c in np.asarray(L.tris, int):
        ke[a] |= {b, c}
        ke[b] |= {a, c}
        ke[c] |= {a, b}
    W = [{bn: w for bn, _, _, w in r} for r in rows]
    for _ in range(vong):
        W2 = []
        for i in range(n):
            acc = dict((k, 0.5 * v) for k, v in W[i].items())
            m = len(ke[i]) or 1
            for j in ke[i]:
                for k, v in W[j].items():
                    acc[k] = acc.get(k, 0.0) + 0.5 * v / m
            W2.append(acc)
        W = W2
    out = []
    for d in W:
        top = sorted(d.items(), key=lambda kv: -kv[1])[:4]
        tot = sum(v for _, v in top) or 1.0
        out.append({k: v / tot for k, v in top if v / tot > 0.003})
    return out


def gan_manh(sk, slot, ten_anh, a0, ten, Wi):
    im, (x0, y0, x1, y1), kq = anh_manh(ten_anh)
    if ten_anh not in sk.images:
        sk.anh(ten_anh, im)
    im = sk.images[ten_anh]
    _, to_rig, _ = tf()
    bv = max(6.0, min(12.0, 0.06 * min(im.width, im.height)))
    L = luoi.luoi_vung(im, buoc_vien=bv, buoc_trong=bv * 1.5, vien=2, ten=slot, in_tk=False)
    Px = np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1)
    V = to_rig(Px)
    rows = trong_so_goc(V, a0, ten, Wi)
    vong = MUOT.get(ten_anh, MUOT_NGON if ten_anh.startswith("ngon_") else 0)
    if vong:
        Wd = lam_tron_ts(L, rows, vong)
        sk.luoi_gan(slot, ten_anh, L, Wd, the_gioi=V)
        return L
    Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
    sk.luoi_gan(slot, ten_anh, L, trongso.cung(L.n, "move"), the_gioi=Vs)
    sk.atts[slot][ten_anh]["verts"] = rows
    return L


def gan_ngon(sk, ten_m):
    """ngón vuốt của mình: xương gốc ngón RIÊNG đặt đúng chân ngón (đỉnh lưới gần mút xương lòng bàn tay nhất), con của xương lòng bàn tay,
    trục chĩa về giữa ngón; ngón bám cứng xương đó. (Bám xương ngón của họ thì ngón quay quanh khớp ngón gốc, ở chỗ khác → co duỗi là văng
    khỏi lòng bàn tay.) Danh sách xương gốc ngón từng bên: sk.info['ngon'][bên]."""
    side = ten_m[5]
    b_tay = TAY_PHU[side][2]
    by0, ten, Wi = sk.info["by0"], sk.info["ten"], sk.info["Wi"]
    a_tay = gop_att([by0["jixieshouR2" if side == "R" else "jixieshouL2"]])
    im, (x0, y0, x1, y1), kq = anh_manh(ten_m)
    if ten_m not in sk.images:
        sk.anh(ten_m, im)
    im = sk.images[ten_m]
    _, to_rig, _ = tf()
    bv = max(6.0, min(12.0, 0.06 * min(im.width, im.height)))
    L = luoi.luoi_vung(im, buoc_vien=bv, buoc_trong=bv * 1.5, vien=2, ten=ten_m, in_tk=False)
    V = to_rig(np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1))
    bn = sk.bones[sk.bi[b_tay]]
    mut = (sk.W0[b_tay] @ np.array([bn["length"] or 80.0, 0.0, 1.0]))[:2]
    goc_ = V[int(np.argmin(np.hypot(*(V - mut).T)))]
    huong = V.mean(0) - goc_
    xb = f"g_{ten_m}"
    # cha = xương nặng nhất của ĐỈNH lòng bàn tay (mảnh duoi_* của mình, đã gắn) gần chân ngón nhất: ngón đi cùng đúng chỗ lòng bàn tay
    sp = sk.atts.get(f"duoi_{side}", {}).get(f"duoi_{side}")
    if sp is not None:
        j = int(np.argmin(np.hypot(*(np.asarray(sp["V"]) - goc_).T)))
        cha = max(sp["verts"][j], key=lambda r: r[3])[0]
    else:
        w0 = trong_so_goc(np.array([goc_]), a_tay, ten, Wi)[0]
        cha = max(w0, key=lambda r: r[3])[0] if w0 else b_tay
    sk.xuong(xb, cha, float(goc_[0]), float(goc_[1]), goc=math.degrees(math.atan2(huong[1], huong[0])), dai=float(np.hypot(*huong)),
             the_gioi=True)
    sk.luoi_gan(ten_m, ten_m, L, [{xb: 1.0}] * L.n, the_gioi=V)
    sk.info.setdefault("ngon", {"L": [], "R": []})[side].append(xb)
    return L


def ngon_goc(ten_anh, by0, side):
    """slot ngón gốc gần tâm mảnh ngón nhất (ngón của mình có thể 3 hay 4 / tay)."""
    _, (x0, y0, x1, y1), kq = anh_manh(ten_anh)
    _, to_rig, _ = tf()
    c = to_rig(np.array([[(x0 + x1) / 2, (y0 + y1) / 2]]))[0]
    best = min(NGON_GOC[side], key=lambda grp: float(np.hypot(*(np.concatenate(
        [np.array(by0[s]["xy"], float).reshape(-1, 2) for s in grp]).mean(0) - c))))
    return best


# ---------------------------------------------------------------- dựng
def dung():
    D, D0, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    Wi = mats(D0)
    by0 = {a["slot"]: a for a in D0["atts"]}
    sk = khung.Sk(TEN_RIG)
    sk.xuong("root")
    sk.xuong("move", "root")
    goc0 = {}
    for b in IB:
        nm = b["name"]
        if nm in ("root",) or nm in BO_XUONG:
            continue
        cha = ten[b["parent"]]
        g = [b["x"], b["y"], b["rot"], b["sx"], b["sy"]]
        goc0[nm] = g
        sk.xuong(nm, "move" if cha == "root" else cha, g[0], g[1], goc=g[2], dai=b["len"], sx=g[3], sy=g[4])
    sk.xuong("mieng", "move", 0.0, 0.0)
    sk.info.update(by0=by0, ten=ten, Wi=Wi)
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    tong = [0, 0]
    cho_ngon = []
    for ten_m, goc in MANH_GOC:
        if ten_m not in DATJ and not os.path.exists(os.path.join(G.BASE, "manh_goc", "dat.json")):
            continue
        if ten_m.startswith("ngon_"):
            if ten_m not in DATJ:
                continue
            sk.slot(ten_m, "move", ten_m)
            cho_ngon.append(ten_m)                                       # gắn sau, khi đã có lưới lòng bàn tay (duoi_*)
            continue
        a0 = gop_att([by0[s] for s in goc])
        sk.slot(ten_m, "move", ten_m)
        L = gan_manh(sk, ten_m, ten_m, a0, ten, Wi)
        tong[0] += L.n
        tong[1] += len(L.tris)
    for ten_m in cho_ngon:
        gan_ngon(sk, ten_m)
    # ngón thứ tư (nếu GPT vẽ bốn ngón một tay): slot thêm ngay sau ngón thứ ba cùng bên
    for side in "LR":
        k = 4
        while f"ngon_{side}{k}" in DATJ:
            s = f"ngon_{side}{k}"
            sk.slot(s, "move", s, truoc=f"duoi_{side}")
            gan_ngon(sk, s)
            k += 1
    # tay trước nửa phải tranh (L) vẽ SAU thân như con gốc; lúc đấm ngực nó phải ra TRƯỚC ngực: bản sao ẩn ngay sau thân (đổi thứ tự vẽ
    # trong clip bằng hai slot, skill pokiclash-spine-rig mục 28)
    for s_ in ("vai_L", "canh_L", "dam_L"):
        if s_ in sk.si:
            sk.slot(s_ + "~t", "move", s_, an=True, truoc="vai_R")
            sk.atts[s_ + "~t"][s_] = sk.atts[s_][s_]
            sk.luoi[(s_ + "~t", s_)] = sk.luoi[(s_, s_)]
    for e, m in (("trung", "khung trúng"), ("dam1", "attack: nhịp đấm 1 (VFX chớp, đá vụn)"), ("dam2", "attack: nhịp đấm 2"),
                 ("nen", "cast / skill: nắm đấm nện đất (VFX sóng chấn, bụi, rung)"), ("tu", "skill: bắt đầu tụ tảng đá giữa hai tay phụ (VFX)"),
                 ("nem", "skill: tung tảng đá (code sinh đạn từ xương mieng, cỡ = tỉ lệ xương mieng)"), ("cham_dat", "appear: đáp đất"),
                 ("dam_nguc", "appear: một cú đấm ngực (bụi nhỏ)"), ("gam", "appear: gầm"), ("soi_roi", "idle: sỏi rơi khỏi vai")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác")
    return sk, dict(IB=IB, ten=ten, goc0=goc0, slots=[s["name"] for s in I["slots"]], S=S, Wi=Wi)


# ---------------------------------------------------------------- chuyển động của họ
def chuyen_dong(info):
    S, ten, goc0 = info["S"], info["ten"], info["goc0"]
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
        out[clip] = (float(v["dur"]), res, len(fr))
    return out


# ---------------------------------------------------------------- mốc giờ
# attack: ba nhịp rút từ skill_01 (gốc: đấm 0,48; móc 0,96; hai tay phụ đập 1,69)
M_ATTACK = [(0.0, 0.0), (0.20, 0.30, "io"), (0.28, 0.48, "in"), (0.42, 0.70, "out"), (0.54, 0.96, "in"), (0.70, 1.32, "io"),
            (0.84, 1.55, "io"), (0.94, 1.69, "in"), (1.10, 1.93, "out"), (1.40, 2.167, "io")]
T_DAM1, T_DAM2, T_DAM3, D_ATTACK = 0.28, 0.54, 0.94, 1.40
# cast: skill_02 kéo dài (gốc: giơ 0,14–0,58, nện 0,72)
M_CAST = [(0.0, 0.0), (0.40, 0.43, "io"), (0.62, 0.58, "lin"), (0.72, 0.72, "in"), (1.10, 1.01, "out"), (1.55, 1.30, "io")]
T_NEN, D_CAST = 0.72, 1.55
# skill
T_TU0, T_TU1 = 0.15, 1.15              # hai tay phụ giơ lên, tảng đá lớn dần
T_NEN1, T_NEN2 = 1.32, 1.62            # hai nhịp nện gồng
T_NGA, T_NEM = 1.82, 2.02              # ngả ra sau, tung
D_SKILL = 2.80
# appear
T_DAP = 0.36                           # đáp đất
T_DUNG0, T_DUNG1 = 0.80, 1.05          # đứng dậy
T_NGUC = [1.12, 1.26, 1.40, 1.54, 1.68]   # bốn tay đấm ngực so le (vào ngực ở các mốc này)
T_GAM0, T_GAM1 = 1.86, 2.32
D_APPEAR = 2.70


def lam_clip(sk, info, cao=1050.0):
    CD = chuyen_dong(info)

    def dat(P, goc, tau, lap=False, chi=None, bo=None, k=1.0):
        dur, R, n = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            if (chi is not None and b not in chi) or (bo is not None and b in bo):
                continue
            v = A[i0] * (1 - w) + A[i1] * w
            for q in (3, 4):                                  # tỉ lệ lật dấu giữa hai khung mẫu (khoá bậc của họ): lấy khung gần nhất
                if A[i0][q] * A[i1][q] < 0:
                    v[q] = A[i0][q] if w < 0.5 else A[i1][q]
            if abs(v[0]) > 1e-4:
                P.rot(b, k * float(v[0]))
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, k * float(v[1]), k * float(v[2]))
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, 1 + k * (float(v[3]) - 1), 1 + k * (float(v[4]) - 1))

    def pha(Pa, Pb, w, chi=None):
        """hoà Pa → Pb (w 0..1) trên các xương chi (mặc định mọi xương); Pa giữ nguyên các xương khác."""
        Q = Pa.copy()
        for b in (set(Pa.t) | set(Pb.t)) if chi is None else chi:
            a_ = Pa.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            b_ = Pb.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            dr = (b_[2] - a_[2] + 180.0) % 360.0 - 180.0          # góc: đường ngắn nhất (khoá gốc có thể lệch ±360)
            sc = []
            for q in (3, 4):                                  # tỉ lệ đổi dấu (họ lật cẳng tay phụ sy = −1): nhảy ở giữa, không đi qua 0
                sc.append((b_[q] if w >= 0.5 else a_[q]) if a_[q] * b_[q] < 0 else a_[q] + (b_[q] - a_[q]) * w)
            Q.t[b] = [a_[0] + (b_[0] - a_[0]) * w, a_[1] + (b_[1] - a_[1]) * w, a_[2] + dr * w, sc[0], sc[1]]
        return Q

    def chep(P, Q):
        P.t.clear()
        P.t.update({k: list(v) for k, v in Q.t.items()})
        P.alpha.update(Q.alpha)
        P.att.update(Q.att)

    def tg(P, b, loc=(0.0, 0.0)):
        W = sk.the_gioi(P)
        return (W[b] @ np.array([loc[0], loc[1], 1.0]))[:2]

    def ngon_tip(side, b_cang):
        bn = sk.bones[sk.bi[b_cang]]
        return (bn["length"] or 100.0, 0.0)

    def ik(P, dui, cang, dich, uon=None):
        tip = ngon_tip(None, cang)
        hoat.ik_hai_doan(sk, P, dui, cang, dich, ngon=tip, uon=uon)

    def giu_dam(P, Pg, sides="RL"):
        """giữ hai nắm đấm trước đúng chỗ thế giới của chúng ở tư thế Pg (điểm tựa: nắm đấm chống đất) khi thân đổi dáng."""
        for s in sides:
            v, c, d = TAY_TRUOC[s]
            ik(P, v, c, tg(Pg, c, ngon_tip(s, c)))

    def ngon_quap(P, side, k):
        """quặp (k > 0) / xoè (k < 0) các ngón tay phụ của mình: xoay xương gốc ngón 30° × k (dấu theo bên), ngón sau trễ biên độ chút."""
        dau = 1.0 if side == "L" else -1.0
        for j, b in enumerate(sk.info.get("ngon", {}).get(side, [])):
            P.rot(b, dau * (30.0 - 4.0 * j) * k)

    # ------------------------------------------------ idle: SÓNG MỀM lệch pha dựng từ dáng tĩnh (người dùng chê idle tatu "giật, không mềm mại")
    # Không dùng chuyển động gốc trong idle (không có nhịp snap): dáng khung 0 của idle_01 + thở bằng tỉ lệ 1 ± 2 % chu kỳ 2 s, đầu trễ 0,1 s,
    # vai / tay phụ / ngón / khố trễ thêm 0,15–0,35 s, biên độ nhỏ, mọi sóng chu kỳ 2 s hoặc 4 s (khép vòng 4 s); nắm đấm giữ đất (IK);
    # trò riêng: tay phụ nửa phải tranh gãi đầu CHẬM 2,20 → 3,60 s (vào / ra 0,5 s êm, hai nhịp gãi 0,5 s).
    D_IDLE = 4.0
    G0, G1, GV = 1.80, 3.90, 0.75

    def em(u):                                                          # bậc năm: vận tốc và gia tốc bằng 0 ở hai đầu
        u = min(1.0, max(0.0, u))
        return u * u * u * (u * (6 * u - 15) + 10)
    KHO = ("bone57", "bone58", "bone59", "bone60", "bone67", "bone68", "bone69", "bone70")

    def song_(t, tre, chu=2.0):
        return math.sin(2 * math.pi * (t - tre) / chu)

    def f_idle(t, P):
        dat(P, "idle_01", 0.0)
        Pg = P.copy()
        b = song_(t, 0.0)
        P.scale("bone12", 1 + 0.010 * b, 1 + 0.020 * b)              # ngực phồng xẹp
        P.move("bone", 0.0, 5.0 * b)                                   # hông nhấp nhô nhẹ theo nhịp thở
        P.rot("bone11", 0.8 * song_(t, 0.05))
        P.rot("bone14", 1.2 * song_(t, 0.10))                          # đầu trễ 0,1 s
        P.move("bone14", 0.0, 3.0 * song_(t, 0.10))
        for side, dau in (("R", -1.0), ("L", 1.0)):                     # tay phụ: gốc → ngọn trễ dần
            b1, b2, b3 = TAY_PHU[side]
            lech = 0.0 if side == "R" else 0.5                          # hai bên lệch nửa chu kỳ 4 s cho khỏi đối xứng
            P.rot(b1, dau * 2.5 * song_(t, 0.20 + lech, 4.0))
            P.rot(b2, dau * 3.5 * song_(t, 0.30 + lech, 4.0))
            P.rot(b3, dau * 4.5 * song_(t, 0.35 + lech, 4.0))
            ngon_quap(P, side, 0.22 * song_(t, 0.35 + lech, 4.0))
        for j, bn in enumerate(KHO):                                    # khố đung đưa, đốt dưới trễ hơn
            P.rot(bn, 2.0 * song_(t, 0.15 + 0.06 * (j % 4), 2.0))
        u = (t - G0) / (G1 - G0)
        if 0 < u < 1:
            e = em((t - G0) / GV) * em((G1 - t) / GV)
            Q = P.copy()
            dau_ = tg(Q, "bone14", DAU)
            tg_gai = t - G0 - GV                                        # gãi: hai nhịp nhỏ, vào / ra theo bao êm
            gai = 12.0 * math.sin(2 * math.pi * max(0.0, tg_gai) / 0.30) * em(tg_gai / 0.15) * em((G1 - GV - t) / 0.15)
            b1, b2, b3 = TAY_PHU["L"]
            ik(Q, b1, b2, dau_ + np.array([60.0 + gai, 30.0 + 0.4 * gai]), uon=1.0)
            Q.rot(b3, -20.0)
            ngon_quap(Q, "L", 0.55)
            Q.rot("bone14", -3.0)                                       # nghiêng đầu nhẹ về phía tay gãi
            chep(P, pha(P, Q, e))
        giu_dam(P, Pg)                                                  # hai nắm đấm chống đất đứng yên

    def f_walk(t, P):
        dat(P, "run_01", t, True)

    def f_hit(t, P):
        dat(P, "hit_01", t)

    def f_die(t, P):
        d = CD["die_01"][0]
        dat(P, "die_01", t)
        a = float(np.clip(1.0 - (t - d) / (TAN - 0.1), 0.0, 1.0))
        if a < 0.999:
            for sl in sk.slots:
                P.alpha[sl["name"]] = a

    # ------------------------------------------------ attack: liên hoàn ba nhịp
    def f_attack(t, P):
        dat(P, "skill_01", tmap(t, M_ATTACK))
        for tk, s in ((T_DAM1, 0.05), (T_DAM2, 0.05), (T_DAM3, 0.09)):     # giật nhẹ cả thân đúng khung chạm
            k = math.exp(-((t - tk) / 0.05) ** 2)
            P.scale("bone", 1 + s * k, 1 - 0.6 * s * k)

    # ------------------------------------------------ cast: giơ hai nắm đấm quá đầu, gồng, nện đất
    def f_cast(t, P):
        tau = tmap(t, M_CAST)
        dat(P, "skill_02", tau)
        if 0.40 < t < 0.64:                                   # gồng: hai dáng lệch 2,5° đổi nhau mỗi 2 khung
            r = hoat.rung(t, 0.40, 0.64, 2)
            P.rot("bone12", 2.5 * r)
            P.rot("bone14", -2.0 * r)
        k = math.exp(-((t - (T_NEN + 0.03)) / 0.06) ** 2)
        P.scale("bone", 1 + 0.06 * k, 1 - 0.08 * k)
        # điểm phát VFX: giữa hai nắm đấm, mặt đất
        Pm = P.copy()
        a, b = tg(Pm, "bone22", (100.0, 0.0)), tg(Pm, "bone18", (100.0, 0.0))
        P.move("mieng", float((a[0] + b[0]) / 2), 0.0)

    # ------------------------------------------------ skill: ôm tảng đá lớn dần, nện hai nhịp, tung
    def da_tam(t, P):
        """tâm và bán kính tảng đá (thế giới) ở giây t: trên đầu, lớn dần khi tụ, ngả theo thân lúc ngả, đẩy tới trước lúc tung."""
        dau = tg(P, "bone14", DAU)
        r = 70.0 + 150.0 * ease((t - T_TU0) / (T_TU1 - T_TU0), "out") if t > T_TU0 else 70.0
        c = dau + np.array([0.0, 120.0 + 0.9 * r])
        if t > T_NGA - 0.12:
            u = ease((t - (T_NGA - 0.12)) / (T_NEM - T_NGA + 0.12), "io")
            c = c + np.array([-70.0 + 230.0 * u, 40.0 * math.sin(math.pi * u)])
        return c, r

    def than_skill(t, P):
        # nền: idle khung 0; thân + hai tay trước theo skill_02 ở các nhịp nện; ngả ra sau rồi chồm tới lúc tung
        f_idle(0.0, P)                                                 # nền tĩnh = khung 0 idle (không lấy chuyển động gốc)
        bo = set(TAY_PHU["L"] + TAY_PHU["R"] + NGON["L"] + NGON["R"]) | {"bone23", "bone33"}
        w_nen = 0.0
        if T_TU1 - 0.40 < t < T_NGA:
            # hai nhịp nện: giơ (gốc 0,43) → nện (0,72), lặp hai lần, thu gọn
            if t < T_NEN1 + 0.12:
                tau = tmap(t, [(T_TU1 - 0.40, 0.0), (T_NEN1 - 0.07, 0.45, "io"), (T_NEN1, 0.72, "in"), (T_NEN1 + 0.12, 0.80, "out")])
            else:
                tau = tmap(t, [(T_NEN1 + 0.12, 0.80), (T_NEN2 - 0.09, 0.48, "io"), (T_NEN2, 0.72, "in"), (T_NGA, 0.95, "out")])
            Q = khung.Pose()
            dat(Q, "skill_02", tau, bo=bo)
            w = ease((t - (T_TU1 - 0.40)) / 0.20) if t < T_TU1 - 0.20 else (1.0 if t < T_NGA - 0.1 else ease((T_NGA - t) / 0.1))
            w_nen = w
            chep(P, pha(P, Q, w, chi=set(Q.t) - bo))
        if t >= T_NGA - 0.2:
            u1 = ease((t - (T_NGA - 0.2)) / 0.2) if t < T_NGA else 1.0
            u2 = ease((t - T_NGA) / (T_NEM - T_NGA), "in") if t > T_NGA else 0.0
            u3 = ease((t - (T_NEM + 0.12)) / (D_SKILL - 0.25 - T_NEM - 0.12), "io") if t > T_NEM + 0.12 else 0.0
            lean = (-13.0 * u1 + 32.0 * u2) * (1 - u3)
            P.rot("bone11", lean)
            P.rot("bone14", -0.35 * lean)
            P.move("bone", 70.0 * (u2 - 0.6 * u1) * (1 - u3), -25.0 * u1 * (1 - u3) - 30.0 * u2 * (1 - u3))
            kk = math.exp(-((t - (T_NEM + 0.03)) / 0.05) ** 2)
            P.scale("bone", 1 + 0.07 * kk, 1 - 0.09 * kk)
        # gồng lúc tụ: thân rung nhẹ hai dáng
        if T_TU0 + 0.3 < t < T_TU1:
            r = hoat.rung(t, T_TU0 + 0.3, T_TU1, 2)
            P.rot("bone12", 1.5 * r)
        Pg = khung.Pose()
        dat(Pg, "idle_01", 0.0)
        if w_nen < 0.999:                                     # nắm đấm chống đất giữ chỗ (IK), hoà dần ra khi vào đoạn nện
            Pk = P.copy()
            giu_dam(Pk, Pg)
            chep(P, pha(P, Pk, 1.0 - w_nen))

    def f_skill(t, P):
        than_skill(t, P)
        c, r = da_tam(t, P)
        # hai tay phụ: giơ dần lên ôm hai bên tảng đá, ngón quặp; lúc tung đẩy theo tảng đá; xong buông về idle
        up = ease((t - T_TU0) / 0.45, "io") if t > T_TU0 else 0.0
        ve = ease((t - (T_NEM + 0.10)) / 0.45, "io") if t > T_NEM + 0.10 else 0.0
        w = up * (1 - ve)
        if w > 1e-3:
            Q = P.copy()
            for side, dx in (("R", -1.0), ("L", 1.0)):
                b1, b2, b3 = TAY_PHU[side]
                dich = c + np.array([dx * (r * 0.95 + 30.0), -0.15 * r])
                if t > T_NEM:                                   # buông: tay vung theo đà về trước
                    dich = dich + np.array([140.0 * ease((t - T_NEM) / 0.25, "out"), -60.0 * ease((t - T_NEM) / 0.25, "out")])
                ik(Q, b1, b2, dich, uon=(1.0 if side == "L" else -1.0))
                Q.rot(b3, (-1.0 if side == "L" else 1.0) * 35.0)
                ngon_quap(Q, side, 0.9 if t < T_NEM else 0.9 - 1.3 * ease((t - T_NEM) / 0.12))
            chep(P, pha(P, Q, w))
        # xương mieng = tâm tảng đá (tỉ lệ = bán kính / 100) tới lúc tung
        P.move("mieng", float(c[0]), float(c[1]))
        sc = max(0.02, r / 100.0) if t < T_NEM + 0.02 else 0.02
        P.scale("mieng", sc, sc)

    # ------------------------------------------------ appear: nhảy xuống, đáp, đứng dậy, đấm ngực bốn tay, gầm
    def f_appear(t, P):
        D3 = CD["skill_03"][0]
        if t < T_DAP:                                          # đang rơi: dáng bay (gốc 1,38), từ trên cao xuống
            dat(P, "skill_03", 1.30 + 0.12 * (t / T_DAP))
            u = t / T_DAP
            P.move("move", 0.0, 1.15 * cao * (1 - u * u))
            for sl in sk.slots:
                P.alpha[sl["name"]] = min(1.0, t / 0.12)
            return
        if t < T_DUNG0:                                        # đáp: dáng đáp (gốc 1,61 → 1,84) + bẹp nảy
            dat(P, "skill_03", tmap(t, [(T_DAP, 1.58), (T_DAP + 0.12, 1.70, "out"), (T_DUNG0, 1.84, "io")]))
            b = math.exp(-(t - T_DAP) / 0.08) * math.cos((t - T_DAP) * 2 * math.pi / 0.2)
            P.scale("bone", 1 + 0.10 * b, 1 - 0.12 * b)
            return
        # đứng dậy: hoà dáng cuối skill_03 → idle 0
        Pa = khung.Pose()
        dat(Pa, "skill_03", min(D3, 1.84 + (t - T_DUNG0) * 0.9))
        Pb = khung.Pose()
        f_idle(0.0, Pb)
        w = ease((t - T_DUNG0) / (T_DUNG1 - T_DUNG0), "io")
        chep(P, pha(Pa, Pb, w))
        if T_NGUC[0] - 0.14 < t < T_GAM0 + 0.05:
            # đấm ngực: mỗi tay vào ngực ở mốc của nó (so le), đánh ra rồi về; tay trước giữ nắm đấm chạm ngực bằng IK
            nguc = tg(P, "bone12", NGUC)
            Q = P.copy()
            for j, (kind, side) in enumerate((("truoc", "R"), ("truoc", "L"), ("phu", "R"), ("phu", "L"), ("truoc", "R"))):
                tk = T_NGUC[j]
                k = math.exp(-((t - tk) / 0.07) ** 2)
                if k < 1e-3:
                    continue
                if kind == "truoc":
                    v, c, d = TAY_TRUOC[side]
                    dich = nguc + np.array([(-50.0 if side == "R" else 50.0), 10.0])
                    Qa = Q.copy()
                    ik(Qa, v, c, dich)
                    Qa.rot(d, (25.0 if side == "R" else -25.0))
                    Q = pha(Q, Qa, min(1.0, 1.5 * k))
                    if side == "L" and k > 0.12:
                        for s_ in ("vai_L", "canh_L", "dam_L"):
                            Q.alpha[s_] = 0.0
                            Q.alpha[s_ + "~t"] = 1.0
                else:                                          # tay phụ vỗ mạnh xuống đỉnh vai cùng bên
                    b1, b2, b3 = TAY_PHU[side]
                    vai = tg(Q, TAY_TRUOC[side][0])
                    dich = vai + np.array([(-40.0 if side == "R" else 40.0), 150.0 - 60.0 * k])
                    Qa = Q.copy()
                    ik(Qa, b1, b2, dich, uon=(1.0 if side == "L" else -1.0))
                    ngon_quap(Qa, side, 0.8)
                    Q = pha(Q, Qa, min(1.0, 1.4 * k))
                ky = math.exp(-((t - tk - 0.02) / 0.035) ** 2)        # ngực nảy, đầu giật đúng lúc tay chạm
                Q.scale("bone12", 1 + 0.035 * ky, 1 - 0.025 * ky)
                Q.rot("bone14", (4.0 if j % 2 else -4.0) * ky)
            chep(P, Q)
        if t > T_GAM0 - 0.1:                                   # gầm: dáng dang tay của skill_02 (gốc 0,95), ngửa đầu, rung
            w = ease((t - (T_GAM0 - 0.1)) / 0.18) if t < T_GAM1 else 1 - ease((t - T_GAM1) / (D_APPEAR - 0.05 - T_GAM1))
            Q = khung.Pose()
            dat(Q, "skill_02", 0.95)
            Q.rot("bone14", 14.0)
            Q.rot("bone11", -5.0)
            if T_GAM0 < t < T_GAM1:
                r = hoat.rung(t, T_GAM0, T_GAM1, 2)
                Q.rot("bone12", 2.0 * r)
            chep(P, pha(P, Q, max(0.0, min(1.0, w))))

    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=[(T_DAP, "cham_dat", ""), *[(tk, "dam_nguc", "") for tk in T_NGUC], (T_GAM0, "gam", "")]),
        Clip("idle", D_IDLE, f_idle, loop=True, ev=[(1.0, "soi_roi", "")]),
        Clip("walk", CD["run_01"][0], f_walk, loop=True),
        Clip("attack", D_ATTACK, f_attack, ev=[(T_DAM1, "dam1", ""), (T_DAM2, "dam2", ""), (T_DAM3, "trung", "")], trung=T_DAM3),
        Clip("cast", D_CAST, f_cast, ev=[(T_NEN, "nen", ""), (T_NEN, "trung", "")], trung=T_NEN),
        Clip("skill", D_SKILL, f_skill, ev=[(T_TU0, "tu", ""), (T_NEN1, "nen", ""), (T_NEN2, "nen", ""), (T_NEM, "nem", ""),
                                             (T_NEM, "trung", "")], trung=T_NEM),
        Clip("hit", CD["hit_01"][0], f_hit),
        Clip("die", CD["die_01"][0] + TAN, f_die),
    ]
    return clips


# ---------------------------------------------------------------- bộ mảnh tạm bằng da gốc
def goc_tam():
    """mỗi mảnh của mình vẽ bằng các part gốc tương ứng ở khung 0 idle, đặt về px concept (nghịch phép căn) → manh_goc/ + dat.json:
    để dựng thử rig, clip khi tờ mảnh GPT chưa về."""
    from quai.soi import _tris
    ra = os.path.join(G.BASE, "manh_goc")
    os.makedirs(ra, exist_ok=True)
    _, imgs, atts = G.nap("att_idle0.json")
    bys = {a["slot"]: a for a in atts}
    _, _, to_px = tf()
    DATJ = {}
    nhom = dict(MANH_GOC)
    for side in "LR":
        for k, grp in enumerate(NGON_GOC[side], 1):
            nhom[f"ngon_{side}{k}"] = grp
    for ten_m, grp in nhom.items():
        lay = Image.new("RGBa", (1536, 1024), (0, 0, 0, 0))
        for s in grp:
            a = bys[s]
            im = G.part_goc(a)
            uv, tr = G.luoi(a)
            _tris(lay, im.convert("RGBa"), to_px(np.array(a["xy"], float).reshape(-1, 2)), uv, tr)
        lay = lay.convert("RGBA")
        bb = lay.getbbox()
        lay.crop(bb).save(os.path.join(ra, ten_m + ".png"))
        DATJ[ten_m] = dict(hop=[bb[0], bb[1], bb[2], bb[3]], nguon="da gốc")
    json.dump(DATJ, open(os.path.join(ra, "dat.json"), "w"), indent=1)
    print(ra, len(DATJ))


def main(a):
    if a and a[0] == "goc_tam":
        goc_tam()
        return
    sk, info = dung()
    clips = lam_clip(sk, info)
    ve0 = soi.Ve(sk)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0)
    clips = lam_clip(sk, info, cao)
    print(f"chiều cao {cao:.0f}")
    if a and a[0] == "kiem":
        for c in clips:
            fr = hoat.nuong(sk, c)
            xau = []
            for i in range(1, len(fr)):
                A, B = fr[i - 1], fr[i]
                for b in set(A.t) | set(B.t):
                    da = abs(B.t.get(b, khung.ZERO)[2] - A.t.get(b, khung.ZERO)[2])
                    if da > 35.0 and b != "mieng":
                        xau.append(f"{i / 30:.2f}s {b} xoay {da:.0f}°")
            Wl = [sk.the_gioi(P) for P in fr]
            for b in ("bone14", "bone18", "bone22", "bone26", "bone36", "bone12"):
                for i in range(1, len(fr)):
                    d = float(np.hypot(*(Wl[i][b][:2, 2] - Wl[i - 1][b][:2, 2])))
                    if d > 0.22 * cao and c.ten != "appear":
                        xau.append(f"{i / 30:.2f}s {b} dời {d / cao:.2f} cao/khung")
            print(f"{c.ten}: {len(fr)} khung" + ("" if not xau else " | " + "; ".join(xau[:14]) + (" ..." if len(xau) > 14 else "")))
            if c.ten == "idle":                                          # độ mềm: vận tốc góc, gia tốc góc (độ / khung²), vận tốc điểm
                ten_x = sorted(set().union(*[set(P.t) for P in fr]))
                A = np.array([[P.t.get(b, khung.ZERO)[2] for b in ten_x] for P in fr])
                v = np.diff(A, axis=0)
                a_ = np.diff(v, axis=0)
                top = sorted(zip(np.abs(a_).max(0), np.abs(v).max(0), ten_x), reverse=True)[:6]
                print("  idle: gia tốc góc lớn nhất (độ/khung²), vận tốc góc lớn nhất (độ/khung): " +
                      ", ".join(f"{b} {aa:.2f}/{vv:.2f}" for aa, vv, b in top))
                Pp = np.array([[Wl[i][b][:2, 2] for b in ("bone14", "bone26", "bone36", "bone18", "bone22")] for i in range(len(fr))])
                vp = np.linalg.norm(np.diff(Pp, axis=0), axis=2)
                ap = np.linalg.norm(np.diff(Pp, n=2, axis=0), axis=2)
                print("  idle: điểm (đầu, hai lòng tay phụ, hai nắm đấm) vận tốc max " + " ".join(f"{x:.1f}" for x in vp.max(0)) +
                      " đv/khung, gia tốc max " + " ".join(f"{x:.2f}" for x in ap.max(0)))
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
        sc = float(a[3]) if len(a) > 3 else 0.25
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
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de="Vượn núi đá bốn tay (quy_nui_1): tướng 5 đảo Thổ", dang=1, so_dang=1,
                  dung_yen=("cast", "skill"), lao=(), far=(), ma_goc=None, khop_idle=0.2, cao=cao, impact=IMPACT,
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.4, tran_mb=0.7, span=3.4)


if __name__ == "__main__":
    main(sys.argv[1:])
