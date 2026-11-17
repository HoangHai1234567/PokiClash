# -*- coding: utf-8 -*-
"""Thạch Giáp DẠNG 2 (cong_da_2; tướng 1 đảo Thổ, ải 1): hình của mình chạy trên ĐÚNG rig con gốc monster_3528 (game tham khảo). Ghi chú
inbox/cong_da_2_ghichu.md. Cách làm như cong_da_rig.py (dạng 1, rig 3378):
- XƯƠNG: đủ mọi xương của họ, thêm `move` (cú lao), `day` (đáy chân: nhún, nảy), `tam` (tâm núi đá: nghiêng; cha của `all`), `pha_le`
  (cụm pha lê đỉnh), `ph_t` / `ph_p` (cụm pha lê hốc trái / phải), `mat` (con mắt: chớp), `mieng` (chóp mõm: điểm phát VFX).
- MẢNH (cong_da2_manh.py → inbox/cong_da_2/manh/): đặt vào thế giới rig ở dáng idle 0 theo chỗ trên concept (concept to hơn con gốc ~1,2
  lần) rồi bám như điểm tương ứng trên lưới của họ:
    mai  (núi đá trên)  bám MỀM nhiều khối fangkuai_4 / _1 / _5 / _6 / __2 / __3 (mỗi đỉnh theo khối gần nhất, hoà ở mép giữa hai khối)
    tou  (thân + đầu)   bám mềm lưới tou (xích đầu fangkuai__2) + lưới yao (thân)
    vay  (váy đá dưới)  cứng trên `yao` (gốc chân, thân); chân cứng trên xương chân dưới của họ; đuôi theo lưới weiba_1
  Lớp (sau → trước): bốn chân < mầm pha lê đỉnh trái (gốc khuất sau mép mai) < mai < váy < thân + đầu < mắt < đuôi < vay_truoc (lưới con của váy che gốc đuôi) < mỗi cụm pha lê
  rồi ngay sau nó nửa vành trước của hốc (vanh_d / vanh_t / vanh_p: lưới con của mai, lỗ hai lớp)
  (người dùng 2026-11-17: thân tatu nằm TRƯỚC váy đá dưới; thân là mảnh liền gen lại M6, không đuôi).
- CHUYỂN ĐỘNG (giống ý dạng 1, mạnh hơn; clip gốc 3528 làm nền):
    appear = núi đá rơi phịch, nảy → chân, đầu, đuôi bật ra, rũ mình, cau mày
    idle   = idle_01 khung 0 + sóng mềm lệch pha 2 s; trò: đầu thò ra hít hít rồi rụt nhẹ, tai giật, chớp mắt, đuôi vẫy
    walk   = run_01 (chân của họ vung rất xa: bớt còn 45 % vì chân ngắn dưới váy)
    attack = skill_01_3 (ngửa lấy đà, LAO HÚC chúi đầu xuống), quãng tới dồn vào `move`
    cast   = skill_01_2 (chồm đứng lên) + LẮC NÚI ĐÁ: ba cụm pha lê (hốc trái, hốc phải, mảnh nhỏ đỉnh) rời hốc bay găm vào đối thủ
             (mảnh của rig, xương far + fly_*, game lái), DẬM xuống, cụm bay về lắp lại
    skill  = rụt chân, hạ sát đất, núi đá rung lạch cạch (gồng) → cụm pha lê đỉnh vọt lên trời (ban_troi) → đứng dậy chĩa mõm, mưa pha lê
             (mua, VFX), mảnh to cắm xuống (trung), cụm mọc lại (moc)
    hit = hit_01; die = die_01 + sụp + mờ
Xương, lưới và chuyển động gốc là của nhà phát hành game gốc; hình là của mình. Dùng nội bộ, không đăng công khai.

    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/cong_da2_rig.py        → inbox/cong_da_2/rig/
    py -3 -I ArtGen/Spine/cong_da2_rig.py soi <clip> <giây,...|n=12|t0:t1:n> [tỉ lệ]          → rig/soi_<clip>.png
    py -3 -I ArtGen/Spine/cong_da2_rig.py kiem                                                  (đo góc nhảy, bước dời)
    py -3 -I ArtGen/Spine/cong_da2_rig.py diem                                                  (vị trí xương theo giờ clip, cho HatTho.cs)
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
import cong_da_rig as R1  # noqa: E402  (trong_so_goc, mats; nhập vào thì hoa_ho trỏ dạng 1 → đặt lại dạng 2 ngay dưới)
import tho5_dang2  # noqa: E402
from hoa_ho_rig import ease, tmap, _goc  # noqa: E402

G = tho5_dang2.dat2("cong_da")
TEN_RIG = "cong_da_2"
D_PX = float(os.environ.get("CD2_DPX", "0.9"))          # pixel ảnh atlas cho mỗi đơn vị rig (0,9: .atomik 287 KB < đích 0,3 MB)
MANH = os.path.join(G.BASE, "manh")
RA = os.environ.get("CD2_RA") or os.path.join(G.BASE, "rig")
TAN = 0.45
FPS = 30.0
IMPACT = {"attack": (0.08, 0.45, 0.10), "cast": (0.07, 0.48, 0.10), "skill": (0.16, 0.85, 0.20, "#ffffff40")}   # mạnh hơn dạng 1

SLOT = ["jiao_r", "shou_r", "jiao_l", "shou_l", "yezi_1", "mai", "vay", "tou", "yankuang", "weiba_1", "vay_truoc", "tinh_the", "vanh_d",
        "phach_t", "vanh_t", "phach_p", "vanh_p"]                                         # người dùng 2026-11-17: thân + đầu TRƯỚC váy đá; đuôi trước thân, gốc chui dưới mép tấm váy trái
KHOI = ["fangkuai_4", "fangkuai_1", "fangkuai_5", "fangkuai_6", "fangkuai__2", "fangkuai__3"]   # khối của họ mà mai bám
CHAN = ("jiao_l", "shou_l", "jiao_r", "shou_r")
DUI = ("yao2", "yao4", "yao3", "yao5")                   # đùi của từng chân (cha của xương chân dưới)
DAU = "fangkuai__2"                                       # xích đầu của họ (tou, mắt, khối trước phải)


# ---------------------------------------------------------------- nạp
def nap():
    scan = G.scan()
    rd = lambda f: json.load(open(os.path.join(scan, f), encoding="utf-8"))
    return rd("att_goc.json"), rd("att_idle0.json"), rd("info.json"), rd("sample_goc.json")


def tf():
    j = json.load(open(os.path.join(G.MAU, "goc_ca_con.json")))
    s, cx, cy = j["s"], j["cx"], j["cy"]
    to_rig = lambda P: np.stack([cx + (P[:, 0] - 768) / s, cy - (P[:, 1] - 512) / s], 1)
    to_px = lambda V: np.stack([768 + (V[:, 0] - cx) * s, 512 - (V[:, 1] - cy) * s], 1)
    return s, to_rig, to_px


def anh_manh(ten):
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    s_px, _, _ = tf()
    g = Image.open(os.path.join(MANH, ten + ".png")).convert("RGBA")
    hop = DATJ[ten]["hop"]
    kq = D_PX / s_px
    g = g.convert("RGBa").resize((max(2, round(g.width * kq)), max(2, round(g.height * kq))), Image.LANCZOS).convert("RGBA")
    return anh.loang_mau(g), hop, kq


def _bone_of(a0, ten):
    b = a0.get("bone")
    return ten[b] if isinstance(b, int) else b


def _cung(V, b, Wi):
    return [[(b, *[float(q) for q in np.linalg.solve(Wi[b], np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]


WI = {}                                                  # thế giới KHUNG 0 IDLE của mọi xương (của họ: att_idle0; xương thêm: tính theo cha)


def xuong_idle(sk, b, cha, p, goc_tg=0.0):
    """xương thêm b con của cha, đặt sao cho Ở KHUNG 0 IDLE nó nằm ở p (thế giới) với trục x theo góc goc_tg: mảnh cứng trên nó tính toạ
    độ theo thế giới idle (như lưới của họ), không lệch khi idle_01 dời các xương khỏi dáng gốc."""
    Wp = WI[cha]
    lp = np.linalg.solve(Wp, np.array([p[0], p[1], 1.0]))
    d = np.linalg.solve(Wp[:2, :2], np.array([math.cos(math.radians(goc_tg)), math.sin(math.radians(goc_tg))]))
    rot = math.degrees(math.atan2(d[1], d[0]))
    sk.xuong(b, cha, float(lp[0]), float(lp[1]), goc=rot)
    WI[b] = Wp @ khung.mat(float(lp[0]), float(lp[1]), rot)


def _kc_da_giac(p, a0):
    """khoảng cách (đơn vị rig) từ p tới bao lồi các đỉnh hình a0 (0 nếu ở trong)."""
    Q = np.array(a0["xy"], np.float32).reshape(-1, 2)
    hull = cv2.convexHull(Q)
    d = cv2.pointPolygonTest(hull, (float(p[0]), float(p[1])), True)
    return max(0.0, -float(d))


def bam_nhieu(V, cands, by0, ten, Wi, sigma=14.0, dai=40.0, chon=None):
    """mỗi đỉnh V bám như hình gần nhất trong cands (lưới có trọng số: theo lưới, như trong_so_goc; hình cứng: cứng trên xương của nó);
    trong dải `dai` đơn vị quanh hình gần nhất thì hoà các hình khác theo exp(-Δd / sigma) cho khỏi gãy ở mép giữa hai khối."""
    rows_c = {}
    chon = chon or [cands] * len(V)
    for c in cands:
        a0 = by0[c]
        rows_c[c] = R1.trong_so_goc(V, a0, ten, Wi) if a0.get("w") else _cung(V, _bone_of(a0, ten), Wi)
    out = []
    for i, p in enumerate(V):
        d = {c: _kc_da_giac(p, by0[c]) for c in chon[i]}
        dm = min(d.values())
        ws = {c: math.exp(-(d[c] - dm) / sigma) for c in d if d[c] <= dm + dai}
        tong = sum(ws.values())
        gop = {}
        for c, wc in ws.items():
            for n, x, y, w in rows_c[c][i]:
                k = w * wc / tong
                if k < 1e-6:
                    continue
                g = gop.setdefault(n, [0.0, 0.0, 0.0])
                g[0] += k * x
                g[1] += k * y
                g[2] += k
        out.append([(n, g[0] / g[2], g[1] / g[2], g[2]) for n, g in gop.items()])
    return out


def gan_manh(sk, slot, a0s, ten, Wi, cach, xuong=None):
    """mảnh `slot` thành lưới đặt đúng chỗ concept ở dáng idle 0. cach: "cung" (cứng trên xuong), "goc" (theo lưới a0s[0]), "nhieu"
    (bam_nhieu trên a0s)."""
    im, (x0, y0, x1, y1), kq = anh_manh(slot)
    sk.anh(slot, im)
    im = sk.images[slot]
    _, to_rig, _ = tf()
    if cach == "cung":
        L = luoi.luoi_o(im.width, im.height, 2, 2, ten=slot)
    else:
        L = luoi.luoi_vung(im, buoc_vien=10.0, buoc_trong=16.0, vien=2, ten=slot, in_tk=False)
    V = to_rig(np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1))
    if cach == "cung":
        rows = _cung(V, xuong, WI)
    elif cach == "goc":
        rows = R1.trong_so_goc(V, a0s[0], ten, Wi)
    else:
        rows = bam_nhieu(V, a0s, None, ten, Wi) if False else None
    if rows is None:
        raise ValueError("cach")
    Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
    sk.luoi_gan(slot, slot, L, trongso.cung(L.n, "move"), the_gioi=Vs)
    sk.atts[slot][slot]["verts"] = rows
    return L, V


def gan_nhieu(sk, slot, cands, by0, ten, Wi, chon=None):
    im, (x0, y0, x1, y1), kq = anh_manh(slot)
    sk.anh(slot, im)
    im = sk.images[slot]
    _, to_rig, _ = tf()
    L = luoi.luoi_vung(im, buoc_vien=10.0, buoc_trong=16.0, vien=2, ten=slot, in_tk=False)
    Px = np.stack([x0 + L.pts[:, 0] / kq, y0 + L.pts[:, 1] / kq], 1)
    V = to_rig(Px)
    rows = bam_nhieu(V, cands, by0, ten, Wi, chon=[chon(q) for q in Px] if chon else None)
    Vs = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows])
    sk.luoi_gan(slot, slot, L, trongso.cung(L.n, "move"), the_gioi=Vs)
    sk.atts[slot][slot]["verts"] = rows
    return L, rows


def xuong_troi(rows_mai, V_mai, p):
    """xương nặng nhất của mai ở đỉnh gần p nhất (để đặt cha cho cụm pha lê)."""
    i = int(np.argmin(np.hypot(*(V_mai - p).T)))
    return max(rows_mai[i], key=lambda r: r[3])[0]


# ---------------------------------------------------------------- dựng
def dung():
    D, D0, I, S = nap()
    IB = I["bones"]
    ten = [b["name"] for b in IB]
    Wi = R1.mats(D0)
    WI.clear()
    WI.update(Wi)
    by0 = {a["slot"]: a for a in D0["atts"]}
    _, to_rig, _ = tf()
    DATJ = json.load(open(os.path.join(MANH, "dat.json")))
    hm = DATJ["mai"]["hop"]
    Vm = to_rig(np.array([[hm[0], hm[1]], [hm[2], hm[3]]], float))
    y_day = float(min(to_rig(np.array([[0.0, DATJ[c]["hop"][3] - 6.0]]))[0, 1] for c in CHAN))
    tam = np.array([float(Vm[:, 0].mean()), float(Vm[:, 1].mean())])
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
    tong = [0, 0]

    def dem(L):
        tong[0] += L.n
        tong[1] += len(L.tris)

    for s in SLOT:
        if s not in DATJ:
            print(f"  (thiếu mảnh) bỏ slot {s}")
    # mai trước (cụm pha lê lấy cha theo nó)
    sk.slot("jiao_r", "move", "jiao_r")
    sk.slot("shou_r", "move", "shou_r")
    sk.slot("jiao_l", "move", "jiao_l")
    sk.slot("shou_l", "move", "shou_l")
    for c in ("jiao_r", "shou_r", "jiao_l", "shou_l"):
        L, _ = gan_manh(sk, c, None, ten, Wi, "cung", xuong=_bone_of(by0[c], ten))
        dem(L)
    # mầm pha lê nhỏ đỉnh trái: SAU mai (concept: gốc mầm khuất sau mép tấm; rig gốc cũng để yezi sau các khối)
    sk.slot("yezi_1", "move", "yezi_1")
    L, _ = gan_manh(sk, "yezi_1", None, ten, Wi, "cung", xuong="yezi_2")
    dem(L)
    sk.slot("mai", "move", "mai")
    # vùng đỉnh mai (hốc pha lê trên, y concept < 280) chỉ bám khối sau fangkuai_4: cụm pha lê đỉnh khỏi trượt khỏi hốc khi xích đầu
    # (khối trước phải fangkuai_1) lắc khác khối sau
    Lm, rows_mai = gan_nhieu(sk, "mai", KHOI, by0, ten, Wi, chon=lambda q: ["fangkuai_4"] if q[1] < 280 else KHOI)
    dem(Lm)
    V_mai = np.array([sum(w * (WI[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows_mai])   # chỗ ở khung 0 idle
    # xương `dau` (con của xích đầu, ở giữa đầu): mọi động tác RIÊNG của đầu (thò, hít, gật) đi qua nó, không kéo núi đá theo
    ht = DATJ["tou"]["hop"]
    xuong_idle(sk, "dau", DAU, to_rig(np.array([[930.0, 620.0]]))[0], 0.0)
    sk.slot("vay", "move", "vay")
    L, _ = gan_manh(sk, "vay", None, ten, Wi, "cung", xuong="yao")
    dem(L)
    sk.slot("tou", "move", "tou")
    L, rows_tou = gan_nhieu(sk, "tou", ["tou", "yao"], by0, ten, Wi)
    inv_d = np.linalg.inv(WI["dau"])
    sk_rows = []
    for r in rows_tou:                                     # phần bám xích đầu (fangkuai__2 / __5 / __6) chuyển sang `dau`
        gop, dd = [], [0.0, 0.0, 0.0]
        for n, x, y, ww in r:
            if n in (DAU, "fangkuai__5", "fangkuai__6"):
                q = inv_d @ (Wi[n] @ np.array([x, y, 1.0]))
                dd[0] += ww * q[0]
                dd[1] += ww * q[1]
                dd[2] += ww
            else:
                gop.append((n, x, y, ww))
        if dd[2] > 1e-6:
            gop.append(("dau", dd[0] / dd[2], dd[1] / dd[2], dd[2]))
        sk_rows.append(gop)
    sk.atts["tou"]["tou"]["verts"] = sk_rows
    sk.atts["tou"]["tou"]["V"] = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in sk_rows])
    dem(L)
    # con mắt: xương `mat` con của `dau` ở tâm mắt (chớp = bóp dọc)
    hy = DATJ["yankuang"]["hop"]
    cm = to_rig(np.array([[(hy[0] + hy[2]) / 2.0, (hy[1] + hy[3]) / 2.0]]))[0]
    xuong_idle(sk, "mat", "dau", cm, 0.0)
    sk.slot("yankuang", "move", "yankuang")
    L, _ = gan_manh(sk, "yankuang", None, ten, Wi, "cung", xuong="mat")
    dem(L)
    # đuôi: chuỗi xương riêng duoi1 → duoi3 (gốc ở chỗ đuôi chui dưới tấm váy trái, con của yao); đuôi gốc của họ dài, khớp ở xa nên
    # lắc thì gốc đuôi trồi khỏi váy. Trọng số mềm theo khoảng cách tới gốc từng đốt (exp(-d / 28 px concept)).
    D_PX_DUOI = [(505.0, 858.0), (556.0, 880.0), (603.0, 846.0)]
    for k, (pp, q) in enumerate(zip(D_PX_DUOI, D_PX_DUOI[1:] + [(640.0, 815.0)])):
        a_, b_ = to_rig(np.array([pp, q]))
        g_ = math.degrees(math.atan2(b_[1] - a_[1], b_[0] - a_[0]))
        xuong_idle(sk, f"duoi{k + 1}", "yao" if k == 0 else f"duoi{k}", a_, g_)
    sk.slot("weiba_1", "move", "weiba_1")
    im_d, (dx0, dy0, _, _), kq_d = anh_manh("weiba_1")
    sk.anh("weiba_1", im_d)
    Ld = luoi.luoi_vung(sk.images["weiba_1"], buoc_vien=8.0, buoc_trong=12.0, vien=2, ten="weiba_1", in_tk=False)
    Pd = np.stack([dx0 + Ld.pts[:, 0] / kq_d, dy0 + Ld.pts[:, 1] / kq_d], 1)
    Vd = to_rig(Pd)
    rows_d = []
    for pp, vv in zip(Pd, Vd):
        ws_ = np.array([math.exp(-math.hypot(pp[0] - c[0], pp[1] - c[1]) / 28.0) for c in D_PX_DUOI])
        ws_ /= ws_.sum()
        rows_d.append([(f"duoi{k + 1}", *[float(q) for q in np.linalg.solve(WI[f"duoi{k + 1}"], np.array([vv[0], vv[1], 1.0]))[:2]],
                        float(w_)) for k, w_ in enumerate(ws_) if w_ > 0.01])
        tot = sum(r[3] for r in rows_d[-1])
        rows_d[-1] = [(n_, x_, y_, w_ / tot) for n_, x_, y_, w_ in rows_d[-1]]
    Vs_d = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows_d])
    sk.luoi_gan("weiba_1", "weiba_1", Ld, trongso.cung(Ld.n, "move"), the_gioi=Vs_d)
    sk.atts["weiba_1"]["weiba_1"]["verts"] = rows_d
    dem(Ld)
    # lớp hai của váy: LƯỚI CON trên chính ảnh `vay` (cùng điểm ảnh, cùng cứng trên yao → trùng khít, không lộ mép), chỉ phủ vùng che
    # gốc đuôi chui dưới tấm váy trái (cong_da2_manh.sua_lop → manh/vay_truoc_mask.png, toạ độ ảnh váy trên concept)
    sk.slot("vay_truoc", "move", "vay")
    im_v, (vx0, vy0, _, _), kq_v = anh_manh("vay")
    mk = Image.open(os.path.join(MANH, "vay_truoc_mask.png")).convert("L").resize(im_v.size, Image.BILINEAR)
    Lt = luoi.luoi_vung(np.asarray(mk) > 127, buoc_vien=8.0, buoc_trong=12.0, vien=3, ten="vay_truoc", in_tk=False)
    Vt = to_rig(np.stack([vx0 + Lt.pts[:, 0] / kq_v, vy0 + Lt.pts[:, 1] / kq_v], 1))
    rows_t = _cung(Vt, "yao", WI)
    Vs_t = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows_t])
    sk.luoi_gan("vay_truoc", "vay", Lt, trongso.cung(Lt.n, "move"), the_gioi=Vs_t)
    sk.atts["vay_truoc"]["vay"]["verts"] = rows_t
    dem(Lt)
    # pha lê: xương riêng ở chân cụm, con của khối mai nặng nhất tại đó; trục x chĩa LÊN thế giới (vọt lên trời / bay)
    # nửa vành trước của từng hốc (lỗ hai lớp: vành sau + lòng hốc trong mai → pha lê → vành trước): LƯỚI CON trên chính ảnh mai, bám mềm
    # y như mai (cùng bam_nhieu, cùng chọn khối) nên trùng khít từng điểm ảnh (cong_da2_manh.hoc_pha_le → manh/<vanh>_mask.png)
    im_m, (mx0, my0, _, _), kq_m = anh_manh("mai")
    chon_mai = lambda q: ["fangkuai_4"] if q[1] < 280 else KHOI
    VANH = {"tinh_the": "vanh_d", "phach_t": "vanh_t", "phach_p": "vanh_p"}

    def vanh_truoc(ten_v):
        mk = Image.open(os.path.join(MANH, ten_v + "_mask.png")).convert("L").resize(im_m.size, Image.BILINEAR)
        mk = np.asarray(mk) > 127
        if not mk.any():
            return
        sk.slot(ten_v, "move", "mai")
        Lv = luoi.luoi_vung(mk, buoc_vien=8.0, buoc_trong=12.0, vien=3, ten=ten_v, in_tk=False)
        Pv = np.stack([mx0 + Lv.pts[:, 0] / kq_m, my0 + Lv.pts[:, 1] / kq_m], 1)
        rows_v = bam_nhieu(to_rig(Pv), KHOI, by0, ten, Wi, chon=[chon_mai(q) for q in Pv])
        Vs_v = np.array([sum(w * (sk.W0[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in rows_v])
        sk.luoi_gan(ten_v, "mai", Lv, trongso.cung(Lv.n, "move"), the_gioi=Vs_v)
        sk.atts[ten_v]["mai"]["verts"] = rows_v
        dem(Lv)

    for s, b in (("tinh_the", "pha_le"), ("phach_t", "ph_t"), ("phach_p", "ph_p")):
        hp = DATJ[s]["hop"]
        goc = to_rig(np.array([[(hp[0] + hp[2]) / 2.0, hp[3] - 0.18 * (hp[3] - hp[1])]]))[0]
        cha = xuong_troi(rows_mai, V_mai, goc)
        xuong_idle(sk, b, cha, goc, 90.0)
        sk.slot(s, "move", s)
        L, _ = gan_manh(sk, s, None, ten, Wi, "cung", xuong=b)
        dem(L)
        vanh_truoc(VANH[s])
        print(f"  {s}: xương {b} con của {cha}; vành trước {VANH[s]}")
    # chóp mõm (điểm phát VFX): tìm điểm phải nhất của tou ở hàng mũi (concept ~ (1045, 650))
    mui = to_rig(np.array([[1045.0, 650.0]]))[0]
    xuong_idle(sk, "mieng", "dau", mui, 0.0)
    for e, m in (("trung", "khung trúng"), ("cham_dat", "chạm đất (appear, cast, skill)"),
                 ("phong", "cast: một cụm pha lê rời hốc bay tới đối thủ (chuỗi = a trái / b phải / c mảnh nhỏ)"),
                 ("ve", "cast: cụm pha lê bay về lắp lại hốc"), ("ran", "cast: lắc núi đá (VFX bụi, sỏi rơi)"),
                 ("gong", "skill: rụt chân gồng, núi đá rung (VFX bụi dưới chân)"), ("ban_troi", "skill: cụm pha lê đỉnh vọt lên trời"),
                 ("moc", "skill: cụm pha lê mọc lại"), ("mua", "skill: mưa pha lê rơi xuống đối thủ (VFX)"),
                 ("bung", "appear: chân, đầu bật ra khỏi núi đá"), ("dam", "attack / cast: dậm chân trước xuống đất")):
        sk.su_kien(e, m)
    print(f"{len(sk.bones)} xương, {len(sk.slots)} slot, {tong[0]} đỉnh, {tong[1]} tam giác; đáy y = {y_day:.1f}, tâm ({tam[0]:.1f}, "
          f"{tam[1]:.1f})")
    return sk, dict(IB=IB, ten=ten, goc0=goc0, y_day=y_day, tam=tam, S=S, Wi=Wi)


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
T_HUC, LAO, D_ATTACK = 0.46, 0.55, 1.00                 # attack: ngửa lấy đà 0,30 s, chúi húc
D_WALK, D_HIT, D_DIE = 0.60, 0.50, 1.10
T_NHAY, T_DAP_C = 0.46, 0.68                            # cast: chồm đứng cao nhất, dậm xuống
T_LAC0, T_LAC1 = 0.26, 0.54                             # cast: lắc núi đá
BAY_MANH = {"a": ("phach_t", "ph_t"), "b": ("phach_p", "ph_p"), "c": ("yezi_1", "yezi_2")}
T_PHONG = {"a": 0.46, "b": 0.52, "c": 0.58}            # cụm rời hốc (nối nhau)
BAY, GIU, VE = 0.20, 0.14, 0.30
VONG_DI = {"a": 70.0, "b": 110.0, "c": 50.0}
VONG_VE = {"a": 170.0, "b": 230.0, "c": 130.0}
TV = max(T_PHONG.values()) + BAY + GIU + VE
D_CAST = round(TV + 0.30, 2)
T_RUT, T_GONG0, T_GONG1 = 0.22, 0.30, 0.84              # skill: rụt chân, núi đá rung
T_BAN_TROI, T_DUNG, T_MUA, T_SKILL_TRUNG = 0.90, 1.06, 1.22, 1.56
T_MOC = 1.74
D_SKILL = 2.20
T_CHAM, T_BUNG = 0.36, 0.66                             # appear: núi đá chạm đất, chân / đầu bật ra
D_APPEAR = 1.70


def lam_clip(sk, info, cao=300.0):
    CD = chuyen_dong(info)

    def dat(P, goc, tau, lap=False, chi=None, bo=(), kq=None):
        dur, R, n = CD[goc]
        tq = tau % dur if lap else min(max(tau, 0.0), dur)
        x = tq * FPS
        i0 = min(int(x), n - 1)
        i1 = min(i0 + 1, n - 1)
        w = x - i0
        for b, A in R.items():
            if (chi is not None and b not in chi) or b in bo:
                continue
            v = A[i0] * (1 - w) + A[i1] * w
            k = kq.get(b, 1.0) if kq else 1.0
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]) * k)
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]) * k, float(v[2]) * k)
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, float(1 + (v[3] - 1) * k), float(1 + (v[4] - 1) * k))

    def dam(P, a, chi=None):
        if a < 0.999:
            for sl in sk.slots:
                if chi is None or sl["name"] in chi:
                    P.alpha[sl["name"]] = a * P.alpha.get(sl["name"], sl["alpha"])

    def nheo(P, k):
        P.scale("mat", 1.0, k)

    def _dich_cha(P, b, dx, dy):
        W = sk.the_gioi(P)
        Wp = W[sk.bones[sk.bi[b]]["parent"]]
        d = np.linalg.solve(Wp[:2, :2], np.array([dx, dy]))
        return float(d[0]), float(d[1])

    CHAN_KQ = {b: 0.45 for b in DUI + CHAN}

    # ------------------------------------------------ idle: sóng mềm lệch pha 2 s + trò nhỏ
    D_IDLE = 2.0
    w = 2 * math.pi / D_IDLE

    def song(t, tre, k=1.0):
        return math.sin(w * k * (t - tre))

    def f_idle(t, P):
        dat(P, "idle_01", 0.0)
        th = song(t, 0.0)
        P.scale("day", 1.0 + 0.012 * th, 1.0 - 0.016 * th)        # thở (giữ thể tích), núi đá nặng nên nhỏ
        P.move("day", 0.0, 1.8 * song(t, 0.05))
        P.rot("tam", 0.6 * song(t, 0.10))
        P.rot(DAU, 0.6 * song(t, 0.16))                            # khối trước + đầu trễ thân
        P.rot("dau", 1.6 * song(t, 0.20))
        for b, tre, a in (("fangkuai_4", 0.22, 0.8), ("fangkuai_5", 0.30, 1.6), ("fangkuai_6", 0.34, 1.4)):
            P.rot(b, a * song(t, tre))
        for b, tre, a in (("pha_le", 0.30, 2.0), ("ph_t", 0.38, 3.0), ("ph_p", 0.26, 3.0), ("yezi_2", 0.42, 5.0)):
            P.rot(b, a * song(t, tre))                              # cụm pha lê lúc lắc trễ dần
        for b, tre, a in (("duoi1", 0.30, 1.5), ("duoi2", 0.38, 4.0), ("duoi3", 0.46, 7.0)):
            P.rot(b, a * song(t, tre, 2.0))                          # đuôi vẫy hai nhịp mỗi vòng, ngọn trễ
        # trò: đầu thò ra hít hít (0,50 → 0,95), chớp mắt (1,30), đầu rụt nhẹ cau lại (1,55 → 1,85)
        tho = hoat.cv(t, [(0.50, 0.0), (0.62, 1.0, "out"), (0.86, 1.0), (0.98, 0.0, "io")])
        hit = hoat.cv(t, [(0.62, 0.0), (0.67, 1.0, "io"), (0.72, 0.0, "io"), (0.77, 1.0, "io"), (0.83, 0.0, "io")])
        P.move("dau", 7.0 * tho, 2.0 * tho)
        P.rot("dau", -2.0 * tho + 2.0 * hit)
        nheo(P, 1.0 - 0.9 * hoat.cv(t, [(1.28, 0.0), (1.32, 1.0, "io"), (1.38, 0.0, "io")]))
        rut = hoat.cv(t, [(1.55, 0.0), (1.66, 1.0, "out"), (1.82, 0.0, "io")])
        P.move("dau", -4.0 * rut, -2.0 * rut)

    def lac_tre(P, t, t0, a, chu_ky=0.16, tat=0.12, bones=(("pha_le", 0.0, 1.0), ("ph_t", 0.03, 1.4), ("ph_p", 0.05, 1.3),
                                                             ("yezi_2", 0.07, 2.2))):
        """cụm pha lê lúc lắc tắt dần sau cú va ở t0 (trễ dần từng cụm)."""
        for b, tre, k in bones:
            u = t - t0 - tre
            if u > 0:
                P.rot(b, a * k * math.exp(-u / tat) * math.sin(u * 2 * math.pi / chu_ky))

    def duoi(P, t, a=1.0, ky=0.5):
        for b, tre, aa in (("duoi1", 0.0, 1.5), ("duoi2", 0.05, 4.0), ("duoi3", 0.10, 7.0)):
            P.rot(b, a * aa * math.sin(2 * math.pi * (t - tre) / ky))

    # ------------------------------------------------ walk: lạch bạch (chân ngắn bước so le dưới váy, núi đá lắc, đầu gật)
    def f_walk(t, P):
        dat(P, "idle_01", 0.0)
        ph = 2 * math.pi * t / D_WALK
        for b, lech, a in (("yao2", 0.0, 9.0), ("yao5", 0.0, 9.0), ("yao4", math.pi, 9.0), ("yao3", math.pi, 9.0)):
            P.rot(b, a * math.sin(ph + lech))                                  # chéo cặp như thú bốn chân
        for b, lech in (("yao2", 0.0), ("yao5", 0.0), ("yao4", math.pi), ("yao3", math.pi)):
            nang = max(0.0, math.sin(ph + lech + 0.6))
            P.scale(b, 1.0 - 0.10 * nang, 1.0)                                 # nhấc chân (đùi co) ở pha vung tới
        P.move("day", 0.0, 0.016 * cao * abs(math.sin(ph)))
        P.scale("day", 1.0 + 0.012 * math.cos(2 * ph), 1.0 - 0.012 * math.cos(2 * ph))
        P.rot("tam", 1.6 * math.sin(ph))
        P.rot("dau", 1.8 * math.sin(2 * ph - 0.6))
        P.move("dau", 0.0, 1.5 * math.sin(2 * ph - 0.6))
        for b, tre, a in (("fangkuai_5", 0.3, 1.2), ("fangkuai_6", 0.5, 1.2)):
            P.rot(b, a * math.sin(2 * ph - tre))
        for b, tre, a in (("pha_le", 0.5, 1.5), ("ph_t", 0.8, 2.0), ("ph_p", 0.7, 2.0), ("yezi_2", 1.0, 4.0)):
            P.rot(b, a * math.sin(2 * ph - tre))
        duoi(P, t, 1.0, D_WALK)

    # ------------------------------------------------ hit: bật lùi, nghiêng ra sau, nheo, pha lê lắc
    def f_hit(t, P):
        dat(P, "idle_01", 0.0)
        k = hoat.cv(t, [(0.0, 0.0), (0.07, 1.0, "out"), (0.18, 0.85), (0.42, 0.0, "io"), (D_HIT, 0.0)])
        P.move("move", -0.05 * cao * k, 0.0)
        P.rot("tam", 6.0 * k)
        P.scale("day", 1.0 + 0.06 * k, 1.0 - 0.06 * k)
        P.move("dau", -9.0 * k, 3.0 * k)
        P.rot("dau", 6.0 * k)
        nheo(P, 1.0 - 0.75 * k)
        lac_tre(P, t, 0.05, 7.0)
        for b in DUI:
            P.rot(b, -5.0 * k)
        duoi(P, t, 1.4 * k, 0.24)

    # ------------------------------------------------ die: bật lùi → chân rụt, núi đá sụp xuống, đầu gục, mắt nhắm → mờ
    def f_die(t, P):
        dat(P, "idle_01", 0.0)
        k = hoat.cv(t, [(0.0, 0.0), (0.08, 1.0, "out"), (0.30, 0.6, "io")])
        P.move("move", -0.05 * cao * k, 0.0)
        P.rot("tam", 6.0 * k)
        sup = ease((t - 0.28) / 0.34, "in") if t > 0.28 else 0.0
        for b in DUI:
            P.scale(b, 1.0 - 0.5 * sup, 1.0)
        P.move("day", 0.0, -0.10 * cao * sup)
        P.rot("tam", -9.0 * sup)                                            # đổ chúi về trước
        P.move("dau", 6.0 * sup, -12.0 * sup)
        P.rot("dau", -10.0 * sup)
        if t > 0.62:
            b = math.exp(-(t - 0.62) / 0.07) * math.sin((t - 0.62) * 2 * math.pi / 0.18)
            P.scale("day", 1 + 0.07 * b, 1 - 0.09 * b)
            lac_tre(P, t, 0.62, 8.0)
        nheo(P, 1.0 - 0.9 * min(1.0, t / 0.35))
        dam(P, float(np.clip(1.0 - (t - D_DIE) / (TAN - 0.1), 0.0, 1.0)))

    # ------------------------------------------------ attack: ngửa lấy đà (nặng: 0,3 s) → LAO HÚC chúi đầu → khựng → quá đà → về
    def f_attack(t, P):
        dat(P, "idle_01", 0.0)
        lay = hoat.cv(t, [(0.0, 0.0), (0.30, 1.0, "io"), (T_HUC - 0.04, 0.0, "in")])
        huc = hoat.cv(t, [(0.30, 0.0), (T_HUC, 1.0, "in"), (T_HUC + 0.12, 1.0), (T_HUC + 0.20, 1.12, "out"), (0.80, 0.0, "io"),
                          (D_ATTACK, 0.0)])
        if t < T_HUC - 0.12:
            lao = -0.07 * ease(t / (T_HUC - 0.12))
        elif t < T_HUC:
            lao = -0.07 + (LAO + 0.07) * ease((t - (T_HUC - 0.12)) / 0.12, "in")
        elif t < T_HUC + 0.12:
            lao = LAO
        else:
            lao = LAO * (1 - ease((t - T_HUC - 0.12) / max(0.05, D_ATTACK - 0.12 - T_HUC - 0.12)))
        P.move("move", cao * lao, 0.0)
        P.rot("tam", 7.0 * lay - 11.0 * huc)                                 # ngửa ra sau rồi chúi đầu húc
        P.scale("day", 1.0 + 0.04 * lay, 1.0 - 0.05 * lay)
        P.move("day", 0.0, 0.03 * cao * math.sin(math.pi * min(1.0, max(0.0, (t - 0.30) / (T_HUC - 0.30)))))
        P.move("dau", -7.0 * lay + 12.0 * huc, -3.0 * lay - 4.0 * huc)
        P.rot("dau", 4.0 * lay - 8.0 * huc)
        for b, a in (("yao4", -12.0), ("yao5", -12.0), ("yao2", 14.0), ("yao3", 14.0)):   # chân trước vươn tới, chân sau đạp
            P.rot(b, a * huc - 0.4 * a * lay)
        k = math.exp(-((t - (T_HUC + 0.02)) / 0.05) ** 2)
        P.scale("day", 1 - 0.09 * k, 1 + 0.08 * k)
        if T_HUC - 0.06 < t < T_HUC + 0.28:
            nheo(P, 0.55)
        lac_tre(P, t, T_HUC, 9.0)
        duoi(P, t, 0.6 + 1.2 * huc, 0.30)

    # ------------------------------------------------ cast: chồm đứng, lắc núi đá → ba cụm pha lê bay găm → dậm xuống → cụm bay về
    far = sk.W0["far"][:2, 2] if "far" in sk.bi else np.array([0.9 * cao + 140.0, 0.45 * cao])

    def than_cast(t, P):
        dat(P, "idle_01", 0.0)
        chom = hoat.cv(t, [(0.0, 0.0), (0.12, -0.25, "io"), (T_NHAY, 1.0, "out"), (T_DAP_C - 0.06, 0.9), (T_DAP_C, -0.15, "in"),
                           (T_DAP_C + 0.16, 0.0, "io")])
        cp = max(chom, 0.0)
        P.rot("tam", 9.0 * chom)                                             # chồm đứng: đầu, chân trước ngóc lên
        P.move("day", -0.02 * cao * cp, 0.05 * cao * cp)
        for b in ("yao4", "yao5"):
            P.rot(b, 16.0 * cp)
        for b in ("yao2", "yao3"):
            P.rot(b, -6.0 * cp)
        P.scale("day", 1.0 + 0.04 * max(-chom, 0.0), 1.0 - 0.05 * max(-chom, 0.0))
        P.move("dau", 6.0 * cp, 3.0 * cp)
        if T_LAC0 < t < T_LAC1 + 0.06:                                      # lắc núi đá mạnh như chó rũ nước
            e = math.sin(math.pi * min(1.0, (t - T_LAC0) / (T_LAC1 + 0.06 - T_LAC0)))
            r = 5.0 * e * math.sin((t - T_LAC0) * 2 * math.pi / 0.075)
            P.rot("tam", r)
            for k, b in enumerate(("fangkuai_4", "fangkuai_5", "fangkuai_6")):
                P.rot(b, 1.2 * r * (1 if k % 2 else -1))
            for b in ("pha_le", "ph_t", "ph_p", "yezi_2"):
                P.rot(b, 2.0 * r)
            nheo(P, 0.55)
        if t > T_DAP_C:                                                      # dậm xuống phịch
            b = math.exp(-(t - T_DAP_C) / 0.08) * math.sin((t - T_DAP_C) * 2 * math.pi / 0.2)
            P.scale("day", 1 + 0.10 * b, 1 - 0.12 * b)
            lac_tre(P, t, T_DAP_C, 6.0, bones=(("pha_le", 0.0, 1.0),))
        for k in BAY_MANH:                                                   # mỗi cụm về: núi đá nảy nhẹ đón
            tv = T_PHONG[k] + BAY + GIU + VE
            if t > tv:
                b = math.exp(-(t - tv) / 0.05) * math.sin((t - tv) * 2 * math.pi / 0.14)
                P.rot("tam", 1.2 * b)
        duoi(P, t, 1.0, 0.32)

    def f_cast(t, P):
        than_cast(t, P)
        W = None
        for ben, (s_, b_) in BAY_MANH.items():
            t0 = T_PHONG[ben]
            t_toi, t_ve0 = t0 + BAY, t0 + BAY + GIU
            t_ve1 = t_ve0 + VE
            fb, bb = f"fly_{ben}", f"bay_{ben}"
            if fb not in sk.bi:
                continue
            if t < t0:
                P.alpha[bb] = 0.0
                continue
            tt = min(t, t_ve1)
            if t < t_ve1:
                P.alpha[s_] = 0.0
                P.alpha[bb] = 1.0
            else:
                P.alpha[bb] = 0.0
            A = sk.W0[fb][:2, 2].copy()
            v = far - A
            n = np.array([-v[1], v[0]]) / (float(np.hypot(*v)) or 1.0)
            if tt < t_toi:
                f = ease((tt - t0) / BAY, "in")
                pos = A + f * v + n * VONG_DI[ben] * math.sin(math.pi * f)
                ang = -360.0 * f
            elif tt < t_ve0:
                pos = far.copy() + np.array([6.0, 0.0]) * math.sin((tt - t_toi) * 60.0) * math.exp(-(tt - t_toi) / 0.06)
                ang = -360.0
            else:
                if W is None:
                    W = sk.the_gioi(P)
                rb, Wl = REF[ben]
                Mt = W[rb] @ np.linalg.inv(Wl) @ sk.W0[bb]
                u = (tt - t_ve0) / VE
                e = ease(u, "io")
                pos = far * (1 - e) + Mt[:2, 2] * e + n * VONG_VE[ben] * math.sin(math.pi * u)
                g1 = _goc(Mt) - _goc(sk.W0[bb])
                ang = -360.0 * (1 - e) + (g1 - 360.0) * e
            P.move(fb, float(pos[0] - A[0]), float(pos[1] - A[1]))
            P.rot(bb, float(ang))

    # ------------------------------------------------ skill: rụt chân gồng → pha lê vọt lên trời → đứng dậy chĩa mõm, mưa pha lê
    def f_skill(t, P):
        dat(P, "idle_01", 0.0)
        rut = hoat.cv(t, [(0.0, 0.0), (T_RUT, 1.0, "out"), (T_GONG1, 1.0), (T_BAN_TROI, -0.40, "out"), (T_DUNG, 0.0, "io"), (D_SKILL, 0.0)])
        r = max(rut, 0.0)
        for b in DUI:                                                     # rụt chân vào dưới váy
            P.scale(b, 1.0 - 0.55 * r, 1.0)
        P.move("day", 0.0, -0.09 * cao * r + 0.05 * cao * max(-rut, 0.0))     # bật lên lúc pha lê bung
        P.scale("day", 1.0 + 0.03 * r, 1.0 - 0.03 * r)
        P.move("dau", -10.0 * r, -7.0 * r)                                 # đầu rụt vào núi đá
        if r > 0.2:
            nheo(P, 1.0 - 0.6 * min(1.0, r))
        if T_GONG0 < t < T_GONG1 + 0.04:                                   # núi đá rung lạch cạch, cụm pha lê rung
            e = min(1.0, (t - T_GONG0) / 0.2)
            q = 3.0 * e * math.sin((t - T_GONG0) * 2 * math.pi / 0.06)
            P.rot("tam", q)
            for k, b in enumerate(("fangkuai_4", "fangkuai_5", "fangkuai_6", "ph_t", "ph_p")):
                P.rot(b, (2.0 + k) * e * math.sin((t - T_GONG0) * 2 * math.pi / (0.07 + 0.012 * k)))
        if t < T_BAN_TROI:                                                 # nén một nhịp rồi VỌT lên trời → ẩn → mọc lại
            nen = hoat.cv(t, [(T_BAN_TROI - 0.12, 0.0), (T_BAN_TROI - 0.04, 1.0, "out"), (T_BAN_TROI, 0.0)])
            P.scale("pha_le", 1.0 - 0.12 * nen, 1.0 + 0.08 * nen)
        elif t < T_MOC:
            if t < T_MOC - 0.08:                                            # vọt lên; về hốc lúc CÒN ẨN (khỏi bay ngược xuống)
                vot = ease((t - T_BAN_TROI) / 0.14, "in")
                P.move("pha_le", *_dich_cha(P, "pha_le", 0.0, 2.8 * cao * vot))
                P.scale("pha_le", 1.0 + 0.4 * vot, 1.0 - 0.15 * vot)
            else:
                P.scale("pha_le", 0.1, 0.1)
            if t > T_BAN_TROI + 0.14:
                P.alpha["tinh_the"] = 0.0
        else:
            k = hoat.cv(t, [(T_MOC, 0.1), (T_MOC + 0.12, 1.2, "out"), (T_MOC + 0.22, 0.94, "io"), (T_MOC + 0.30, 1.0, "io")])
            P.scale("pha_le", k, k)
        for b, t1 in (("ph_t", T_BAN_TROI + 0.02), ("ph_p", T_BAN_TROI + 0.05)):   # hai cụm hốc bên nảy theo
            k = hoat.cv(t, [(t1 - 0.01, 1.0), (t1 + 0.06, 1.25, "out"), (t1 + 0.18, 1.0, "io")])
            P.scale(b, k, k)
        chi = hoat.cv(t, [(T_DUNG, 0.0), (T_DUNG + 0.14, 1.0, "out"), (1.80, 1.0), (D_SKILL - 0.05, 0.0, "io")])
        P.rot("dau", -6.0 * chi)
        P.move("dau", 8.0 * chi, 0.0)
        P.rot("tam", -3.0 * chi)
        if T_MUA < t < 1.80:                                               # dáng giữ có trôi
            P.rot("tam", 1.0 * math.sin((t - T_MUA) * 2 * math.pi / 0.16))
        if t > T_SKILL_TRUNG:
            b = math.exp(-(t - T_SKILL_TRUNG) / 0.09) * math.sin((t - T_SKILL_TRUNG) * 2 * math.pi / 0.2)
            P.scale("day", 1 + 0.05 * b, 1 - 0.06 * b)

    # ------------------------------------------------ appear: núi đá rơi → chạm đất nảy → chân, đầu, đuôi bật ra → rũ mình → cau mày
    than_an = ("tou", "yankuang", "weiba_1") + CHAN

    def f_appear(t, P):
        dat(P, "idle_01", 0.0)
        y = hoat.cv(t, [(0.0, 0.9 * cao), (T_CHAM, 0.0, "in"), (0.44, 0.08 * cao, "out"), (0.52, 0.0, "in")])
        P.move("day", 0.0, y)
        P.rot("tam", hoat.cv(t, [(0.0, -18.0), (T_CHAM, 0.0, "in"), (0.44, 3.0, "out"), (0.52, 0.0, "in")]))
        for x in (T_CHAM, 0.52):
            if t > x:
                b = math.exp(-(t - x) / 0.06) * math.sin((t - x) * 2 * math.pi / 0.16)
                P.scale("day", 1 + 0.12 * b, 1 - 0.14 * b)
        dam(P, min(1.0, t / 0.06))
        hien = 1.0 if t >= T_BUNG - 0.02 else 0.0                          # hiện tức thì (mờ dần thì nhìn xuyên thấy váy qua thân)
        dam(P, hien, chi=than_an)
        if t < T_BUNG + 0.30:                                              # chân bật ra (dài dần, vượt, về), đầu thò ra
            # chân thò ra từ dưới váy: vượt ít (1,03) vì chân ngắn, duỗi quá thì thò dài khỏi váy (người dùng chê "chân dài quá")
            k = hoat.cv(t, [(T_BUNG - 0.04, 0.55), (T_BUNG + 0.08, 1.03, "out"), (T_BUNG + 0.18, 0.99, "io"), (T_BUNG + 0.28, 1.0, "io")])
            for b in DUI:
                P.scale(b, k, 1.0)
            P.move("dau", -16.0 * (1 - min(1.0, k)), -9.0 * (1 - min(1.0, k)))
        if 1.00 < t < 1.34:                                                # rũ mình
            e = math.sin(math.pi * (t - 1.00) / 0.34)
            r = 5.0 * e * math.sin((t - 1.00) * 2 * math.pi / 0.11)
            P.rot("tam", r)
            for k, b in enumerate(("fangkuai_4", "fangkuai_5", "fangkuai_6")):
                P.rot(b, 1.4 * r * (1 if k % 2 else -1))
            nheo(P, 0.5)
        cau = hoat.cv(t, [(1.38, 0.0), (1.48, 1.0, "out"), (D_APPEAR, 1.0)])
        P.rot("dau", -2.0 * cau)
        P.move("dau", 5.0 * cau, 0.0)

    clips = [
        Clip("appear", D_APPEAR, f_appear, ev=[(T_CHAM, "cham_dat", ""), (T_BUNG, "bung", "")]),
        Clip("idle", D_IDLE, f_idle, loop=True),
        Clip("walk", D_WALK, f_walk, loop=True),
        Clip("attack", D_ATTACK, f_attack, ev=[(T_HUC, "trung", "")], trung=T_HUC),
        Clip("cast", D_CAST, f_cast, ev=[(T_LAC0, "ran", "")] + [(round(T_PHONG[k], 3), "phong", k) for k in BAY_MANH] +
             [(round(T_PHONG["a"] + BAY, 3), "trung", ""), (T_DAP_C, "cham_dat", "")] +
             [(round(T_PHONG[k] + BAY + GIU + VE, 3), "ve", k) for k in BAY_MANH], trung=round(T_PHONG["a"] + BAY, 3)),
        Clip("skill", D_SKILL, f_skill, ev=[(T_GONG0, "gong", ""), (T_BAN_TROI, "ban_troi", ""), (T_MUA, "mua", ""),
                                             (T_SKILL_TRUNG, "trung", ""), (T_MOC, "moc", "")], trung=T_SKILL_TRUNG),
        Clip("hit", D_HIT, f_hit),
        Clip("die", D_DIE + TAN, f_die),
    ]
    return clips, than_cast


REF = {}


def them_bay(sk, info, than_cast, cao, far_xy=None):
    """xương far + fly_<k> (tâm cụm lúc rời hốc) + bay_<k> và slot bản sao (ẩn) cho từng cụm bay của cast (như cong_da_rig.them_soi_bay)."""
    fx, fy = far_xy if far_xy is not None else (0.9 * cao + 140.0, 0.45 * cao)
    sk.xuong("far", "root", float(fx), float(fy))
    for ben, (s, rb) in BAY_MANH.items():
        P = khung.Pose()
        than_cast(T_PHONG[ben], P)
        W = sk.the_gioi(P)
        att = sk.atts[s][s]
        V = np.array([sum(w * (W[b] @ np.array([x, y, 1.0]))[:2] for b, x, y, w in r) for r in att["verts"]])
        c = V.mean(0)
        sk.xuong(f"fly_{ben}", "root", float(c[0]), float(c[1]))
        sk.xuong(f"bay_{ben}", f"fly_{ben}", float(c[0]), float(c[1]), goc=_goc(W[rb]), the_gioi=True)
        inv = np.linalg.inv(sk.W0[f"bay_{ben}"])
        rows = [[(f"bay_{ben}", *[float(q) for q in (inv @ np.array([p[0], p[1], 1.0]))[:2]], 1.0)] for p in V]
        sk.slot(f"bay_{ben}", "move", s, an=True)
        sk.luoi_gan(f"bay_{ben}", s, sk.luoi[(s, s)], trongso.cung(len(rows), "move"), the_gioi=V)
        sk.atts[f"bay_{ben}"][s]["verts"] = rows
        REF[ben] = (rb, W[rb].copy())


def dung_het(far_xy=None):
    sk, info = dung()
    ve0 = soi.Ve(sk)
    clips, than_cast = lam_clip(sk, info)
    idle0 = hoat.nuong(sk, clips[1])[0]
    cao = soi.chieu_cao(ve0, idle0)
    them_bay(sk, info, than_cast, cao, far_xy)
    clips, _ = lam_clip(sk, info, cao)
    return sk, info, clips, cao


def diem(sk, clips, cao):
    """vị trí xương (đơn vị chiều cao dáng đứng; x về phía đối thủ = +x của rig, y lên; gốc = giữa đáy hộp idle 0) theo giờ clip."""
    ve0 = soi.Ve(sk)
    cl = {c.ten: c for c in clips}
    idle0 = hoat.nuong(sk, cl["idle"])[0]
    bx = ve0.bao(idle0)
    cx, yg = (bx[0] + bx[2]) / 2.0, bx[1]
    viec = [("cast", "tam", np.arange(0.26, 0.62, 0.08)), ("cast", "ph_t", [T_PHONG["a"]]), ("cast", "ph_p", [T_PHONG["b"]]),
            ("cast", "yezi_2", [T_PHONG["c"]]), ("cast", "mieng", [T_DAP_C]), ("skill", "pha_le", [T_BAN_TROI]),
            ("skill", "mieng", [T_MUA, T_SKILL_TRUNG]), ("attack", "mieng", [T_HUC]), ("idle", "mieng", [0.0])]
    for clip, b, ts in viec:
        fr = hoat.nuong(sk, cl[clip])
        o = []
        for t in ts:
            P = fr[min(len(fr) - 1, int(round(t * 30)))]
            p = sk.the_gioi(P)[b][:2, 2]
            o.append(f"new Vector2({(p[0] - cx) / cao:.3f}f, {(p[1] - yg) / cao:.3f}f)")
        print(f"  {clip}.{b} t={[round(float(t), 2) for t in ts]}: " + ", ".join(o))


def main(a):
    sk, info, clips, cao = dung_het()
    ve0 = soi.Ve(sk)
    print(f"chiều cao {cao:.0f}")
    if a and a[0] == "diem":
        diem(sk, clips, cao)
        return
    if a and a[0] == "kiem":
        # memory rig-kiem-goc-nhay: ở 60 khung/giây đo góc xoay lớn nhất giữa hai khung của mọi xương (≥ 180° là lật ngược khi nội suy,
        # > 45° là nhìn thấy giật) và bước dời lớn nhất của mọi xương (× chiều cao / khung); bỏ xương bay của cast (bay_*, fly_*: vật bay)
        print("clip      khung | xoay lớn nhất (xương, giây) | dời lớn nhất (xương, giây, cao/khung)")
        for c in clips:
            fr = hoat.nuong(sk, c, fps=60)
            Wl = [sk.the_gioi(P) for P in fr]
            ten_x = [b["name"] for b in sk.bones if not b["name"].startswith(("bay_", "fly_", "far"))]
            gx = (0.0, "", 0.0)
            dx = (0.0, "", 0.0)
            for i in range(1, len(fr)):
                for b in ten_x:
                    g0 = math.degrees(math.atan2(Wl[i - 1][b][1, 0], Wl[i - 1][b][0, 0]))
                    g1 = math.degrees(math.atan2(Wl[i][b][1, 0], Wl[i][b][0, 0]))
                    dg = abs((g1 - g0 + 180.0) % 360.0 - 180.0)
                    if dg > gx[0]:
                        gx = (dg, b, i / 60.0)
                    dd = float(np.hypot(*(Wl[i][b][:2, 2] - Wl[i - 1][b][:2, 2]))) / cao
                    if dd > dx[0]:
                        dx = (dd, b, i / 60.0)
            canh = " ⚠" if gx[0] > 45 or dx[0] > 0.15 else ""
            print(f"{c.ten:8s} {len(fr):4d} | {gx[0]:5.1f}° ({gx[1]}, {gx[2]:.2f}s) | {dx[0]:.3f} ({dx[1]}, {dx[2]:.2f}s){canh}")
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
        sc = float(a[3]) if len(a) > 3 else 0.6
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
    xuat.xuat_het(sk, clips, RA, TEN_RIG, tieu_de="Thạch Giáp dạng 2 (cong_da_2): tướng 1 đảo Thổ", dang=2, so_dang=2,
                  dung_yen=("cast", "skill"), far=("cast",), ma_goc=None, khop_idle=0.2, cao=cao, impact=IMPACT,
                  tol={"rotate": 0.08, "translate": 0.15, "scale": 0.0015}, dich_mb=0.3, tran_mb=0.5, span=3.6)


if __name__ == "__main__":
    main(sys.argv[1:])
