# -*- coding: utf-8 -*-
"""Dòng tm09 "Hàn Ngạc" (cá sấu băng vực sâu, lô 10 tướng mới đảo Thủy 2026-11-11): cắt tờ mảnh GPT, dựng rig bằng mã với thư
viện quai/, nướng 7 clip (+ evolve ở dạng 1), xuất .atomik + game.json, tờ khung, lưới, ảnh cận.

Con gốc tham khảo monster_3281 (chỉ lấy cấu trúc: hàm một xương, thân chia trọng số đầu / hàm / gốc đuôi, đuôi chuỗi, chân IK
bám đất; nhịp cắn há 0,47 s táp 0,60 s). Thiết kế, ghi chú: inbox/tm09_ghichu.md. Gói GPT: build_tm09.py.

    py -3 -I ArtGen/Spine/tm09.py cat 2            cắt tờ M01..M03 của dạng 2 vào inbox/tm09_2/manh/ (+ _soi.png)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm09.py rig 2      dựng + xuất dạng 2
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm09.py rig 1      dạng 1 + evolve gộp dạng 2
    ... tm09.py all                                                                    dạng 2 rồi dạng 1
Thiếu ảnh mảnh thì dùng hình giữ chỗ (dựng song song lúc chờ gen).
"""
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from quai import anh, hoat, khung, luoi, mieng, soi, tienhoa, trongso, xuat  # noqa: E402
from quai.hoat import Clip, DayMem, LoXo, an_hien, chuoi_song, cv, ease, lui, rung, song  # noqa: E402
from quai.khung import Dat  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "tm09"
TEN = {1: "Ngạc Nhi", 2: "Hàn Ngạc Vương"}
B_VIEN, B_TRONG = 11.0, 15.0

# ---------------------------------------------------------------- cấu hình từng dạng
# giữ chỗ: (hình, w, h, màu) theo cỡ tờ GPT (1536 × 1024); ti: co về pixel atlas
C2 = dict(ti=0.5, body=(31, 85, 102), far=(26, 71, 86), ice=(230, 241, 244),
          giu_cho={"dau": ("bo", 440, 300), "ham": ("ham", 380, 120), "mieng": ("mieng", 240, 170), "sung": ("giot", 420, 330),
                   "luoi": ("luoi", 250, 60), "mi": ("mi", 120, 80), "chuy": ("giot", 320, 300), "than": ("tron", 1100, 340),
                   "duoi": ("dai", 1000, 180), "go_vai": ("giot", 400, 280), "go_lung": ("giot", 320, 190), "go_hong": ("giot", 260, 130),
                   "chan_tn": ("chan", 260, 500), "chan_sn": ("chan", 300, 500), "chan_tx": ("chan", 240, 480), "chan_sx": ("chan", 280, 480)},
          go=("go_vai", "go_lung", "go_hong"), duoi_dot=6, luoi_dot=3,
          # vị trí theo tỉ lệ (Wt, Ht = cỡ thân): x tính từ tâm thân, y từ tâm thân
          hinge=(0.32, 0.76), snout=(0.985, 0.76), sung_goc=(0.15, 0.04), sung_goc_xa=(0.09, 0.02), sung_goc_deg=-28,
          go_x=(0.19, -0.11, -0.37), go_y=(0.40, 0.42, 0.34), duoi_y=0.0, dau_y=0.20, dau_neo=(0.03, 0.52),
          x_truoc=0.30, x_sau=-0.30, xa_truoc=-0.14, xa_sau=0.12, y_bung=0.50, mace_goc=-10, duoi_x=-0.40,
          ti_rieng={"duoi": 0.75, "sung": 1.45, "dau": 1.5, "ham": 1.5, "mieng": 1.5, "mi": 1.5, "go_vai": 1.15, "go_lung": 1.1,
                    "chan_tn": 1.15, "chan_sn": 1.15, "chan_tx": 1.15, "chan_sx": 1.15},
          duoi_ti=(1.0, 1.0), duoi_day=(1.5, 0.9),
          # đặt theo place.json: K = px rig / px concept; gờ chìm xuống lưng (px concept); gốc đuôi xoay thêm so với dây cung
          # (gốc chĩa ra sau-hơi lên), curl uốn dần tới ngọn (âm = nhấc): tổng ≈ góc ngọn − góc gốc
          K=0.6, go_chim=30, duoi_goc=45, curl=(0.0, 0.0), ham_nghi=0.0, ham_mo=36.0)
C1 = dict(ti=0.42, body=(60, 131, 150), far=(51, 111, 128), ice=(230, 241, 244),
          giu_cho={"dau": ("bo", 440, 360), "ham": ("ham", 300, 120), "mieng": ("mieng", 200, 150), "sung": ("giot", 220, 150),
                   "luoi": ("luoi", 190, 56), "mi": ("mi", 150, 120), "chuy": ("giot", 220, 200), "than": ("tron", 900, 380),
                   "duoi": ("dai", 760, 190), "go_vai": ("giot", 170, 170), "go_lung": ("giot", 170, 150), "go_hong": ("giot", 170, 130),
                   "chan_tn": ("chan", 260, 440), "chan_sn": ("chan", 290, 440), "chan_tx": ("chan", 240, 420), "chan_sx": ("chan", 270, 420)},
          go=("go_vai", "go_lung", "go_hong"), duoi_dot=4, luoi_dot=3,
          hinge=(0.30, 0.82), snout=(0.985, 0.78), sung_goc=(0.20, 0.08), sung_goc_xa=(0.14, 0.05), sung_goc_deg=-34,
          go_x=(0.16, -0.10, -0.34), go_y=(0.42, 0.44, 0.38), duoi_y=-0.02, dau_y=0.16, dau_neo=(0.03, 0.56),
          x_truoc=0.28, x_sau=-0.30, xa_truoc=-0.15, xa_sau=0.13, y_bung=0.50, mace_goc=-12, duoi_x=-0.40,
          ti_rieng={"dau": 1.6, "ham": 1.6, "mieng": 1.6, "mi": 1.6, "sung": 1.3, "than": 0.75, "duoi": 0.45, "chuy": 0.6,
                    "go_vai": 0.9, "go_lung": 0.9, "go_hong": 0.9, "chan_tn": 1.0, "chan_sn": 1.0, "chan_tx": 1.0, "chan_sx": 1.0},
          duoi_ti=(1.0, 1.0), duoi_day=(1.8, 1.1),
          K=0.5, go_chim=24, duoi_goc=18, curl=(0.0, 0.0), ham_nghi=0.0, ham_mo=28.0)
CFG = {1: C1, 2: C2}


def inbox(k, *p):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", *p)


# ---------------------------------------------------------------- cắt tờ
def _o(to, cols, rows):
    """mảnh theo ô (hàng, cột) của lưới cols × rows trên tờ."""
    cells = {}
    for m in to.manh:
        cx, cy = (m["x0"] + m["x1"]) / 2, (m["y0"] + m["y1"]) / 2
        cells.setdefault((min(rows - 1, int(cy / (to.h / rows))), min(cols - 1, int(cx / (to.w / cols)))), []).append(m)
    return cells


def cat(k):
    tv, ra = inbox(k, "tai_ve"), inbox(k, "manh")
    os.makedirs(ra, exist_ok=True)
    ten = {}
    # M01: 3 × 2: đầu, hàm, lòng miệng / sừng, (lưỡi + 2 mí), chùy
    p = anh.to_moi_nhat(tv, "M01")
    if p:
        to = anh.doc_to(p)
        cells = _o(to, 3, 2)
        g = {}
        for key, nm in (((0, 0), "dau"), ((0, 1), "ham"), ((0, 2), "mieng"), ((1, 0), "sung"), ((1, 2), "chuy")):
            ms = cells.get(key, [])
            if ms:
                g[nm] = max(ms, key=lambda m: m["dt"])
        ms = sorted(cells.get((1, 1), []), key=lambda m: -m["dt"])
        if ms:
            wide = max(ms, key=lambda m: (m["x1"] - m["x0"]) / max(1, m["y1"] - m["y0"]))
            g["luoi"] = wide
            rest = [m for m in ms if m is not wide]
            if rest:
                g["mi"] = max(rest, key=lambda m: m["dt"])
            if len(rest) > 1:
                g["mi_nho"] = min(rest, key=lambda m: m["dt"])
        ten.update(anh.luu_manh(to, g, ra, duc={"mieng": ("tu_dong", 400)}))
    # M09 (lượt 3, bám hình concept): đầu, hàm to, lòng miệng / lưỡi ngắn, 2 mí, (trống) — đè lên mảnh của M01
    p = anh.to_moi_nhat(tv, "M09")
    if p:
        to = anh.doc_to(p)
        cells = _o(to, 3, 2)
        g = {}
        for key, nm in (((0, 0), "dau"), ((0, 1), "ham"), ((0, 2), "mieng"), ((1, 0), "luoi")):
            ms = cells.get(key, [])
            if ms:
                g[nm] = max(ms, key=lambda m: m["dt"])
        ms = sorted(cells.get((1, 1), []), key=lambda m: -m["dt"])
        if ms:
            g["mi"] = ms[0]
            if len(ms) > 1:
                g["mi_nho"] = ms[1]
        ten.update(anh.luu_manh(to, g, ra, duc={"mieng": ("tu_dong", 400)}))
    # M08 (lượt 3): thân bám hình concept (một mảnh lớn nhất) — đè lên thân của M02
    p = anh.to_moi_nhat(tv, "M08")
    if p:
        to = anh.doc_to(p)
        if to.manh:
            ten.update(anh.luu_manh(to, {"than": max(to.manh, key=lambda m: m["dt"])}, ra))
    # M02: 3 hàng: thân / đuôi / 3 gờ (trái → phải)
    p = anh.to_moi_nhat(tv, "M02")
    if p:
        to = anh.doc_to(p)
        rows = _o(to, 1, 3)
        g = {}
        if rows.get((0, 0)):
            g["than"] = max(rows[(0, 0)], key=lambda m: m["dt"])
        if rows.get((1, 0)):
            g["duoi"] = max(rows[(1, 0)], key=lambda m: m["dt"])
        bot = sorted(rows.get((2, 0), []), key=lambda m: m["x0"])
        for nm, m in zip(CFG[k]["go"], bot):
            g[nm] = m
        ten.update(anh.luu_manh(to, g, ra))
    # M03: 2 × 2 chân: trước gần, sau gần / trước xa, sau xa
    p = anh.to_moi_nhat(tv, "M03")
    if p:
        to = anh.doc_to(p)
        g = anh.gan_theo_o(to, [["chan_tn", "chan_sn"], ["chan_tx", "chan_sx"]])
        ten.update(anh.luu_manh(to, g, ra))
    print("  đã cắt:", ", ".join(sorted(ten)))
    print("  soi:", anh.to_soi(ra, list(CFG[k]["giu_cho"]) + ["mi_nho"]))


# ---------------------------------------------------------------- dựng rig
def tim_mat(im):
    """tâm con mắt hổ phách trên ảnh đầu (px ảnh): cụm màu cam vàng lớn nhất."""
    a = np.asarray(im.convert("RGBA")).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    m = (al > 128) & (r > 190) & (g > 130) & (g < 215) & (b < 120) & (r - b > 90)
    lab, cs = anh.thanh_phan(m)
    if not cs:
        return None
    c = max(cs, key=lambda q: q["dt"])
    ys, xs = np.nonzero(lab == c["i"])
    return float(xs.mean()), float(ys.mean())


def dung(k):
    """dựng rig từ place.json (tm09_place.py: từng mảnh đã dò khớp vào concept). Toạ độ rig = toạ độ concept × K, gốc ở đất
    giữa hai chân, y lên. Mảnh không thấy trên concept (hàm, lòng miệng, lưỡi, mí) đặt theo đầu."""
    import json
    C = CFG[k]
    K = C["K"]
    pj = json.load(open(inbox(k, "place.json"), encoding="utf-8"))
    PL, (xg, yg) = pj["parts"], pj["ground"]

    def conv(x, y):
        return (x - xg) * K, (yg - y) * K

    # mật độ lưới theo chiều cao con (Claude điều phối bổ sung): bước viền ≈ 1,5 % chiều cao, bước trong ≈ 2 %
    cpa = np.asarray(Image.open(inbox(k, "tai_ve", "L1_duyet.png")).convert("RGB"))
    y_top = int(np.nonzero((cpa.min(axis=2) < 225).any(axis=1))[0].min())
    H_con = (yg - y_top) * K
    bv, bt = 0.015 * H_con, 0.02 * H_con
    print(f"  dạng {k}: chiều cao con {H_con:.0f} px rig → bước viền {bv:.1f}, bước trong {bt:.1f}")

    # nạp mảnh ở đúng cỡ rig (không phí atlas): tỉ lệ riêng = max(sx, sy) × K
    gc = {n: (h, w, hh, C["ice"] if n in ("sung", "chuy") or n.startswith("go") else (C["far"] if n.endswith("x") else C["body"]))
          for n, (h, w, hh) in C["giu_cho"].items()}
    gc["mieng"] = ("mieng", *C["giu_cho"]["mieng"][1:], (27, 79, 102))
    gc["luoi"] = ("luoi", *C["giu_cho"]["luoi"][1:], (74, 155, 181))
    gc["ham"] = ("ham", *C["giu_cho"]["ham"][1:], (217, 230, 234))
    tir = {}
    for n in gc:
        p = PL.get(n if n != "sung" else "sung")
        if p:
            tir[n] = max(p["sx"], p["sy"]) * K
    sd = PL["dau"]
    for n in ("ham", "mieng", "luoi", "mi"):
        tir[n] = max(sd["sx"], sd["sy"]) * K
    pc = anh.nap_manh(inbox(k, "manh"), gc, ti_le=1.0, ti_le_rieng=tir)
    sk = khung.Sk(f"{CODE}_{k}")
    for n, im in pc.items():
        sk.anh(n, im)

    def dat_cua(n, neo=(0.5, 0.5), lat=None, dcy=0.0, dgoc=0.0):
        """Dat của mảnh n theo place.json (tâm hoặc điểm gốc q0 trên concept)."""
        p = PL[n]
        t = tir["sung" if n == "sung_xa" else n]
        ti = (p["sx"] * K / t, p["sy"] * K / t)
        if p.get("two"):
            x, y = conv(*p["q0"])
        else:
            x, y = conv(p["cx"], p["cy"] + dcy)
        return Dat(x, y, goc=p["r"] + dgoc, ti=ti, neo=neo, lat=p["lat"] if lat is None else lat)

    # ---- xương thân
    dat_than = dat_cua("than")
    Wt, Ht = pc["than"].size
    P_than = dat_than.mot((0.5 * Wt, 0.5 * Ht), Wt, Ht)
    P_hong = dat_than.mot((0.22 * Wt, 0.5 * Ht), Wt, Ht)
    P_nguc = dat_than.mot((0.74 * Wt, 0.5 * Ht), Wt, Ht)
    P_co = dat_than.mot((0.94 * Wt, 0.40 * Ht), Wt, Ht)
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("than", "move", *P_than, dai=60)
    sk.xuong("hong", "than", *P_hong, the_gioi=True, dai=50)
    sk.xuong("nguc", "than", *P_nguc, the_gioi=True, dai=50)
    sk.xuong("co", "nguc", *P_co, the_gioi=True, dai=30)
    # ---- đầu, hàm, miệng
    dau = pc["dau"]
    w, h = dau.size
    dat_dau = dat_cua("dau")
    neck = dat_dau.mot((C["dau_neo"][0] * w, C["dau_neo"][1] * h), w, h)
    hinge = dat_dau.mot((C["hinge"][0] * w, C["hinge"][1] * h), w, h)
    snout = dat_dau.mot((C["snout"][0] * w, C["snout"][1] * h), w, h)
    sk.xuong("dau", "co", *neck, the_gioi=True, dai=float(np.hypot(*(snout - neck))))
    gj = math.degrees(math.atan2(*(snout - hinge)[::-1]))
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*(snout - hinge))), the_gioi=True)
    sk.xuong("mieng", "dau", snout[0] + 6, snout[1] + 8, goc=-3, dai=30, the_gioi=True)
    luoi_im = pc["luoi"]
    jd = (snout - hinge) / max(1e-9, np.hypot(*(snout - hinge)))
    dai_ham = float(np.hypot(*(snout - hinge)))
    # lưỡi nằm TRONG lòng miệng: gốc ở 0,18 hàm, dài tối đa 0,5 hàm (co nếu ảnh dài hơn), hơi thấp dưới trục hàm; không vượt mút hàm
    ti_luoi = min(1.0, 0.5 * dai_ham / luoi_im.width)
    root_l = hinge + jd * 0.18 * dai_ham - np.array([-jd[1], jd[0]]) * 0.02 * h
    dat_luoi = Dat(root_l[0], root_l[1], goc=gj - 3, ti=ti_luoi, neo=(0.0, 0.5))
    Ll = luoi.luoi_dai(luoi_im, C["luoi_dot"], ten="luoi", buoc=max(6.0, 0.8 * bt))
    luoi_b = sk.chuoi("luoi", "ham", dat_luoi.ra(Ll.khop(C["luoi_dot"]), *luoi_im.size))
    # ---- đuôi: đặt theo hai đầu khớp trên concept, trục ảnh xoay thêm goc_goc (gốc chĩa ra sau-hơi lên), curl uốn tới ngọn
    duoi_im = pc["duoi"]
    dat_duoi = dat_cua("duoi", neo=(0.02, 0.5), dgoc=C["duoi_goc"])
    nd = C["duoi_dot"]
    Ld = luoi.luoi_dai(duoi_im, nd, ten="duoi", buoc=bt)
    Jd = dat_duoi.ra(Ld.khop(nd), *duoi_im.size)
    duoi = sk.chuoi("duoi", "hong", Jd)
    # ---- chân: đặt theo hai đầu khớp, lưới vùng + trọng số chiếu
    legs = {}
    for nm, par in (("chan_tx", "nguc"), ("chan_sx", "hong"), ("chan_tn", "nguc"), ("chan_sn", "hong")):
        im = pc[nm]
        Lc = luoi.luoi_vung(im, bv, bt, ten=nm)
        dat = dat_cua(nm, neo=(0.5, 0.04))
        J = dat.ra([(im.width * 0.5, im.height * 0.04), (im.width * 0.45, im.height * 0.52), (im.width * 0.5, im.height * 0.97)], *im.size)
        J[-1, 1] = max(5.0, J[-1, 1])
        names = sk.chuoi(nm.replace("chan_", "c"), par, J)
        legs[nm] = (Lc, dat, names, J, par)
    # ---- slot (sau → trước)
    sk.slot("chan_sx", legs["chan_sx"][2][0], "chan_sx")
    sk.slot("chan_tx", legs["chan_tx"][2][0], "chan_tx")
    sk.slot("duoi", duoi[0], "duoi")
    sk.slot("chuy", duoi[-1], "chuy")
    for g in C["go"]:
        sk.slot(g, {"go_vai": "nguc", "go_lung": "than", "go_hong": "hong"}[g], g)
    sk.slot("sung_xa", "dau", "sung")
    sk.slot("than", "than", "than")
    sk.slot("chan_sn", legs["chan_sn"][2][0], "chan_sn")   # chân gần đè lên thân như concept (cả hai dạng)
    sk.slot("chan_tn", legs["chan_tn"][2][0], "chan_tn")
    sk.slot("mieng", "ham", "mieng")
    sk.slot("luoi", luoi_b[0], "luoi")
    sk.slot("ham", "ham", "ham")
    sk.slot("dau", "dau", "dau")
    sk.slot("mi", "dau", "mi", an=True)
    sk.slot("sung", "dau", "sung")
    # ---- thân: lưới vùng, bốn xương hoà theo khoảng cách đi trong lưới
    Lt = luoi.luoi_vung(pc["than"], bv, bt, ten="than")
    Wtn = trongso.vung(Lt, [("hong", [(0, 0), (0.30 * Wt, 0), (0.30 * Wt, Ht), (0, Ht)]),
                            ("co", [(0.90 * Wt, 0), (Wt, 0), (Wt, Ht), (0.90 * Wt, Ht)]),
                            ("nguc", [(0.62 * Wt, 0), (Wt, 0), (Wt, Ht), (0.62 * Wt, Ht)]),
                            ("than", [(0, 0), (Wt, 0), (Wt, Ht), (0, Ht)])], dai_hoa=0.11 * Wt)
    Wtn = trongso.lam_tron(Lt, Wtn, 2)
    trongso.kiem(Wtn, "than")
    sk.luoi_gan("than", "than", Lt, Wtn, dat=dat_than)
    # gờ băng: cứng, chân gờ chồng xuống lưng (dcy: dời xuống theo px concept)
    for g in C["go"]:
        sk.manh(g, g, dat_cua(g, dcy=C["go_chim"]))
    # đầu: lưới vùng; gáy hoà vào cổ
    Lh = luoi.luoi_vung(dau, bv, bt, ten="dau")
    Wh = trongso.vung(Lh, [("co", [(0, 0.25 * h), (0.14 * w, 0.4 * h), (0.14 * w, h), (0, h)]), ("dau", [(0, 0), (w, 0), (w, h), (0, h)])],
                      dai_hoa=0.09 * w)
    Wh = trongso.lam_tron(Lh, Wh, 1)
    trongso.kiem(Wh, "dau", cho_cung=("dau",))
    sk.luoi_gan("dau", "dau", Lh, Wh, dat=dat_dau)
    # hàm dưới: lưới hai xương, cùng tỉ lệ với đầu
    ham = pc["ham"]
    dat_ham = Dat(*hinge, goc=gj, ti=(dat_dau.sx * 0.85, dat_dau.sy * 0.85), neo=(0.05, 0.28))
    Lj = luoi.luoi_vung(ham, 0.85 * bv, 0.85 * bt, ten="ham")
    Wj = mieng.ham_hai_xuong(dat_ham.ra(Lj.pts, *ham.size), hinge, snout, "dau", "ham")
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dat_ham)
    mieng.long_mieng(sk, "mieng", "mieng", "dau", "ham", hinge, snout, duoi=-0.26, tren=(-0.03, -0.05, -0.08, -0.12, -0.16))
    Wl = trongso.chuoi(Ll.s, Ll.truc[1][-1] / C["luoi_dot"], luoi_b, cha="ham", cha_hoa=0.6)
    sk.luoi_gan("luoi", "luoi", Ll, Wl, dat=dat_luoi)
    # mí mắt
    eye = tim_mat(dau)
    if eye is None:
        eye = (0.62 * w, 0.42 * h)
        print("  (không tìm thấy mắt hổ phách trên ảnh đầu: dùng điểm ước)")
    kq = mieng.fit_lid(dau, pc["mi"], hat=(int(eye[0]), int(eye[1])), hop=(0.3 * w, 0.05 * h, 0.95 * w, 0.75 * h), ten=f"dạng {k}")
    sk.manh("mi", "mi", mieng.dat_mi(dat_dau, dau, kq))
    # sừng: cứng trên đầu, đặt theo dò khớp (gốc trong sọ)
    sk.manh("sung", "sung", dat_cua("sung"))
    sk.manh("sung_xa", "sung", dat_cua("sung_xa"))
    # đuôi + chùy (chùy đặt theo dò, bám đốt cuối)
    Wd = trongso.chuoi(Ld.s, Ld.truc[1][-1] / nd, duoi, cha="hong", cha_hoa=0.7)
    trongso.kiem(Wd, "duoi")
    sk.luoi_gan("duoi", "duoi", Ld, Wd, dat=dat_duoi)
    # chùy: concept cho vị trí lúc đuôi ĐÃ cong (curl); đốt cuối ở dáng gốc thẳng, nên gắn ở chỗ mà sau khi curl nó về đúng concept
    curl = np.linspace(*C["curl"], nd)
    Pc = khung.Pose()
    for i, b in enumerate(duoi):
        Pc.rot(b, float(curl[i]))
    Wc = sk.the_gioi(Pc)
    last = duoi[-1]
    ln = sk.bones[sk.bi[last]]["length"]
    tip_idle = (Wc[last] @ np.array([ln, 0.0, 1.0]))[:2]
    tip_rest = (sk.W0[last] @ np.array([ln, 0.0, 1.0]))[:2]
    th = float(curl.sum())
    pm = PL["chuy"]
    mace_rig = np.array(conv(pm["cx"], pm["cy"]))
    d = mace_rig - tip_idle
    cr, sr = math.cos(math.radians(-th)), math.sin(math.radians(-th))
    d_rest = np.array([cr * d[0] - sr * d[1], sr * d[0] + cr * d[1]])
    pos = tip_rest + d_rest
    t = tir["chuy"]
    sk.manh("chuy", "chuy", Dat(pos[0], pos[1], goc=pm["r"] - th, ti=(pm["sx"] * K / t, pm["sy"] * K / t), lat=pm["lat"]))
    print(f"  chùy: ngọn đuôi sau curl {tip_idle.round(0)} ↔ concept {mace_rig.round(0)} (đuôi xoay tổng {th:.0f}°)")
    for nm, (Lc, dat, names, J, par) in legs.items():
        Wc = trongso.chuoi_chieu(dat.ra(Lc.pts, *pc[nm].size), J, names, cha=par, cha_hoa=0.8)
        Wc = trongso.lam_tron(Lc, Wc, 1)
        sk.luoi_gan(nm, nm, Lc, Wc, dat=dat)
    for e, m in (("trung", "khung đòn thường trúng (cắn)"), ("phun", "bắt đầu phun hơi băng (VFX bám xương mieng)"),
                 ("het_phun", "hết phun"), ("gam", "chiêu cuối bung (gầm)"), ("het_gam", "hết chiêu cuối"),
                 ("nen", "chùy đuôi / chân nện đất (VFX cọc băng, tảng băng)")):
        sk.su_kien(e, m)
    foot = {nm: np.array(v[3][-1]) for nm, v in legs.items()}
    Hl = max(pc["chan_tn"].height, pc["chan_sn"].height)
    info = {"duoi": duoi, "luoi": luoi_b, "legs": {nm: v[2] for nm, v in legs.items()}, "foot": foot, "pc": pc, "Ht": Ht, "Wt": Wt,
            "Hl": Hl, "cy": float(P_than[1]), "k": k, "mat": tuple(dat_dau.mot(eye, w, h)), "K": K, "ground": (xg, yg),
            "ref_size": pj["ref_size"], "H_con": H_con, "buoc": (bv, bt)}
    print(f"  dạng {k}: thân {Wt}×{Ht}, chân cao {Hl}, tâm thân y {P_than[1]:.0f}; K={K}; {sk.tom_tat()}")
    return sk, info


LAI = {  # điểm đọc trên concept (px): khớp hàm, mút mõm (khép), điểm cổ (xương dau), gốc cổ (xương co), trục đuôi gốc → chùy
    2: dict(hinge=(1185, 462), snout=(1445, 445), jaw_tip=(1400, 548), neck=(1050, 395), co=(1010, 470),
            duoi=[(482, 600), (405, 565), (335, 515), (272, 450), (232, 395), (185, 345)]),
    1: dict(hinge=(1085, 545), snout=(1440, 520), jaw_tip=(1380, 640), neck=(880, 390), co=(840, 480),
            duoi=[(335, 655), (275, 640), (215, 625), (160, 605)]),
}


def dung_lai(k):
    """cách lai: lớp đầu (+ sừng), thân (+ cổ/họng + gờ), đuôi (+ chùy), bốn chân cắt thẳng từ concept (tm09_lai.py); mảnh GPT
    chỉ còn hàm dưới, lòng miệng, lưỡi, mí. Toạ độ rig = concept × K."""
    import json
    C = CFG[k]
    K = C["K"]
    Lc = LAI[k]
    lj = json.load(open(inbox(k, "manh_lai", "lop.json"), encoding="utf-8"))
    xg, yg = lj["ground"]
    W, H = lj["ref_size"]

    def conv(x, y):
        return (x - xg) * K, (yg - y) * K

    cpa = np.asarray(Image.open(inbox(k, "tai_ve", "L1_duyet.png")).convert("RGB"))
    y_top = int(np.nonzero((cpa.min(axis=2) < 225).any(axis=1))[0].min())
    H_con = (yg - y_top) * K
    bv, bt = 0.015 * H_con, 0.02 * H_con
    print(f"  dạng {k} (lai): chiều cao con {H_con:.0f} px rig → bước viền {bv:.1f}, bước trong {bt:.1f}")
    # ---- lớp từ concept
    pc, dat_l = {}, {}
    for n, L in lj["lop"].items():
        im = Image.open(inbox(k, "manh_lai", n + ".png")).convert("RGBA")
        im = im.resize((max(2, round(im.width * K)), max(2, round(im.height * K))), Image.LANCZOS)
        pc[n] = anh.loang_mau(im)
        x, y = conv(L["x0"], L["y0"])
        dat_l[n] = Dat(x, y, neo=(0.0, 0.0))
    # ---- mảnh GPT: hàm, lòng miệng, lưỡi, mí (cỡ theo hàm concept)
    hinge, snout = np.array(conv(*Lc["hinge"])), np.array(conv(*Lc["snout"]))
    dai_ham = float(np.hypot(*(snout - hinge)))
    gc = {"mi": ("mi", *C["giu_cho"]["mi"][1:], C["body"])}
    pg = anh.nap_manh(inbox(k, "manh"), gc, ti_le=0.55 * K)
    pc.update(pg)
    sk = khung.Sk(f"{CODE}_{k}")
    for n, im in pc.items():
        sk.anh(n, im)
    # ---- xương
    than_im = pc["than"]
    Lb = lj["lop"]["than"]
    bx0, by0 = conv(Lb["x0"], Lb["y0"])
    Wt, Ht = than_im.size
    P_than = (bx0 + 0.5 * Wt, by0 - 0.5 * Ht)
    P_hong = (bx0 + 0.18 * Wt, by0 - 0.55 * Ht)
    P_nguc = (bx0 + 0.66 * Wt, by0 - 0.5 * Ht)
    P_co = conv(*Lc["co"])
    neck = np.array(conv(*Lc["neck"]))
    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("than", "move", *P_than, dai=60)
    sk.xuong("hong", "than", *P_hong, the_gioi=True, dai=50)
    sk.xuong("nguc", "than", *P_nguc, the_gioi=True, dai=50)
    sk.xuong("co", "nguc", *P_co, the_gioi=True, dai=30)
    sk.xuong("dau", "co", *neck, the_gioi=True, dai=float(np.hypot(*(snout - neck))))
    jaw_tip = np.array(conv(*Lc["jaw_tip"]))
    gj = math.degrees(math.atan2(*(jaw_tip - hinge)[::-1]))   # hàm dưới ở dáng gốc ĐÃ há như concept
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*(jaw_tip - hinge))), the_gioi=True)
    sk.xuong("mieng", "dau", snout[0] + 6, snout[1] + 8, goc=-3, dai=30, the_gioi=True)
    luoi_b = []   # lưỡi nằm trong lớp hàm concept, không chuỗi riêng
    # đuôi: chuỗi theo trục đọc trên concept (đã cong sẵn), lưới vùng của lớp, trọng số geodesic từ khớp
    Jd = np.array([conv(*p) for p in Lc["duoi"]])
    duoi = sk.chuoi("duoi", "hong", Jd)
    nd = len(duoi)
    # chân: hai đầu khớp từ tm09_place.TWO (concept)
    import tm09_cfg_place as tp
    legs = {}
    for nm, par in (("chan_tx", "nguc"), ("chan_sx", "hong"), ("chan_tn", "nguc"), ("chan_sn", "hong")):
        if nm not in pc:
            continue
        q0, q1 = tp.TWO[k][nm][0], tp.TWO[k][nm][1]
        a, b = np.array(conv(*q0)), np.array(conv(*q1))
        b[1] = max(5.0, b[1])
        J = np.array([a, 0.5 * (a + b) + np.array([-0.06 * (b[1] - a[1]), 0.0]), b])
        names = sk.chuoi(nm.replace("chan_", "c"), par, J)
        legs[nm] = (names, J, par)
    # ---- slot (sau → trước)
    for nm in ("chan_sx", "chan_tx"):
        if nm in pc:
            sk.slot(nm, legs[nm][0][0], nm)
    sk.slot("duoi", duoi[0], "duoi")
    sk.slot("than", "than", "than")
    for nm in ("chan_sn", "chan_tn"):
        if nm in pc:
            sk.slot(nm, legs[nm][0][0], nm)
    sk.slot("ham", "ham", "ham")
    sk.slot("dau", "dau", "dau")
    sk.slot("mi", "dau", "mi", an=True)
    # ---- lưới + trọng số
    # thân: vùng theo x (hông / thân / ngực / cổ-họng)
    Lt = luoi.luoi_vung(than_im, bv, bt, ten="than")
    Wtn = trongso.vung(Lt, [("hong", [(0, 0), (0.30 * Wt, 0), (0.30 * Wt, Ht), (0, Ht)]),
                            ("co", [(0.86 * Wt, 0), (Wt, 0), (Wt, Ht), (0.86 * Wt, Ht)]),
                            ("nguc", [(0.58 * Wt, 0), (Wt, 0), (Wt, Ht), (0.58 * Wt, Ht)]),
                            ("than", [(0, 0), (Wt, 0), (Wt, Ht), (0, Ht)])], dai_hoa=0.11 * Wt)
    Wtn = trongso.lam_tron(Lt, Wtn, 2)
    trongso.kiem(Wtn, "than")
    sk.luoi_gan("than", "than", Lt, Wtn, dat=dat_l["than"])
    # đầu (+ sừng): gáy / dưới cằm hoà vào cổ
    dau = pc["dau"]
    w, h = dau.size
    Lh = luoi.luoi_vung(dau, bv, bt, ten="dau")
    nk = dat_l["dau"]
    # vùng cổ trên lớp đầu = quanh điểm cổ (toạ độ lớp)
    px = (np.array(conv(*Lc["co"])) - np.array([nk.x, nk.y])) * np.array([1, -1])
    r = 0.12 * w
    Wh = trongso.vung(Lh, [("co", [(px[0] - r, px[1] - r), (px[0] + r, px[1] - r), (px[0] + r, px[1] + r), (px[0] - r, px[1] + r)]),
                           ("dau", [(0, 0), (w, 0), (w, h), (0, h)])], dai_hoa=0.08 * w)
    Wh = trongso.lam_tron(Lh, Wh, 1)
    trongso.kiem(Wh, "dau", cho_cung=("dau",))
    sk.luoi_gan("dau", "dau", Lh, Wh, dat=nk)
    # hàm dưới = lớp concept (hàm + lòng miệng + lưỡi, thịt trong miệng theo hàm): hai xương, sát bản lề hoà vào đầu
    ham = pc["ham"]
    Lj = luoi.luoi_vung(ham, 0.85 * bv, 0.85 * bt, ten="ham")
    Wj = mieng.ham_hai_xuong(dat_l["ham"].ra(Lj.pts, *ham.size), hinge, jaw_tip, "dau", "ham", u0=-0.05, u1=0.18)
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dat_l["ham"])
    # mí: dò trên lớp đầu (cắt từ concept)
    eye = tim_mat(dau)
    if eye is None:
        eye = (0.62 * w, 0.55 * h)
        print("  (không tìm thấy mắt hổ phách trên lớp đầu: dùng điểm ước)")
    kq = mieng.fit_lid(dau, pc["mi"], hat=(int(eye[0]), int(eye[1])), hop=(0.3 * w, 0.3 * h, 0.95 * w, 0.85 * h), ten=f"dạng {k} (lai)")
    sk.manh("mi", "mi", mieng.dat_mi(nk, dau, kq))
    # đuôi: lưới vùng, trọng số geodesic từ khớp (trục cong)
    Ld = luoi.luoi_vung(pc["duoi"], bv, bt, ten="duoi")
    dk = dat_l["duoi"]
    J_img = np.array([[(x - dk.x), (dk.y - y)] for x, y in Jd])
    Wd = trongso.chuoi_geo(Ld, J_img, duoi, cha="hong", cha_hoa=0.7)
    Wd = trongso.lam_tron(Ld, Wd, 1)
    trongso.kiem(Wd, "duoi")
    sk.luoi_gan("duoi", "duoi", Ld, Wd, dat=dk)
    # chân: lưới vùng, trọng số chiếu lên khớp
    for nm, (names, J, par) in legs.items():
        im = pc[nm]
        Lg = luoi.luoi_vung(im, bv, bt, ten=nm)
        Wc = trongso.chuoi_chieu(dat_l[nm].ra(Lg.pts, *im.size), J, names, cha=par, cha_hoa=0.8)
        Wc = trongso.lam_tron(Lg, Wc, 1)
        sk.luoi_gan(nm, nm, Lg, Wc, dat=dat_l[nm])
    for e, m in (("trung", "khung đòn thường trúng (cắn)"), ("phun", "bắt đầu phun hơi băng (VFX bám xương mieng)"),
                 ("het_phun", "hết phun"), ("gam", "chiêu cuối bung (gầm)"), ("het_gam", "hết chiêu cuối"),
                 ("nen", "chùy đuôi / chân nện đất (VFX cọc băng, tảng băng)")):
        sk.su_kien(e, m)
    foot = {nm: np.array(v[1][-1]) for nm, v in legs.items()}
    Hl = max(pc[n].height for n in legs)
    info = {"duoi": duoi, "luoi": luoi_b, "legs": {nm: v[0] for nm, v in legs.items()}, "foot": foot, "pc": pc, "Ht": Ht, "Wt": Wt,
            "Hl": Hl, "cy": float(P_than[1]), "k": k, "mat": tuple(nk.mot(eye, w, h)), "K": K, "ground": (xg, yg),
            "ref_size": [W, H], "H_con": H_con, "buoc": (bv, bt)}
    print(f"  dạng {k} (lai): thân {Wt}×{Ht}, chân cao {Hl}; {sk.tom_tat()}")
    return sk, info


# ---------------------------------------------------------------- clip
def clips(sk, info, k):
    duoi, luoi_b, legs, foot = info["duoi"], info["luoi"], info["legs"], info["foot"]
    Hc = info["cy"] + 0.5 * info["Ht"]            # cỡ chuyển động: lưng
    nd = len(duoi)
    big = k == 2
    tail_amp = np.linspace(1.4, 5.0, nd) * (0.8 if big else 1.0)
    curl = np.linspace(*CFG[k]["curl"], nd)   # đuôi vểnh sẵn (dáng concept)
    mem = [LoXo(duoi, k=list(np.linspace(420, 150, nd)), damp=0.62, maxang=10),
           ] + ([DayMem(luoi_b, k0=0.3, k1=0.12, zeta=0.55, lim=(10, 16), luc=lambda t, i: np.array([0.0, -500.0 * (1 + i)]))] if luoi_b else [])
    HM = CFG[k].get("ham_mo", 0.0)   # hàm ở dáng gốc đã há HM độ (lớp concept): "khép" = xoay +HM; "há thêm" = âm

    def cuon(P):
        """dáng nghỉ: đuôi vểnh (curl) và miệng hé như concept: phải có ở MỌI clip, mọi khung, kể cả die, evolve."""
        for i, b in enumerate(duoi):
            P.rot(b, curl[i])
        P.rot("ham", -CFG[k]["ham_nghi"])

    def nen(P, tt, amp=1.0, win=None):
        """chuyển động nền idle. Mọi dao động nhân cửa sổ win (mặc định sin²(π tt / 2): 0 ở t = 0 và t = 2 của idle) nên khung 0
        idle = dáng nghỉ thuần; clip không lặp truyền win = sin²(π t / D) để khung đầu và khung cuối cũng là dáng nghỉ."""
        w = (math.sin(math.pi * tt / 2.0) ** 2 if win is None else win) * amp
        s, c = song(tt, 2.0), song(tt, 2.0, math.pi)
        P.move("than", 0, 2.6 * s * w)
        P.rot("nguc", 1.4 * c * w)
        P.rot("hong", -0.9 * c * w)
        P.rot("dau", (-1.6 * c + 1.0 * song(tt, 1.0)) * w)
        cuon(P)
        chuoi_song(P, duoi, tt, 2.0, tail_amp * w, tre=0.11, ngon_dan=False)

    def wclip(t, D):
        return math.sin(math.pi * min(max(t / D, 0.0), 1.0)) ** 2

    def feet(P, nang=None, theo_move=True):
        """bàn chân bám đất theo move (theo_move=False: bám đất tuyệt đối, thân hạ xuống thì chân gập); nang = {chân: (dx, dy)}."""
        W = sk.the_gioi(P)
        for nm, names in legs.items():
            f = foot[nm]
            tgt = (W["move"] @ np.array([f[0], f[1], 1.0]))[:2] if theo_move else np.array(f, float)
            if nang and nm in nang:
                tgt = tgt + np.asarray(nang[nm], float)
            hoat.ik_hai_doan(sk, P, names[0], names[1], tgt)

    def idle_fn(t, P):
        nen(P, t)
        P.rot("ham", cv(t, [(0, 0), (0.55, 0), (0.68, 0.8 * HM, "out"), (0.78, 0.25 * HM), (0.9, 0.7 * HM, "out"), (1.08, 0, "io"), (2.0, 0)]))  # táp nhẹ (khép)
        an_hien(P, "mi", t, [(1.36, 1.48)])
        feet(P)

    def appear_fn(t, P, D=1.2):
        g = cv(t, [(0, 0.02), (0.42, 1.1, "out"), (0.6, 0.95, "io"), (0.8, 1.0, "io"), (D, 1.0)])
        P.scale("move", g, g)
        a = cv(t, [(0, 0), (0.12, 1)])
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a
        nen(P, t, ease((t - 0.5) / 0.6), win=wclip(t, D))
        P.rot("dau", 9 * cv(t, [(0, 0), (0.68, 0), (0.84, 1, "out"), (1.06, 0, "io"), (D, 0)]))
        P.rot("ham", -(12 if big else 9) * cv(t, [(0, 0), (0.68, 0), (0.84, 1, "out"), (1.06, 0, "io"), (D, 0)]))
        feet(P)

    # đòn thường: cắn. Dạng 2 Băng Nha: lấy đà dài hơn, há to hơn, chùy đuôi nện đất cùng khung táp
    def attack_fn(t, P, D=1.0 if big else 0.9, H=0.55 if big else 0.5):
        A0 = H - 0.25
        lean = cv(t, [(0, 0), (A0, 1, "io"), (A0 + 0.05, 1.06), (H, -1.1, "in"), (H + 0.06, -1.2), (H + 0.22, -1.05, "io"), (D, 0, "io")])
        nen(P, t, 1 - 0.7 * hoat.bao(t, 0.08, D - 0.1, 0.2, 0.25), win=wclip(t, D))
        lao = (0.55 if big else 0.42) * Hc
        P.move("move", cv(t, [(0, 0), (A0, -0.08 * Hc, "io"), (H, lao, "in"), (H + 0.2, lao * 0.9), (D, 0, "io")]),
               cv(t, [(0, 0), (A0, -0.03 * Hc, "io"), (H - 0.05, 0.03 * Hc), (H + 0.1, 0), (D, 0)]))
        P.rot("nguc", 5 * lean)
        P.rot("hong", -3 * lean)
        P.rot("dau", (10 if big else 8) * lean)
        mo = 18 if big else 12
        P.rot("ham", -cv(t, [(0, 0), (A0 - 0.05, mo * 0.5, "io"), (H - 0.03, mo), (H, -HM, "in"), (H + 0.06, -HM + 5), (H + 0.25, -0.8 * HM), (D, 0, "io")]))
        P.scale("dau", cv(t, [(0, 1), (H - 0.03, 1), (H, 1.13), (H + 0.05, 0.97), (H + 0.2, 1), (D, 1)]),
                cv(t, [(0, 1), (H - 0.03, 1), (H, 0.92), (H + 0.05, 1.03), (H + 0.2, 1), (D, 1)]))
        # đuôi (chuỗi lật: góc ÂM = nhấc lên): nhấc chùy lúc lấy đà → nện xuống ĐÚNG khung táp H → dội nhẹ → về
        q = cv(t, [(0, 0), (A0, -1, "io"), (H - 0.02, -1.15), (H, 1.2, "in"), (H + 0.08, 0.55, "out"), (H + 0.2, 0.8, "io"), (D, 0, "io")])
        for i, b in enumerate(duoi):
            P.rot(b, (3 + 2.2 * i) * q * (1.0 if big else 0.7))
        feet(P)

    # chiêu bắn: phun hơi băng từ miệng, đứng tại chỗ, giữ há rung hai dáng
    def cast_fn(t, P, D=1.3 if big else 1.0, H=0.52, E=1.08 if big else 0.84):
        rear = cv(t, [(0, 0), (0.4, 1, "io"), (0.47, 1.06), (H, -0.6, "in"), (H + 0.08, -0.72), (E, -0.55), (D, 0, "io")])
        nen(P, t, 1 - 0.8 * hoat.bao(t, 0.1, D - 0.05, 0.2, 0.2), win=wclip(t, D))
        P.rot("nguc", (6 if big else 5) * rear)
        P.rot("hong", -2 * rear)
        P.rot("dau", (10 if big else 8) * rear + 1.3 * rung(t, H + 0.04, E))
        mo = 16 if big else 12
        P.rot("ham", -(cv(t, [(0, 0), (0.4, -0.5 * HM, "io"), (H, mo, "out"), (E, mo * 0.9), (D, 0, "io")]) + 3 * rung(t, H + 0.04, E)))
        P.move("move", cv(t, [(0, 0), (H, 0), (H + 0.08, -0.04 * Hc, "out"), (E, -0.025 * Hc), (D, 0, "io")]),
               cv(t, [(0, 0), (0.4, 0.02 * Hc, "io"), (H, 0.0), (D, 0)]))
        for i, b in enumerate(duoi):   # ngửa tụ: đuôi nhấc nhẹ
            P.rot(b, -(2 + 1.5 * i) * max(rear, 0) * 0.5)
        feet(P)

    if big:
        # Băng Hà Sụp: tụ (khom, đuôi dựng cao), ngẩng gầm há tối đa, chùy đuôi nện đất, giữ rung, về
        def skill_fn(t, P, D=2.0, H=0.8, N=0.93, E=1.5):
            cr = cv(t, [(0, 0), (0.55, 1, "io"), (0.64, 1.06), (H, -1, "out"), (E, -1), (D, 0, "io")])
            nen(P, t, 1 - 0.85 * hoat.bao(t, 0.1, D - 0.1, 0.25, 0.4), win=wclip(t, D))
            P.scale("move", 1 + 0.04 * max(cr, 0) - 0.03 * min(cr, 0), 1 - 0.08 * max(cr, 0) + 0.06 * min(cr, 0))
            P.move("move", 0, cv(t, [(0, 0), (0.55, -0.03 * Hc, "io"), (H, 0.05 * Hc, "out"), (E, 0.03 * Hc), (D, 0, "io")]))
            P.rot("nguc", -5 * cr + 1.6 * rung(t, H + 0.04, E))
            P.rot("hong", 2 * cr)
            P.rot("dau", -14 * cr + 2.2 * rung(t, H + 0.04, E))
            P.rot("ham", -(cv(t, [(0, 0), (0.55, -0.6 * HM), (H, 26, "out"), (E, 22), (D, 0, "io")]) + 4 * rung(t, H + 0.04, E)))
            P.scale("dau", cv(t, [(0, 1), (0.55, 0.98), (H, 1.08, "out"), (H + 0.15, 1.0), (D, 1)]))
            # đuôi (góc âm = nhấc): dựng cao lúc tụ, nện xuống ở N, dội nhẹ rồi giữ rung
            q = cv(t, [(0, 0), (0.55, -1, "io"), (H, -1.3, "io"), (N, 1.2, "in"), (N + 0.08, 0.7, "out"), (E, 0.8), (D, 0, "io")])
            for i, b in enumerate(duoi):
                P.rot(b, (5 + 2.5 * i) * q + 1.0 * rung(t, N + 0.1, E))
            feet(P)
        sk_ev = [(0.8, "gam", ""), (0.93, "nen", ""), (1.5, "het_gam", "")]
        sk_D = 2.0
    else:
        # Cọc Băng: nhấc chân trước gần, dậm xuống (nen), gầm nhỏ, giữ rung, về
        def skill_fn(t, P, D=1.7, H=0.7, E=1.25):
            cr = cv(t, [(0, 0), (0.45, 1, "io"), (0.5, 1.06), (H, -1, "in"), (H + 0.05, -1.15), (E, -0.9), (D, 0, "io")])
            nen(P, t, 1 - 0.85 * hoat.bao(t, 0.1, D - 0.1, 0.25, 0.4), win=wclip(t, D))
            P.rot("nguc", -7 * cr + 1.4 * rung(t, H + 0.04, E))
            P.rot("hong", 3 * cr)
            P.rot("dau", -8 * cr + 1.8 * rung(t, H + 0.04, E))
            P.rot("ham", -(cv(t, [(0, 0), (0.45, -0.5 * HM), (H, 16, "out"), (E, 12), (D, 0, "io")]) + 3 * rung(t, H + 0.04, E)))
            # chồm: nửa trước nhấc lên (hai chân trước rời đất, thấy rõ dù chân vẽ sau thân) rồi dậm cả hai chân xuống ở H
            P.move("move", 0, cv(t, [(0, 0), (0.45, 0.12 * Hc, "io"), (H - 0.03, 0.13 * Hc), (H, -0.04 * Hc, "in"), (H + 0.1, 0), (D, 0)]))
            up = cv(t, [(0, 0), (0.3, 0), (0.5, 1, "io"), (H - 0.03, 1.05), (H, 0, "in"), (D, 0)])
            P.rot("hong", 6 * up)
            for i, b in enumerate(duoi):   # nhấc đuôi lúc lấy đà (góc âm = nhấc)
                P.rot(b, -(3 + 2 * i) * max(cr, 0) * 0.8)
            feet(P, nang={"chan_tn": (0.1 * Hc * up, 0.3 * Hc * up), "chan_tx": (0.06 * Hc * up, 0.22 * Hc * up)})
        sk_ev = [(0.7, "gam", ""), (0.7, "nen", ""), (1.25, "het_gam", "")]
        sk_D = 1.7

    def hit_fn(t, P, D=0.6):
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 0.55, "io"), (0.42, -0.12, "io"), (D, 0, "io")])
        bd = cv(t, [(0, 0), (0.07, 0.3, "out"), (0.2, 1, "io"), (0.44, -0.05, "io"), (D, 0, "io")])
        nen(P, t, ease((t - 0.25) / 0.35), win=wclip(t, D))
        P.rot("dau", 15 * hd)
        P.rot("nguc", 6 * bd)
        P.move("move", -(0.05 if big else 0.07) * Hc * bd, 0.012 * Hc * hd)
        P.rot("ham", -8 * hd)
        an_hien(P, "mi", t, [(0.03, 0.32)])
        for i, b in enumerate(duoi):   # sóng chạy từ ngọn về gốc (văng lên), chùy văng sau cùng
            P.rot(b, -(5 + 2 * i) * cv(t, [(0, 0), (0.07 + 0.03 * (nd - 1 - i), 1, "out"), (0.35 + 0.03 * i, -0.3, "io"), (D, 0, "io")]))
        feet(P)

    def die_fn(t, P, D=1.9):
        # giật, nhắm mắt → lả đi (đầu gục, hàm trễ, lưỡi thè) → khuỵu xuống bụng chạm đất, chân dang → băng rụng → tan
        cuon(P)
        P.rot("dau", cv(t, [(0, 0), (0.07, 14, "out"), (0.3, 6), (0.85, -26, "io"), (1.25, -30), (D, -30)]))
        P.rot("ham", -cv(t, [(0, 0), (0.07, 10, "out"), (0.3, 3), (0.85, 12, "io"), (D, 14)]))
        P.rot("nguc", cv(t, [(0, 0), (0.07, 5, "out"), (0.85, -6, "io"), (D, -6)]))
        P.rot("hong", cv(t, [(0, 0), (0.85, 0), (1.25, 5, "io"), (D, 5)]))
        for i, b in enumerate(luoi_b):
            P.rot(b, cv(t, [(0, 0), (0.3, 0), (0.85, -12, "io"), (D, -12)]))
        drop = cv(t, [(0, 0), (0.85, 0), (1.22, 1, "in"), (1.3, 0.94, "out"), (D, 0.96)])
        P.move("move", 0, -info["cy"] * 0.52 * drop)
        for i, b in enumerate(duoi):   # giật nhấc nhẹ rồi rũ xuống đất (góc dương = hạ)
            P.rot(b, cv(t, [(0, 0), (0.07, -5, "out"), (0.85, -1), (1.22, 4 + 1.6 * i, "in"), (1.4, 2.5 + 1.2 * i, "out"), (D, 3 + 1.2 * i)]))
        an_hien(P, "mi", t, [(0.04, D + 1)])
        a = cv(t, [(0, 1), (1.45, 1), (1.85, 0, "io"), (D, 0)])
        a_ice = cv(t, [(0, 1), (1.1, 1), (1.42, 0, "io"), (D, 0)])
        for s in sk.slots:
            nm = s["name"]
            if nm in ("sung", "sung_xa", "chuy") or nm.startswith("go"):
                P.alpha[nm] = a_ice
            elif nm == "mi":
                P.alpha[nm] = P.alpha.get(nm, 0.0) * a
            elif s["alpha"] > 0:
                P.alpha[nm] = a
        feet(P, nang={nm: ((0.16 if "t" in nm[5:] else -0.16) * Hc * drop, 0) for nm in legs}, theo_move=False)

    out = [Clip("appear", 1.2, appear_fn, mem=mem),
           Clip("idle", 2.0, idle_fn, loop=True, mem=mem),
           Clip("attack", 1.0 if big else 0.9, attack_fn, ev=[(0.55 if big else 0.5, "trung", "")], mem=mem),
           Clip("cast", 1.3 if big else 1.0, cast_fn, ev=[(0.52, "phun", ""), (1.08 if big else 0.84, "het_phun", "")], mem=mem),
           Clip("skill", sk_D, skill_fn, ev=sk_ev, mem=mem),
           Clip("hit", 0.6, hit_fn, mem=mem),
           Clip("die", 1.9, die_fn, mem=[LoXo(duoi, k=list(np.linspace(1400, 700, nd)), damp=0.8, maxang=6)] + mem[1:])]
    return out


def so_concept(sk, P0, k, ra, info):
    """khung 0 idle vẽ đúng vào khung concept (rig = concept × K) | concept | chồng 55% | mặt nạ khác (đỏ: concept có mà rig
    thiếu, lam: rig thừa). In IoU mặt nạ. Trả IoU."""
    from PIL import ImageDraw
    K = info["K"]
    xg, yg = info["ground"]
    W, H = info["ref_size"]
    ve = soi.Ve(sk)
    box = (-xg * K, (yg - H) * K, (W - xg) * K, yg * K)
    rig_im = ve.ve(P0, box, 1.0 / K, bg=None, ss=2).convert("RGBA")
    if rig_im.size != (W, H):
        rig_im = rig_im.resize((W, H), Image.LANCZOS)
    cp = Image.open(os.path.join(HERE, "inbox", f"{CODE}_{k}", "tai_ve", "L1_duyet.png")).convert("RGB")
    a = np.asarray(cp)
    m_cp = ~anh.nen_tu_mep(a.min(axis=2) > 225)      # nền = vùng sáng nối mép (băng nhạt bên trong vẫn là hình)
    m_rig = np.asarray(rig_im)[..., 3] > 160
    inter, uni = int((m_cp & m_rig).sum()), int((m_cp | m_rig).sum())
    iou = inter / max(1, uni)
    bb = ve.bao(P0)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    ys, xs = np.nonzero(m_cp | m_rig)
    x0, y0, x1, y1 = max(0, xs.min() - 20), max(0, ys.min() - 20), min(W, xs.max() + 20), min(H, ys.max() + 20)
    cp_c = cp.crop((x0, y0, x1, y1)).convert("RGBA")
    rig_c = rig_im.crop((x0, y0, x1, y1))
    rig_w = Image.new("RGBA", cp_c.size, (255, 255, 255, 255))
    rig_w.alpha_composite(rig_c)
    ov = cp_c.copy()
    r2 = rig_c.copy()
    r2.putalpha(r2.getchannel("A").point(lambda v: v * 55 // 100))
    ov.alpha_composite(r2)
    diff = np.full((y1 - y0, x1 - x0, 3), 255, np.uint8)
    mc, mr = m_cp[y0:y1, x0:x1], m_rig[y0:y1, x0:x1]
    diff[mc & ~mr] = (230, 60, 60)
    diff[~mc & mr] = (60, 110, 230)
    diff[mc & mr] = (205, 205, 205)
    tiles = [cp_c.convert("RGB"), rig_w.convert("RGB"), ov.convert("RGB"), Image.fromarray(diff)]
    sc = 760.0 / tiles[0].width
    tiles = [t.resize((760, max(1, round(t.height * sc))), Image.LANCZOS) for t in tiles]
    th = tiles[0].height
    out = Image.new("RGB", (760 * 4 + 60, th + 30), (255, 255, 255))
    d = ImageDraw.Draw(out)
    f = anh.font(16)
    labels = [f"concept dạng {k} (L1_duyet)", f"rig khung 0 idle (bao {bw:.0f}x{bh:.0f}, cao/rộng {bh / bw:.2f})",
              "chồng: concept + rig 55%", f"IoU mặt nạ = {iou:.3f} (đỏ: concept có, rig thiếu; lam: rig thừa)"]
    for i, (t, lb) in enumerate(zip(tiles, labels)):
        out.paste(t, (i * 780, 30))
        d.text((i * 780 + 6, 6), lb, fill=(0, 0, 0), font=f)
    out.save(ra)
    print(f"  so concept dạng {k}: IoU mặt nạ khung 0 idle / concept = {iou:.3f}")
    return iou


def uon_thu(sk, info, ra):
    """uốn thử: đuôi mỗi đốt 18°, gối 40°, đầu 18°, hàm há 40°, lưỡi: soi lưới cong trơn, không gập ở khớp, miệng không hở."""
    P = khung.Pose()
    for b in info["duoi"]:
        P.rot(b, 18)
    for nm, names in info["legs"].items():
        P.rot(names[0], 22)
        P.rot(names[1], -40)
    P.rot("dau", 18)
    P.rot("ham", -14)
    for b in info["luoi"]:
        P.rot(b, -12)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    a = ve.ve(P, B, 1.6, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 110))
    a.convert("RGB").save(ra)
    return ra


def rig(k, sk2=None, fr2=None, cl2=None):
    t0 = time.time()
    ra = inbox(k, "rig")
    sk, info = dung_lai(k) if os.path.exists(inbox(k, 'manh_lai', 'lop.json')) else dung(k)
    cl = clips(sk, info, k)
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    print(f"  dạng {k}: nướng {len(cl)} clip ({time.time() - t0:.1f} s)")
    can = [("can_mieng_skill", "skill", 0.85 if k == 2 else 0.72, "ham", 0.5 * info["Ht"]),
           ("can_mieng_cast", "cast", 0.6, "ham", 0.5 * info["Ht"]),
           ("can_co_attack", "attack", 0.55 if k == 2 else 0.5, "co", 0.6 * info["Ht"]),
           ("can_duoi_hit", "hit", 0.1, info["duoi"][len(info["duoi"]) // 2], 0.7 * info["Ht"]),
           ("can_mi_hit", "hit", 0.1, info["mat"], 0.3 * info["Ht"]),
           ("can_goi_attack", "attack", 0.55 if k == 2 else 0.5, info["legs"]["chan_tn"][1], 0.5 * info["Hl"]),
           # cận má–cổ ở khung đầu xoay mạnh nhất từng clip, và bụng–chân trước lúc lấy đà
           ("can_co_skill", "skill", 0.8 if k == 2 else 0.7, "co", 0.45 * info["Ht"]),
           ("can_co_attack2", "attack", 0.3 if k == 2 else 0.25, "co", 0.45 * info["Ht"]),
           ("can_co_hit", "hit", 0.07, "co", 0.45 * info["Ht"]),
           ("can_co_cast", "cast", 0.52, "co", 0.45 * info["Ht"]),
           ("can_co_die", "die", 1.25, "co", 0.45 * info["Ht"]),
           ("can_bung_attack", "attack", 0.27, info["legs"]["chan_tn"][0], 0.5 * info["Hl"])]
    if k == 1:
        can += [("can_co_evolve", "evolve", 0.76, "co", 0.45 * info["Ht"]), ("can_co_evolve2", "evolve", 1.02, "co", 0.45 * info["Ht"])]
    frM, clM, M = fr, cl, sk
    # con dài dẹt: game co theo height nên khai chiều cao hiệu dụng = max(cao thật, rộng / 1.42) cho vừa sân (max_w của beast.py)
    ve0 = soi.Ve(sk)
    bx = ve0.bao(fr["idle"][0])
    cao_that, rong = soi.chieu_cao(ve0, fr["idle"][0]), bx[2] - bx[0]
    cao = max(cao_that, rong / 2.0)   # cá sấu dài: cho rộng tới 2 lần cao (Thanh Long dùng 1,42)
    print(f"  dạng {k}: cao thật {cao_that:.0f}, rộng {rong:.0f} → height khai {cao:.0f}")
    # khung ĐẦU mỗi clip so với khung 0 idle, đo trên đỉnh lưới đã vẽ của mọi slot (gồm lò xo, curl)
    noi = {}
    for c in cl:
        if c.ten in ("idle", "appear"):
            continue
        d, wsl = soi.lech(ve0, fr[c.ten][0], fr["idle"][0])
        noi[c.ten + "_dau"] = f"khung ĐẦU {c.ten} lệch khung 0 idle {d:.2f} px" + (f" ({wsl})" if wsl else "")
        print("  " + noi[c.ten + "_dau"])
    iou = so_concept(sk, fr["idle"][0], k, os.path.join(ra, "so_concept.png"), info)
    noi["so_concept"] = f"IoU mặt nạ khung 0 idle so concept {iou:.3f}"
    if k == 1 and sk2 is not None:
        ve1, ve2 = soi.Ve(sk), soi.Ve(sk2)
        hA, hB = soi.chieu_cao(ve1, fr["idle"][0]), soi.chieu_cao(ve2, fr2["idle"][0])
        M = tienhoa.gop(sk, sk2)

        curl1 = np.linspace(*CFG[1]["curl"], len(info["duoi"]))
        curl2 = np.linspace(*CFG[2]["curl"], len(sk2.info.get("duoi", [])))

        def gong(t, P):   # dạng cũ gồng: khom, ngửa đầu, há, đuôi dựng (khung 0 = dáng nghỉ: có curl, không dao động)
            for i, b in enumerate(info["duoi"]):
                P.rot(b, curl1[i])
            P.rot("ham", -CFG[1]["ham_nghi"])
            sq = cv(t, [(0, 0), (0.3, -0.07), (0.45, 0.06, "out"), (1.0, 0.04), (1.3, 0.0)])
            P.scale("move", 1 - 0.5 * sq, 1 + sq)
            P.rot("dau", cv(t, [(0, 0), (0.3, -5), (0.6, 12, "out"), (1.3, 14)]) + 1.5 * rung(t, 0.5, 1.3))
            P.rot("ham", -cv(t, [(0, 0), (0.3, -0.5 * CFG[1].get("ham_mo", 0)), (0.6, 10, "out"), (1.3, 12)]))
            for i, b in enumerate(info["duoi"]):
                P.rot(b, -(3 + 2 * i) * cv(t, [(0, 0), (0.6, 1, "io"), (1.3, 1)]))

        def gam(t, P, fl):  # dạng sau gầm, đuôi chùy nhấc lên
            for i, b in enumerate(sk2.info.get("duoi", [])):
                P.rot("n_" + b, curl2[i] - (3 + 2 * i) * fl)
            P.rot("n_ham", -CFG[2]["ham_nghi"])
            P.rot("n_dau", 12 * fl)
            P.rot("n_ham", -18 * fl)
            P.scale("n_move", 1 + 0.05 * fl, 1 + 0.05 * fl)

        memM = cl[1].mem + tienhoa.doi_ten_mem(cl2[1].mem)
        ev = tienhoa.clip_tien_hoa(M, sk, sk2, fr2["idle"][0], tiB=hA / hB, fnA=gong, fnB=gam, mem=memM)
        clM = list(cl) + [ev]
        frM = dict(fr)
        frM["evolve"] = hoat.nuong(M, ev)
        _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], hA / hB)
        noi["evolve"] = s_ev + f" (dạng sau co {hA / hB:.3f} trong rig gộp)"
        d0, w0 = soi.lech(soi.Ve(M), frM["evolve"][0], frM["idle"][0])
        noi["evolve_dau"] = f"khung ĐẦU evolve lệch khung 0 idle {d0:.2f} px" + (f" ({w0})" if w0 else "")
        print("  evolve:", s_ev, "|", noi["evolve_dau"])
    tong = xuat.xuat_het(M, clM, ra, f"{CODE}_{k}", f"Hàn Ngạc dạng {k}: {TEN[k]}", frames=frM, dang=k, so_dang=2, ma_goc=3281,
                         can=can, noi_them=noi, dung_yen=("cast", "skill"), cao=cao)
    uon_thu(sk, info, os.path.join(ra, "uon_thu.png"))
    sk.info["duoi"] = info["duoi"]
    tk = sk.tom_tat()
    with open(os.path.join(ra, "so_sanh.md"), "a", encoding="utf-8") as f:
        f.write("\n## Mật độ lưới theo chiều cao con\n\n"
                f"Chiều cao con {info['H_con']:.0f} px rig; bước viền {info['buoc'][0]:.1f} px (1,5 %), bước trong "
                f"{info['buoc'][1]:.1f} px (2 %); {tk['dinh']} đỉnh / {info['H_con']:.0f} px = {tk['dinh'] / info['H_con']:.2f} "
                "đỉnh mỗi px chiều cao (riêng dạng này, chưa gộp).\n")
    print(f"  mật độ: {tk['dinh']} đỉnh / cao {info['H_con']:.0f} = {tk['dinh'] / info['H_con']:.2f} đỉnh/px")
    print(f"  dạng {k} xong {time.time() - t0:.1f} s; .atomik {tong['atomik_kb']:.0f} KB")
    return sk, fr, cl, tong


def main(argv):
    cmd = argv[0] if argv else "all"
    if cmd == "cat":
        cat(int(argv[1]))
    elif cmd == "rig":
        k = int(argv[1])
        if k == 2:
            rig(2)
        else:
            sk2, info2 = dung_lai(2) if os.path.exists(inbox(2, 'manh_lai', 'lop.json')) else dung(2)
            cl2 = clips(sk2, info2, 2)
            sk2.info["duoi"] = info2["duoi"]
            fr2 = {c.ten: hoat.nuong(sk2, c) for c in cl2}
            rig(1, sk2, fr2, cl2)
    elif cmd == "all":
        sk2, fr2, cl2, _ = rig(2)
        rig(1, sk2, fr2, cl2)
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
