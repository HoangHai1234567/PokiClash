# -*- coding: utf-8 -*-
"""Rig Liên Kình (tm07, lô 10 tướng mới đảo Thủy 2026-11-11): cá kỳ lân biển cõng hoa sen, hai dạng, dựng bằng thư viện quai/.
Dạng 2 Liên Kình (trưởng thành) làm trước; dạng 1 Kình Nụ (bé) gộp dạng 2 để tiến hóa.

    py -3 -I ArtGen/Spine/tm07.py cat 2        cắt tờ mảnh M01..M03 của dạng 2 vào inbox/tm07_2/manh/ (+ _soi.png)
    py -3 -I ArtGen/Spine/tm07.py soi 2        dựng rig (hình giữ chỗ nếu thiếu), vẽ dáng gốc có xương để chỉnh chỗ đặt
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/tm07.py rig 2     nướng clip, xuất inbox/tm07_2/rig/
    ... rig 1                                   dạng 1 + gộp dạng 2 (evolve); cần rig 2 đã chạy trong cùng lệnh: dùng `all`
    ... all                                     rig 2 rồi rig 1

Toạ độ rig = pixel concept × SC, gốc ở chân (đáy nước, giữa), y lên, con nhìn sang phải. Nước: mảnh sóng đã cắt của Hải Long
(inbox/hai_long/manh, cùng ba màu lam), băng chuyền cuộn sóng hai bản sao lệch nửa chu kỳ trong clip lặp `aura`.
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from quai import anh, hoat, khung, luoi, mieng, soi, tienhoa, trongso, xuat  # noqa: E402
from quai.hoat import Clip, LoXo, an_hien, chuoi_song, cv, ease, lui, rung, song  # noqa: E402
from quai.khung import Dat  # noqa: E402

INBOX = os.path.join(HERE, "inbox")
HL_MANH = os.path.join(INBOX, "hai_long", "manh")
CODE = "tm07"
TW = 1.6          # chu kỳ băng chuyền sóng (giây); aura dài 2·TW
NC = 4            # đốt mỗi cuộn sóng
NRB = 8           # xương dọc dải nước
B_VIEN, B_TRONG = 11.0, 15.0   # đặt lại theo chiều cao con trong dung1/dung2 (BUOC)
CAO = {2: (905 - 160) * 0.72, 1: (872 - 290) * 0.72}          # chiều cao con (px rig) đọc từ concept
BUOC = {k: (0.015 * h, 0.02 * h) for k, h in CAO.items()}    # bước viền 1,5 %, bước trong 2 % chiều cao (Claude điều phối)


def d_inbox(k):
    return os.path.join(INBOX, f"{CODE}_{k}")


# ================================================================ cắt tờ
# ô lưới / hàng đã dặn GPT trong build_tm07.py
GRID = {
    (2, "M01"): [["dau", "ham", "mieng"], ["nga", "mi", "vay_lung"]],
    (1, "M01"): [["dau", "ham", "mieng"], ["nga", "mi", "vay_lung"]],
}
ROWS = {   # (dạng, tờ): [(y0, y1 theo tỉ lệ cao tờ, [tên theo x trái → phải])]
    (2, "M02"): [(0.0, 0.36, ["than"]), (0.36, 0.66, ["cuong", "vay_duoi"]), (0.66, 1.0, ["vay_cheo", "canh_a", "canh_b", "canh_c"])],
    (2, "M03"): [(0.0, 0.5, ["sen_sau"]), (0.5, 1.0, ["sen_truoc", "dai", None, "phun_lo", None])],
    (1, "M02"): [(0.0, 0.5, ["than"]), (0.5, 0.72, ["cuong", "vay_duoi", "vay_cheo"]),
                 (0.72, 1.0, ["de_nu", "nu_sau", "nu_truoc", "canh_a", "canh_b", "canh_c"])],
}
DUC = {"dau": "tam", "mi": None}


def gan_hang(to, hang):
    """gán tên theo hàng (y) rồi theo x trái → phải; in mảnh thừa."""
    out, thua = {}, []
    for y0, y1, names in hang:
        ms = [m for m in to.manh if y0 * to.h <= (m["y0"] + m["y1"]) / 2 < y1 * to.h]
        ms.sort(key=lambda m: (m["x0"] + m["x1"]) / 2)
        for nm, m in zip(names, ms):
            if nm:
                out[nm] = m
        thua += ms[len(names):]
        if len(ms) < len(names):
            print(f"  hàng {y0:.2f}-{y1:.2f}: thiếu {names[len(ms):]}")
    if thua:
        print(f"  {os.path.basename(to.path)}: {len(thua)} mảnh thừa: " + ", ".join(f"({m['x0']},{m['y0']}) {m['x1'] - m['x0']}x{m['y1'] - m['y0']}" for m in thua[:8]))
    return out


def cat(k):
    tai, manh_dir = os.path.join(d_inbox(k), "tai_ve"), os.path.join(d_inbox(k), "manh")
    names = []
    for sc in ("M01", "M02", "M03"):
        p = anh.to_moi_nhat(tai, sc)
        if not p:
            print(f"  (chưa có tờ {sc})")
            continue
        to = anh.doc_to(p)
        if (k, sc) in GRID:
            got = anh.gan_theo_o(to, GRID[(k, sc)])
        else:
            got = gan_hang(to, ROWS[(k, sc)])
        duc = {n: v for n, v in DUC.items() if n in got and v}
        anh.luu_manh(to, got, manh_dir, duc=duc)
        names += list(got)
    anh.to_soi(manh_dir, names)
    print("  soi:", os.path.join(manh_dir, "_soi.png"))


# ================================================================ mảnh và chỗ đặt
# cỡ trên tờ GPT (giữ chỗ) và tỉ lệ co riêng (cỡ trong concept / cỡ trên tờ); đơn vị rig = concept px × SC
SC = {2: 0.72, 1: 0.72}   # cùng tỉ lệ để ảnh nước hai dạng trùng nhau trong atlas rig gộp
IND, IVO, CRI, ROSE, GOLD, PERI, CREAM, WINE = ((58, 74, 156), (244, 236, 216), (217, 68, 58), (238, 138, 128), (232, 182, 74),
                                                (143, 167, 230), (247, 240, 223), (139, 47, 69))
GIU_CHO = {
    2: {"dau": ("bo", 440, 300, IND), "ham": ("ham", 340, 120, IVO), "mieng": ("mieng", 240, 170, WINE), "nga": ("dai", 470, 72, GOLD),
        "mi": ("mi", 150, 95, IND), "vay_lung": ("giot", 300, 330, IND), "than": ("dai", 1100, 400, IND), "cuong": ("dai", 300, 170, IND),
        "vay_duoi": ("giot", 360, 300, IND), "vay_cheo": ("dai", 430, 190, IND), "canh_a": ("giot", 90, 150, CRI),
        "canh_b": ("giot", 70, 115, CRI), "canh_c": ("giot", 50, 85, CRI), "sen_sau": ("bo", 640, 430, CRI), "sen_truoc": ("bo", 560, 300, ROSE),
        "dai": ("tron", 210, 160, GOLD), "phun_lo": ("giot", 170, 200, (140, 208, 246))},
    1: {"dau": ("tron", 440, 400, PERI), "ham": ("ham", 260, 110, CREAM), "mieng": ("mieng", 200, 150, WINE), "nga": ("dai", 200, 90, (241, 210, 122)),
        "mi": ("mi", 190, 150, PERI), "vay_lung": ("giot", 180, 200, PERI), "than": ("tron", 800, 500, PERI), "cuong": ("dai", 300, 110, PERI),
        "vay_duoi": ("giot", 240, 190, PERI), "vay_cheo": ("dai", 260, 120, PERI), "de_nu": ("bo", 170, 80, IND), "nu_sau": ("giot", 230, 330, (243, 181, 174)),
        "nu_truoc": ("giot", 190, 260, (243, 181, 174)), "canh_a": ("giot", 70, 120, (243, 181, 174)), "canh_b": ("giot", 55, 95, (243, 181, 174)),
        "canh_c": ("giot", 40, 70, (243, 181, 174))},
}
# tỉ lệ co riêng từng mảnh = cỡ trong concept / cỡ vẽ trên tờ (chỉnh sau khi xem tờ thật)
TI = {
    2: {"dau": 0.70, "ham": 0.55, "mieng": 0.5, "nga": 0.62, "mi": 0.70, "vay_lung": 0.62, "than": 0.73, "cuong": 0.5, "vay_duoi": 1.0,
        "vay_cheo": 0.68, "canh_a": 0.6, "canh_b": 0.6, "canh_c": 0.6, "sen_sau": 0.56, "sen_truoc": 0.54, "dai": 0.52, "phun_lo": 0.5},
    1: {"dau": 0.62, "ham": 0.55, "mieng": 0.5, "nga": 0.55, "mi": 0.62, "vay_lung": 0.6, "than": 0.84, "cuong": 0.5, "vay_duoi": 0.9,
        "vay_cheo": 0.6, "de_nu": 0.6, "nu_sau": 0.56, "nu_truoc": 0.56, "canh_a": 0.6, "canh_b": 0.6, "canh_c": 0.6},
}
TI[1]["than"] = 1.0   # thân bé: 717 px tờ -> ~720 px concept (lưng đỡ nụ ở y≈330, bụng 780)
# điểm trên ảnh mảnh (tỉ lệ ảnh, y xuống): bản lề hàm, chóp mõm (khép), gốc ngà, lỗ thở, hạt mắt, neo hàm (knob), neo gáy
PT = {
    2: {"hinge": (0.52, 0.84), "snout": (0.985, 0.76), "tusk": (0.70, 0.20), "blow": (0.50, 0.12), "eye": (0.63, 0.52),
        "jaw_knob": (0.10, 0.36), "jaw_tip": (0.93, 0.14), "jaw_scale": 1.0, "neck": (0.03, 0.55), "lid_tranh": None},
    1: {"hinge": (0.84, 0.77), "snout": (0.985, 0.73), "tusk": (0.74, 0.14), "blow": (0.5, 0.04), "eye": (0.74, 0.53),
        "jaw_knob": (0.06, 0.32), "jaw_tip": (0.92, 0.12), "jaw_scale": 1.6, "neck": (0.03, 0.6), "lid_tranh": None},
}
# nước: mảnh Hải Long (tỉ lệ co riêng so với tờ Hải Long)
NUOC_TI = {"band": 0.86, "wave_a": 0.62, "wave_c": 0.62, "wave_d": 0.72, "wave_e": 0.8, "curl_s1": 0.78, "curl_s2": 0.68,
           "curl_s3": 0.8, "foam": 0.62, "drop_a": 0.4, "drop_b": 0.42}
SPINES = {
    "wave_a": [(0.25, 0.97), (0.14, 0.62), (0.25, 0.30), (0.50, 0.12), (0.80, 0.18), (0.88, 0.38), (0.76, 0.52)],
    "wave_c": [(0.15, 0.92), (0.06, 0.60), (0.20, 0.28), (0.42, 0.12), (0.62, 0.22), (0.62, 0.42)],
    "wave_d": [(0.30, 0.95), (0.10, 0.65), (0.20, 0.32), (0.48, 0.10), (0.82, 0.16), (0.95, 0.36), (0.80, 0.52)],
    "wave_e": [(0.08, 0.85), (0.30, 0.60), (0.55, 0.52), (0.75, 0.30), (0.90, 0.25), (0.90, 0.45)],
    "curl_s1": [(0.35, 0.97), (0.10, 0.60), (0.25, 0.22), (0.60, 0.10), (0.90, 0.30), (0.80, 0.55)],
    "curl_s2": [(0.35, 0.97), (0.06, 0.60), (0.22, 0.22), (0.60, 0.08), (0.92, 0.28), (0.75, 0.52)],
    "curl_s3": [(0.35, 0.97), (0.08, 0.60), (0.25, 0.25), (0.60, 0.10), (0.90, 0.30), (0.75, 0.55)],
    "foam": [(0.5, 0.95), (0.5, 0.7), (0.5, 0.45), (0.5, 0.2)],
}
# cuộn sóng từng dạng: mảnh, lớp (back: sau thân; front: trước), x, y chân sóng (rig), cỡ, pha, lật; kc độ cuộn, rise độ dâng
WAVES = {
    2: [dict(p="wave_c", lane="back", x=-470, y=40, s=0.95, ph=0.00, flip=False),
        dict(p="wave_a", lane="back", x=430, y=30, s=0.80, ph=0.50, flip=True),
        dict(p="curl_s2", lane="back", x=-120, y=44, s=0.75, ph=0.25, flip=True),
        dict(p="curl_s1", lane="front", x=-430, y=10, s=0.95, ph=0.70, flip=False),
        dict(p="wave_d", lane="front", x=-240, y=6, s=0.85, ph=0.10, flip=True),
        dict(p="foam", lane="front", x=-40, y=12, s=0.6, ph=0.85, flip=False, kc=0.0, rise=0.3),
        dict(p="curl_s3", lane="front", x=170, y=8, s=0.9, ph=0.40, flip=True),
        dict(p="curl_s1", lane="front", x=440, y=12, s=0.8, ph=0.20, flip=True)],
    1: [dict(p="wave_e", lane="back", x=-150, y=18, s=0.9, ph=0.0, flip=False, kc=0.6, rise=0.5),
        dict(p="curl_s2", lane="front", x=-250, y=8, s=0.62, ph=0.3, flip=False),
        dict(p="foam", lane="front", x=-60, y=10, s=0.5, ph=0.8, flip=False, kc=0.0, rise=0.3),
        dict(p="curl_s3", lane="front", x=150, y=6, s=0.72, ph=0.55, flip=True)],
}
WY = {2: 34, 1: 26}      # mặt nước (mép dưới mặt nạ cắt)
NAP_ONG = {2: {"than": (0.05, 0.05), "cuong": (0.0, 0.09)}, 1: {"cuong": (0.0, 0.09)}}   # đoạn cắt ở đầu trái, phải
SC_GOP = 0.38  # tỉ lệ ảnh dạng 2 khi gộp vào rig dạng 1 (chỉ hiện ở evolve; rig riêng dạng 2 vẫn SC 0,72)
TOL_KHOA = {"rotate": 0.4, "translate": 0.8, "scale": 0.005, "alpha": 0.02}   # lược khoá RDP mạnh hơn mặc định (nhiều cuộn sóng)
DAY_THAN = {2: 360, 1: 0}     # bề dày thân ở gáy theo concept (px concept); 0 = giữ như vẽ
DAY_CUONG = {2: 130, 1: 110}  # bề dày cuống đuôi ở gốc
BAND = {2: ("band", 0.86, 0.75, 0, 0), 1: ("band", 0.5, 0.5, 0, -4)}   # dải nước trước: mảnh, tỉ lệ ngang, dọc, dx, dy


def cat_nap(im, trai=0.035, phai=0.035):
    """GPT vẽ hai đầu ống thành đĩa cắt màu ngà: xoá một đoạn ở hai đầu (tỉ lệ bề dài) để chỗ nối ống nấp dưới mảnh kề."""
    a = np.asarray(im.convert("RGBA")).copy()
    w = a.shape[1]
    a[:, : int(w * trai), 3] = 0
    a[:, w - int(w * phai):, 3] = 0
    return Image.fromarray(a, "RGBA")


def mat_cyan(im):
    """mặt nạ con mắt: cụm cyan (mống) + vùng tối bên trong, bao lồi, nới 4 px."""
    a = np.asarray(im.convert("RGBA")).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    cy = (g > 180) & (b > 185) & (r < 130) & (al > 128)   # cyan mống mắt (69,207,224); da lam phấn (143,167,230) không lọt
    lab, cs = anh.thanh_phan(cy)
    if not cs:
        return None
    big = max(cs, key=lambda c: c["dt"])
    ys, xs = np.nonzero(lab == big["i"])
    hull = anh.bao_loi(list(zip(xs.tolist(), ys.tolist())))
    m = anh.to_da_giac(cy.shape, hull)
    return anh.gian(m, 4)


def doc_khop(k):
    """khop.json của tm07_khop.py: {tên: s, r, cx, cy} (concept px); thiếu thì {}. Các lớp sen/nụ canh thẳng hàng theo tâm x của
    đài (hoa đối xứng; khớp từng lớp cùng màu chồng nhau dễ lệch ngang)."""
    p = os.path.join(d_inbox(k), "khop.json")
    kq = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    goc = "dai" if "dai" in kq else ("de_nu" if "de_nu" in kq else None)
    if goc:
        # chân các lớp cánh đặt ở chân hoa (đài sen cao hơn chân hoa ~150 px concept; đế nụ thấp hơn tâm đế 10 px)
        base_y = kq[goc]["cy"] + (150 if goc == "dai" else 10)
        for nm in ("sen_sau", "sen_truoc", "nu_sau", "nu_truoc"):
            pth = os.path.join(d_inbox(k), "manh", nm + ".png")
            if nm in kq and os.path.exists(pth):
                hgt = Image.open(pth).height * kq[nm]["s"]
                kq[nm]["cx"] = kq[goc]["cx"] + (4 if nm.endswith("truoc") else 0)
                kq[nm]["cy"] = base_y - 0.5 * hgt + (6 if nm.endswith("truoc") else 0)
    return kq


def nap(k, sc=None):
    sc = sc or SC[k]
    kq = doc_khop(k)
    ti = dict(TI[k])
    for nm, q in kq.items():   # dải uốn theo đường cong (than, cuong) lấy tỉ lệ từ độ dài đường, không theo khớp
        if nm in ti and nm not in ("than", "cuong", "ham") and os.path.exists(os.path.join(d_inbox(k), "manh", nm + ".png")):
            ti[nm] = q["s"]
    if kq:
        print("  tỉ lệ theo khớp:", ", ".join(f"{n} {ti[n]:.3f}" for n in kq if n in ti))
    pc = anh.nap_manh(os.path.join(d_inbox(k), "manh"), GIU_CHO[k], ti_le=sc, ti_le_rieng=ti)
    for nm, (tr, ph) in NAP_ONG.get(k, {}).items():
        if os.path.exists(os.path.join(d_inbox(k), "manh", nm + ".png")):
            pc[nm] = anh.loang_mau(cat_nap(pc[nm], tr, ph))
    # ảnh nước luôn ở tỉ lệ SC[1] (= SC[2]) để hai dạng và bản gộp dùng chung một vùng atlas; bản co (sc khác) bù bằng tỉ lệ xương
    nuoc = anh.nap_manh(HL_MANH, {n: ("tron", 200, 200, (58, 150, 226)) for n in NUOC_TI}, ti_le=SC[1], ti_le_rieng=NUOC_TI)
    return pc, nuoc


# ================================================================ dải thẳng uốn theo đường cong
def duong(pts):
    """đường gấp khúc (rig) -> (dài, f(s) -> (điểm, tiếp tuyến đơn vị)), s kẹp trong [0, dài]; làm mượt bằng lấy mẫu dày."""
    P = np.asarray(pts, float)
    # làm mượt Catmull-Rom cho đường cong không gãy ở khớp
    dense = []
    for i in range(len(P) - 1):
        p0, p1, p2, p3 = P[max(0, i - 1)], P[i], P[i + 1], P[min(len(P) - 1, i + 2)]
        for u in np.linspace(0, 1, 24, endpoint=(i == len(P) - 2)):
            u2, u3 = u * u, u * u * u
            dense.append(0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u3))
    D = np.asarray(dense)
    seg = np.hypot(*np.diff(D, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    tg = np.gradient(D, axis=0)
    tg /= np.maximum(1e-9, np.hypot(*tg.T))[:, None]

    def f(s):
        s = float(np.clip(s, 0, cum[-1]))
        p = np.array([np.interp(s, cum, D[:, 0]), np.interp(s, cum, D[:, 1])])
        t = np.array([np.interp(s, cum, tg[:, 0]), np.interp(s, cum, tg[:, 1])])
        return p, t / max(1e-9, np.hypot(*t))
    return float(cum[-1]), f


def day_dai(L, u0=0.8, u1=0.95):
    """bề dày (px ảnh) của dải ở đoạn u0..u1 dọc trục (để co dày về đúng concept khi GPT vẽ ống quá mảnh)."""
    Lt = L.truc[1][-1]
    m = (L.s >= u0 * Lt) & (L.s <= u1 * Lt)
    ys = L.pts[m][:, 1]
    return float(ys.max() - ys.min()) if m.any() else float(L.h)


def uon_dai(L, w, h, f, kx, ky, s0=0.0):
    """đỉnh dải lưới L (ảnh w×h, trục ngang giữa, gốc trái) -> thế giới: điểm trục s·kx trên đường f, lệch ngang (yc - y)·ky
    theo pháp tuyến trái của tiếp tuyến."""
    D, cum = L.truc
    yc = float(np.mean(D[:, 1]))
    V = []
    for (x, y), s in zip(L.pts, L.s):
        p, t = f(s0 + s * kx)
        n = np.array([-t[1], t[0]])
        V.append(p + n * ((yc - y) * ky))
    return np.asarray(V)


def khop_cong(f, s_list):
    return np.asarray([f(s)[0] for s in s_list])


# ================================================================ nước (sóng Hải Long dùng lại)
def them_nuoc(sk, nuoc, k, truoc_than, sau_than, thua=False, he=1.0):
    """xương nuoc > song > cuộn sóng (2 bản sao lệch nửa chu kỳ), dải nước trước, giọt. truoc_than(): gọi để thêm slot thân vào
    giữa (lớp back vẽ trước, mặt nạ cắt, thân, rồi lớp front). Trả info nước cho aura."""
    info = {"waves": [], "band": None, "drops": []}
    for n, im in nuoc.items():
        sk.anh("n_" + n if False else n, im)
    sk.xuong("nuoc", "root")
    sk.xuong("song", "nuoc")

    def wave_inst(i, cfg, copy):
        nm = f"w{i}{'ab'[copy]}"
        im = nuoc[cfg["p"]]
        w, h = im.size
        sp = np.array(SPINES[cfg["p"]], float) * (w, h)
        loc = np.stack([sp[:, 0] - sp[0, 0], h - sp[:, 1]], axis=1)      # hệ gốc sóng: chân sống lưng, y lên
        dl = np.hypot(*np.diff(loc, axis=0).T)
        cum = np.concatenate([[0], np.cumsum(dl)])
        tt = np.linspace(0, cum[-1], 81)
        dense = np.stack([np.interp(tt, cum, loc[:, 0]), np.interp(tt, cum, loc[:, 1])], axis=1)
        J = dense[:: 80 // NC]
        sk.xuong(nm, "song", cfg["x"] * he, cfg["y"] * he, 0, 0, (-1 if cfg["flip"] else 1) * cfg["s"] * he, cfg["s"] * he)
        Wb = sk.W0[nm]
        Jw = np.array([(Wb @ np.array([p[0], p[1], 1.0]))[:2] for p in J])
        cn = sk.chuoi(nm + "_", nm, Jw)
        ang = [math.degrees(math.atan2(J[q + 1][1] - J[q][1], J[q + 1][0] - J[q][0])) for q in range(NC)]
        turn = sum(((ang[q + 1] - ang[q] + 180) % 360) - 180 for q in range(NC - 1))
        sense = 1.0 if turn >= 0 else -1.0
        sk.slot(nm, nm, cfg["p"])
        L = luoi.luoi_vung(im, *((18.0, 24.0) if thua else (12.0, 16.0)), vien=(5 if thua else 4), ten=nm, in_tk=False)
        if L.ho:
            print(f"  sóng {nm}: hở {L.ho} px")
        size = max(w, h)
        Wt, V = [], []
        for (px, py) in L.pts:
            X, Y = px - sp[0, 0], h - py
            d2 = (dense[:, 0] - X) ** 2 + (dense[:, 1] - Y) ** 2
            q = int(np.argmin(d2))
            near = math.exp(-(math.sqrt(d2[q]) / (0.30 * size)) ** 2)
            fpos = q / 80 * NC
            d = {b: wv * near for b, wv in trongso.chuoi_f([fpos], cn)[0].items()}
            d[nm] = d.get(nm, 0.0) + 1 - near
            Wt.append(d)
            V.append((Wb @ np.array([X, Y, 1.0]))[:2])
        sk.luoi_gan(nm, cfg["p"], L, trongso.chuan(Wt), the_gioi=np.asarray(V))
        info["waves"].append(dict(cfg, bone=nm, chain=cn, ph=(cfg["ph"] + 0.5 * copy) % 1.0, sense=sense, h=h))

    for i, cfg in enumerate(WAVES[k]):
        if cfg["lane"] == "back" and not thua:    # bản gộp (chỉ hiện ở evolve): bỏ lớp sóng sau cho nhẹ
            for copy in (0, 1):
                wave_inst(i, cfg, copy)
    sau_than()
    # mặt nạ cắt: thân dưới mặt nước bị che
    sk.xuong("goc_cat", "root")      # slot mặt nạ không đặt trên root: tienhoa.gop đổi tên root của dạng sau thành evo
    sk.slot("cat", "goc_cat")
    end = truoc_than()
    sk.cat("cat", end, [(-1400, WY[k] * he), (1400, WY[k] * he), (1400, 2400), (-1400, 2400)])
    # dải nước trước
    bn, sx, sy, dx, dy = BAND[k]
    dx, dy = dx * he, dy * he
    im = nuoc[bn]
    w, h = im.size
    sk.xuong("dai_nuoc", "nuoc", dx, dy)
    Lb = luoi.luoi_dai(im, NRB, cot_moi_dot=3, buoc=(30 if thua else 16), vien=(3 if thua else 2), ten="dai_nuoc", in_tk=False)
    dat = Dat(dx, dy, neo=(0.5, 1.0), ti=(sx * he, sy * he))
    J = dat.ra(Lb.khop(NRB), w, h)
    rn = [f"dn{i}" for i in range(NRB)]
    for i in range(NRB):
        sk.xuong(rn[i], "dai_nuoc", *J[i], the_gioi=True)
    Wc = trongso.chuoi(Lb.s, Lb.truc[1][-1] / NRB, rn)
    Wt = []
    for d, (px, py) in zip(Wc, Lb.pts):
        kk = (1.0 - py / h) ** 1.6
        e = {b: wv * kk for b, wv in d.items()}
        e["dai_nuoc"] = e.get("dai_nuoc", 0.0) + 1 - kk
        Wt.append(e)
    sk.slot("dai_nuoc", "dai_nuoc", bn)
    sk.luoi_gan("dai_nuoc", bn, Lb, trongso.chuan(Wt), dat=dat)
    info["band"] = rn
    for i, cfg in enumerate(WAVES[k]):
        if cfg["lane"] == "front":
            for copy in (0, 1):
                wave_inst(i, cfg, copy)
    for i, (nmd, x, y) in enumerate((("drop_a", -380, 40), ("drop_b", 300, 46), ("drop_b", -120, 50), ("drop_a", 460, 36))):
        x, y = x * he, y * he
        b = f"giot{i}"
        sk.xuong(b, "nuoc", x, y)
        sk.slot(b, b, nmd, an=True)
        sk.manh(b, nmd, Dat(x, y, neo=(0.5, 0.9), ti=he), ten=f"giot{i}", xuong=b)
        info["drops"].append((b, i))
    return info


def aura_nuoc(info, t, P):
    """một khung của clip aura: đời từng cuộn sóng (dâng tại chỗ, mào cuộn, trôi nhẹ, mờ vào ra), dải nước nhấp nhô, giọt."""
    US = (0.0, 0.16, 0.5, 0.8, 0.96, 0.999)
    CURL = (-0.55, -0.30, 0.25, 0.60, 0.95, 1.0)
    AJ = (8.0, 18.0, 26.0, 20.0)
    for wv in info["waves"]:
        u = ((t / TW) - wv["ph"]) % 1.0
        cu = float(np.interp(u, US, CURL))
        g = 0.6 + 0.4 * ease(u / 0.45, "out")
        kc, rise, dx = wv.get("kc", 1.0), wv.get("rise", 1.0), wv.get("dx", 46.0)
        hh, s_ = wv["h"], wv["s"]
        P.move(wv["bone"], (-1 if wv["flip"] else 1) * dx * (u - 0.3),
               -0.24 * hh * s_ * rise * (1 - ease(u / 0.5, "out")) + 0.03 * hh * s_ * u)
        P.scale(wv["bone"], g, g)
        P.alpha[wv["bone"]] = ease(u / 0.16, "io") * (1 - ease((u - 0.8) / 0.16, "io")) * wv.get("a", 1.0)
        for q, b in enumerate(wv["chain"]):
            P.rot(b, wv["sense"] * AJ[q] * cu * kc)
    if info["band"]:
        for i, b in enumerate(info["band"]):
            P.move(b, 0, 7.0 * math.sin(2 * math.pi * t / TW + i * 0.8))
            P.rot(b, 3.0 * math.cos(2 * math.pi * t / TW + i * 0.8))
    for b, i in info["drops"]:
        u = ((t / TW) - 0.23 * i) % 1.0
        hgt = 90 * math.sin(math.pi * min(1, u / 0.55))
        P.move(b, 12 * u, hgt if u < 0.55 else 0)
        P.alpha[b] = 1.0 if 0.03 < u < 0.52 else 0.0


def song0(t, chu_ky, pha=0.0):
    """sin có trừ giá trị tại t = 0: dao động idle bằng 0 ở khung 0 (khung 0 idle trùng dáng gốc, bóng dáng = concept)."""
    return song(t, chu_ky, pha) - song(0.0, chu_ky, pha)


def song_than(P, ten, t, chu_ky, bien_do, tre=0.17, ngon_dan=False):
    """như hoat.chuoi_song nhưng trừ bias tại t = 0 từng đốt (khung 0 = dáng gốc)."""
    n = len(ten)
    amp = np.broadcast_to(np.asarray(bien_do, float), (n,))
    for i, b in enumerate(ten):
        kk = (n - 1 - i) if ngon_dan else i
        f = lambda tt: math.sin(2 * math.pi * (tt - kk * tre) / chu_ky)  # noqa: E731
        P.rot(b, amp[i] * (f(t) - f(0.0)))


# ================================================================ dạng 2: Liên Kình
def dung2(pc, nuoc, nuoc_thua=False, luoi_thua=1.0, sc=None):
    global B_VIEN, B_TRONG
    k = 2
    S = sc or SC[k]
    he = S / SC[k]            # bản co nhỏ (trong rig gộp của dạng 1): mọi toạ độ rig tuyệt đối nhân he
    B_VIEN, B_TRONG = BUOC[k][0] * luoi_thua * he, BUOC[k][1] * luoi_thua * he
    bv_sen, bt_sen = BUOC[k][0] * he, BUOC[k][1] * he   # cánh sen chóp nhọn, mảnh nhỏ: không thưa (bản gộp từng hở 1 px ở chóp)
    print(f"  bước lưới dạng {k}: viền {B_VIEN:.1f}, trong {B_TRONG:.1f} px (cao {CAO[k] * he:.0f})")
    O = (770.0, 905.0)   # gốc rig trên concept 1536x1024

    def R(x, y):
        return ((x - O[0]) * S, (O[1] - y) * S)
    sk = khung.Sk(f"{CODE}_2")
    for n, im in pc.items():
        sk.anh(n, im)
    sk.xuong("root")
    sk.xuong("move", "root")
    info = {"pc": pc}
    KQ = doc_khop(k)

    def DK(nm, mac_dinh):
        """Dat theo khớp tự động (tâm mảnh, góc) nếu có, không thì mặc định."""
        if nm in KQ and os.path.exists(os.path.join(d_inbox(k), "manh", nm + ".png")):
            q = KQ[nm]
            return Dat(*R(q["cx"], q["cy"]), goc=q["r"], neo=(0.5, 0.5))
        return mac_dinh
    info["KQ"] = KQ

    # ---- đầu đặt trước (theo khớp) để biết gáy; sống lưng: đường cong qua concept tới gáy, 6 đốt (4 sau, 2 trước ngực)
    imh = pc["dau"]
    wh, hh = imh.size
    dat_dau = DK("dau", Dat(*R(1190, 420), goc=14, neo=(0.5, 0.5)))
    neck_w = dat_dau.mot((PT[k]["neck"][0] * wh, PT[k]["neck"][1] * hh), wh, hh)
    goc_dau = dat_dau.goc
    spine_img = [(330, 582), (460, 612), (600, 623), (740, 613), (880, 588), (1010, 552)]
    Ltot, f = duong([R(*p) for p in spine_img] + [tuple(neck_w)])
    im = pc["than"]
    w, h = im.size
    Lt = luoi.luoi_dai(im, 6, cot_moi_dot=3, buoc=B_TRONG, ten="than")
    kx = Ltot / Lt.truc[1][-1]
    ky = max(kx, DAY_THAN[k] * S / day_dai(Lt))   # bề dày gáy đúng concept (GPT hay vẽ ống dài mảnh)
    print(f"  thân: kx {kx:.3f}, ky {ky:.3f} (dày vẽ {day_dai(Lt):.0f} px -> đích {DAY_THAN[k] * S:.0f})")
    Vt = uon_dai(Lt, w, h, f, kx, ky)
    sJ = np.linspace(0, Ltot, 7)
    J = khop_cong(f, sJ)
    sk.xuong("than", "move", *J[4], goc=math.degrees(math.atan2(*(J[5] - J[4])[::-1])), dai=60, the_gioi=True)
    bk = sk.chuoi("bk", "than", [J[4], J[3], J[2], J[1], J[0]])          # bk0..bk3: ngực → gốc đuôi
    fw = sk.chuoi("fw", "than", [J[4], J[5], J[6]])                      # fw0, fw1: ngực → gáy
    body_names = ["bk3", "bk2", "bk1", "bk0", "fw0", "fw1"]
    info.update(bk=bk, fw=fw)

    # ---- đuôi: vây đuôi theo khớp, cuống (3 đốt) theo đường cong từ gốc đuôi tới chân vây
    imv = pc["vay_duoi"]
    dat_vd = DK("vay_duoi", Dat(*R(215, 395), goc=8, neo=(0.5, 0.5)))
    vd_root = dat_vd.mot((0.5 * imv.width, 0.96 * imv.height), *imv.size)
    Lc, fc = duong([R(332, 582), R(292, 548), tuple(vd_root)])
    imc = pc["cuong"]
    wc, hc = imc.size
    Ld = luoi.luoi_dai(imc, 3, cot_moi_dot=3, buoc=B_TRONG * 0.85, ten="cuong")
    # ảnh cuống: gốc (to) bên phải, ngọn bên trái -> lật: s đo từ gốc = trái ảnh? GPT vẽ to bên PHẢI: lấy s' = dài - s
    kc_ = Lc / Ld.truc[1][-1]
    kcy = max(kc_, DAY_CUONG[k] * S / day_dai(Ld, 0.75, 0.95))
    Lmirror = Ld.truc[1][-1]
    Vd = []
    Dd, _ = Ld.truc
    yc = float(np.mean(Dd[:, 1]))
    for (x, y), s in zip(Ld.pts, Ld.s):
        p, t = fc((Lmirror - s) * kc_)
        n = np.array([-t[1], t[0]])
        Vd.append(p - n * ((yc - y) * kcy))   # lật ngang: lệch pháp tuyến đổi dấu
    Vd = np.asarray(Vd)
    Jd = khop_cong(fc, np.linspace(0, Lc, 4))
    du = sk.chuoi("du", "bk3", Jd)
    sk.xuong("vd", "du2", *Jd[3], goc=sk.goc_tg("du2")[2], dai=40, the_gioi=True)
    info["du"] = du

    # ---- đầu, hàm, ngà, lỗ thở
    imj = pc["ham"]
    snout = dat_dau.mot((PT[k]["snout"][0] * wh, PT[k]["snout"][1] * hh), wh, hh)
    hinge = dat_dau.mot((PT[k]["hinge"][0] * wh, PT[k]["hinge"][1] * hh), wh, hh)
    gj = math.degrees(math.atan2(*(snout - hinge)[::-1]))
    # hàm dưới neo ở khoé miệng của đầu; hình hàm GPT vẽ chếch sẵn (knob trái-dưới, răng phải-trên) nên trừ độ chếch đó;
    # tỉ lệ hàm = dài miệng (bản lề → mõm) / dài hàm trong hình (knob → răng trước)
    jk, jt = PT[k]["jaw_knob"], PT[k]["jaw_tip"]
    tilt = math.degrees(math.atan2((jk[1] - jt[1]) * imj.height, (jt[0] - jk[0]) * imj.width))
    dj = math.hypot((jt[0] - jk[0]) * imj.width, (jt[1] - jk[1]) * imj.height)
    tj = float(np.hypot(*(snout - hinge))) * PT[k].get("jaw_scale", 1.0) / max(1e-6, dj)
    dat_ham = Dat(*hinge, goc=gj - tilt, ti=tj, neo=jk)
    print(f"  hàm: chếch sẵn {tilt:.1f}°, góc đặt {gj - tilt:.1f}°, co {tj:.3f}")
    sk.xuong("dau", "fw1", *neck_w, goc=goc_dau, dai=wh * 0.8, the_gioi=True)
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*(snout - hinge))), the_gioi=True)
    mp = hinge + 0.86 * (snout - hinge) + np.array([0, 6])
    sk.xuong("mieng", "dau", *mp, goc=gj + 4, dai=40, the_gioi=True)
    imn = pc["nga"]
    dat_nga = DK("nga", Dat(*dat_dau.mot((PT[k]["tusk"][0] * wh, PT[k]["tusk"][1] * hh), wh, hh), goc=goc_dau + 30, neo=(0.03, 0.5)))
    tr = dat_nga.mot((0.03 * imn.width, 0.5 * imn.height), *imn.size)
    sk.xuong("nga", "dau", *tr, goc=dat_nga.goc, dai=imn.width, the_gioi=True)
    sk.xuong("mui_nga", "nga", imn.width * 0.97, 0, 0, 20)
    bl = dat_dau.mot((PT[k]["blow"][0] * wh, PT[k]["blow"][1] * hh), wh, hh)
    sk.xuong("lo_tho", "dau", *bl, goc=90 + 10, dai=20, the_gioi=True)

    # ---- vây chèo (gần, xa), vây lưng
    imf = pc["vay_cheo"]
    wf, hf = imf.size
    Lf = luoi.luoi_dai(imf, 3, cot_moi_dot=3, buoc=B_TRONG * 0.85, ten="vay_cheo")
    dat_vg = DK("vay_cheo", Dat(*R(905, 600), goc=-58, neo=(0.04, 0.5)))
    vg = sk.chuoi("vg", "fw0", dat_vg.ra(Lf.khop(3), wf, hf))
    dat_vx = Dat(*R(1005, 372), goc=46, ti=0.58, neo=(0.04, 0.5))   # (R đã theo S nên tự co theo he)   # vây xa: ló sau lưng giữa sen và đầu, nhỏ hơn vây gần
    vx = sk.chuoi("vx", "fw0", dat_vx.ra(Lf.khop(3), wf, hf))
    iml = pc["vay_lung"]
    wl, hl = iml.size
    Ll = luoi.luoi_vung(iml, B_VIEN, B_TRONG, ten="vay_lung")
    dat_vl = DK("vay_lung", Dat(*R(560, 405), goc=0, neo=(0.62, 1.0)))
    Jl = dat_vl.ra([(0.62 * wl, hl), (0.44 * wl, 0.5 * hl), (0.26 * wl, 0.04 * hl)], wl, hl)
    vl = sk.chuoi("vl", "bk2", Jl)
    info.update(vg=vg, vx=vx, vl=vl)

    # ---- sen: đài, hàng cánh sau (5 xương), hàng cánh trước (4 xương)
    ims, imt, imd = pc["sen_sau"], pc["sen_truoc"], pc["dai"]
    dat_ss = DK("sen_sau", Dat(*R(770, 486), neo=(0.5, 1.0)))
    dat_st = DK("sen_truoc", Dat(*R(770, 486), neo=(0.5, 1.0)))
    dat_dai = DK("dai", Dat(*(np.array(R(770, 486)) + np.array([0, 0.55 * ims.height])), neo=(0.5, 0.5)))
    sen0 = tuple(dat_ss.mot((0.5 * ims.width, 0.98 * ims.height), *ims.size))
    sk.xuong("sen", "bk0", *sen0, goc=90, dai=30, the_gioi=True)
    cs = [sk.xuong(f"cs{i}", "sen", *sen0, goc=90 + a, dai=ims.height * 0.8, the_gioi=True) for i, a in enumerate((42, 21, 0, -21, -42))]
    ct = [sk.xuong(f"ct{i}", "sen", *sen0, goc=90 + a, dai=imt.height * 0.8, the_gioi=True) for i, a in enumerate((40, 14, -14, -40))]
    info.update(cs=cs, ct=ct)

    # ---- slot (sau → trước), nước ở giữa
    def sau_than():
        sk.slot("vx", vx[0], "vay_cheo")
        sk.slot("vl", vl[0], "vay_lung")
        sk.slot("sen_sau", "sen", "sen_sau")
        sk.slot("dai", "sen", "dai")
        sk.slot("sen_truoc", "sen", "sen_truoc")

    def truoc_than():
        sk.slot("vd", "vd", "vay_duoi")
        sk.slot("than", "than", "than")
        sk.slot("cuong", du[0], "cuong")
        sk.slot("long", "ham", "mieng")
        sk.slot("ham", "ham", "ham")
        sk.slot("nga", "nga", "nga")
        sk.slot("dau", "dau", "dau")
        sk.slot("mi", "dau", "mi", an=True)
        sk.slot("phun_lo", "lo_tho", "phun_lo", an=True)
        sk.slot("vg", vg[0], "vay_cheo")
        for i, nmp in enumerate(("canh_a", "canh_b", "canh_c")):
            sk.xuong(f"cr{i}", "sen", 0, 0)
            sk.slot(f"cr{i}", f"cr{i}", nmp, an=True)
        return "cr2"
    nuoc_info = them_nuoc(sk, nuoc, k, truoc_than, sau_than, thua=nuoc_thua, he=he)
    info["nuoc"] = nuoc_info

    # ---- gắn lưới
    Wt = trongso.chuoi(Lt.s, Lt.truc[1][-1] / 6, body_names)
    trongso.kiem(Wt, "than")
    sk.luoi_gan("than", "than", Lt, Wt, the_gioi=Vt)
    Wd = trongso.chuoi(Lmirror - Ld.s, Lmirror / 3, du, cha="bk3", cha_hoa=0.6)
    sk.luoi_gan("cuong", "cuong", Ld, Wd, the_gioi=Vd)
    imv = pc["vay_duoi"]
    sk.manh("vd", "vay_duoi", dat_vd)
    # đầu: vùng gáy hoà vào fw1
    Lh = luoi.luoi_vung(imh, B_VIEN, B_TRONG, ten="dau")
    Wh = trongso.vung(Lh, [("fw1", [(0, 0.25 * hh), (0.13 * wh, 0.35 * hh), (0.14 * wh, hh), (0, hh)]), ("dau", [(0, 0), (wh, 0), (wh, hh), (0, hh)])],
                      dai_hoa=22 * S)
    Wh = trongso.lam_tron(Lh, Wh, 1)
    trongso.kiem(Wh, "dau", cho_cung=("dau",))
    sk.luoi_gan("dau", "dau", Lh, Wh, dat=dat_dau)
    Lj = luoi.luoi_vung(imj, B_VIEN * 0.8, B_TRONG * 0.8, ten="ham")
    Wj = mieng.ham_hai_xuong(dat_ham.ra(Lj.pts, *imj.size), hinge, snout, "dau", "ham")
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dat_ham)
    mieng.long_mieng(sk, "long", "mieng", "dau", "ham", hinge, snout, duoi=-0.34, tren=(-0.02, -0.04, -0.08, -0.12, -0.16))
    sk.manh("nga", "nga", dat_nga)
    # mí mắt
    that = os.path.exists(os.path.join(d_inbox(k), "manh", "dau.png"))
    if that:
        kq = mieng.fit_lid(imh, pc["mi"], mat=mat_cyan(imh), ten="dạng 2")
        sk.manh("mi", "mi", mieng.dat_mi(dat_dau, imh, kq))
    else:
        sk.manh("mi", "mi", Dat(*dat_dau.mot((PT[k]["eye"][0] * wh, PT[k]["eye"][1] * hh), wh, hh), goc=goc_dau))
    sk.manh("phun_lo", "phun_lo", Dat(*bl, goc=goc_dau, neo=(0.5, 1.0)))
    # vây
    Wf = trongso.chuoi(Lf.s, Lf.truc[1][-1] / 3, vg, cha="fw0", cha_hoa=0.6)
    sk.luoi_gan("vg", "vay_cheo", Lf, Wf, dat=dat_vg)
    Wf2 = trongso.chuoi(Lf.s, Lf.truc[1][-1] / 3, vx, cha="fw0", cha_hoa=0.6)
    sk.luoi_gan("vx", "vay_cheo", Lf, Wf2, dat=dat_vx)
    Wl = trongso.chuoi_chieu(dat_vl.ra(Ll.pts, wl, hl), Jl, vl, cha="bk2", cha_hoa=0.6)
    sk.luoi_gan("vl", "vay_lung", Ll, Wl, dat=dat_vl)
    # sen: mỗi cánh một cột
    for nm_, im_, names in (("sen_sau", ims, cs), ("sen_truoc", imt, ct)):
        ww, hh_ = im_.size
        Lp = luoi.luoi_vung(im_, bv_sen, bt_sen, vien=(2 if he == 1 else 3), ten=nm_)   # chóp cánh sen: bản co nới viền 3 px
        n = len(names)
        regs = [(b, [(i * ww / n, 0), ((i + 1) * ww / n, 0), ((i + 1) * ww / n, hh_), (i * ww / n, hh_)]) for i, b in enumerate(names)]
        Wp = trongso.vung(Lp, regs, dai_hoa=16 * S)
        # chân cánh (hàng dưới) hoà về xương sen cho gốc hoa đứng yên
        for d, (px, py) in zip(Wp, Lp.pts):
            kk = max(0.0, 1 - (hh_ - py) / (0.22 * hh_))
            if kk > 0:
                for b in list(d):
                    d[b] *= 1 - kk
                d["sen"] = d.get("sen", 0.0) + kk
        Wp = trongso.lam_tron(Lp, trongso.chuan(Wp), 1)
        sk.luoi_gan(nm_, nm_, Lp, Wp, dat=(dat_ss if nm_ == "sen_sau" else dat_st))
    sk.manh("dai", "dai", dat_dai)
    for i, nmp in enumerate(("canh_a", "canh_b", "canh_c")):
        sk.manh(f"cr{i}", nmp, Dat(*sen0, neo=(0.5, 0.5)))
    for e, m in (("trung", "ngà đâm trúng (VFX lưỡi nước liềm từ mui_nga)"), ("phun", "bắt đầu phun Thủy Pháo (VFX bám xương mieng)"),
                 ("het_phun", "hết phun"), ("gam", "chiêu cuối: gầm, sen xoè"), ("song", "đuôi quật xuống nước: VFX sóng sen dâng"),
                 ("het_gam", "hết chiêu cuối")):
        sk.su_kien(e, m)
    return sk, info


def clips2(sk, info):
    bk, du, fw = info["bk"], info["du"], info["fw"]
    vg, vx, vl, cs, ct = info["vg"], info["vx"], info["vl"], info["cs"], info["ct"]
    nuoc = info["nuoc"]
    chain = bk + du          # ngực → chóp đuôi
    amp = np.array([1.2, 1.9, 2.6, 3.4, 5.5, 7.5, 9.5, 11.0])[:len(chain)]
    mem = [LoXo(du, k=[420, 330, 250], damp=0.6, maxang=14), LoXo(vg, k=[380, 300, 230], damp=0.6, maxang=10),
           LoXo(vx, k=[380, 300, 230], damp=0.6, maxang=10), LoXo(vl, k=[400, 300], damp=0.6, maxang=8)]

    def nen(P, tt, a=1.0):
        """nền idle: thân uốn sóng gốc dẫn ra đuôi, đầu bù, sen rung lệch pha, vây chèo khua, lỗ thở nhấp."""
        song_than(P, chain, tt, 3.2, amp * a, tre=0.09, ngon_dan=False)
        P.rot("fw0", 1.2 * a * song0(tt, 3.2, 0.6))
        P.rot("dau", (-1.6 * song0(tt, 3.2, 0.6) + 1.0 * song0(tt, 3.2, 2.0)) * a)
        P.move("than", 0, 5.0 * a * song0(tt, 3.2, 1.0))
        for i, b in enumerate(cs):
            P.rot(b, 2.2 * a * song0(tt, 3.2, 0.9 * i))
        for i, b in enumerate(ct):
            P.rot(b, 1.8 * a * song0(tt, 3.2, 0.7 * i + 1.5))
        P.rot("vg0", 5.0 * a * song0(tt, 3.2, 0.4))
        P.rot("vx0", -4.0 * a * song0(tt, 3.2, 1.9))
        P.rot("vl0", 1.5 * a * song0(tt, 3.2, 2.5))

    def phun_lo(P, t, t0, D=0.5):
        u = (t - t0) / D
        if 0 <= u < 1:
            P.alpha["phun_lo"] = 1.0 if u < 0.85 else 1 - (u - 0.85) / 0.15
            g = cv(u, [(0, 0.2), (0.25, 1.1, "out"), (0.5, 1.0), (1, 0.75)])
            P.scale("lo_tho", 0.8 + 0.4 * g, g)

    def idle_fn(t, P, D=3.2):
        nen(P, t)
        P.rot("ham", -cv(t, [(0, 0), (2.0, 0), (2.1, 9, "out"), (2.2, 3), (2.3, 7, "out"), (2.5, 0, "io"), (D, 0)]))   # táp miệng
        an_hien(P, "mi", t, [(0.95, 1.07), (1.17, 1.27)])                                                             # chớp đôi
        phun_lo(P, t, 2.05)

    def appear_fn(t, P, D=1.6):
        nen(P, lui(t, D), ease((t - 0.6) / 0.6))
        up = cv(t, [(0, -520), (0.75, 40, "out"), (0.95, -12, "io"), (1.15, 0, "io"), (D, 0)])
        P.move("than", 0, up)
        g = cv(t, [(0, 0.05), (0.4, 1.0, "out"), (D, 1)])
        P.scale("nuoc", g, max(0.05, g))
        a = cv(t, [(0, 0), (0.1, 1)])
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a
        P.rot("dau", cv(t, [(0, -18), (0.75, 10, "out"), (1.05, 0, "io"), (D, 0)]))
        P.rot("ham", -cv(t, [(0, 0), (0.7, 0), (0.85, 26, "out"), (1.15, 0, "io"), (D, 0)]))
        phun_lo(P, t, 0.8, 0.55)
        for i, b in enumerate(cs):
            P.rot(b, (28 - 14 * i) * (1 - ease((t - 0.5) / 0.6)) * (1 if i < 2 else -1 if i > 2 else 0))

    def attack_fn(t, P, D=1.0, H=0.46):
        """Ngà Thương: cổ rụt lấy đà ngược, đầu + ngà đâm tới 1 khung (giãn ngà), giữ có trôi, về."""
        nen(P, lui(t, D), 1 - 0.7 * hoat.bao(t, 0.1, 0.9, 0.2, 0.25))
        pull = cv(t, [(0, 0), (0.3, 1, "io"), (0.38, 1.08), (H, -1.0, "in"), (H + 0.05, -1.2), (0.7, -1.0, "io"), (D, 0, "io")])
        # lấy đà: cổ rụt, ngà ngẩng lên ra sau (pull > 0); đâm: cổ vươn, ngà chúi xuống tới (pull < 0), chạm đúng khung trung
        P.rot("fw0", 4 * pull)
        P.rot("fw1", 7 * pull)
        P.rot("dau", 12 * pull - cv(t, [(0, 0), (H - 0.03, 0), (H, 4), (0.6, 3), (D, 0)]))
        P.move("than", cv(t, [(0, 0), (0.3, -14), (H, 30, "in"), (0.7, 24), (D, 0, "io")]), 0)
        P.scale("nga", cv(t, [(0, 1), (H - 0.03, 0.96), (H, 1.18), (H + 0.06, 1.0), (D, 1)]), 1)
        P.rot("ham", -cv(t, [(0, 0), (0.3, 10, "io"), (H, 2, "in"), (0.7, 0), (D, 0)]))
        for i, b in enumerate(bk):
            P.rot(b, (3 + i) * pull * 0.6)
        P.rot("vg0", -14 * pull)
        P.rot("vg1", -6 * pull)

    def cast_fn(t, P, D=1.5, H=0.55, E=1.25):
        """Thủy Pháo: ngực nén, ngửa tụ, hàm há to, phun 0,7 s giữ rung hai dáng, thở ra."""
        nen(P, lui(t, D), 1 - 0.8 * hoat.bao(t, 0.1, 1.4, 0.2, 0.2))
        rear = cv(t, [(0, 0), (0.4, 1, "io"), (0.5, 1.06), (H, 0.4, "in"), (E, 0.35), (D, 0, "io")])
        P.rot("fw0", 5 * rear)
        P.rot("fw1", 6 * rear)
        P.rot("dau", 10 * rear + 1.4 * rung(t, H + 0.03, E))
        P.rot("ham", -(cv(t, [(0, 0), (0.4, 8, "io"), (H, 42, "out"), (E, 38), (D, 0, "io")]) + 3 * rung(t, H + 0.03, E)))
        P.move("than", cv(t, [(0, 0), (H, 0), (H + 0.08, -16, "out"), (E, -10), (D, 0, "io")]), 0)
        P.scale("than", 1 + 0.03 * cv(t, [(0, 0), (0.45, 1, "io"), (H, -0.5, "in"), (E, -0.3), (D, 0)]), 1)
        for i, b in enumerate(cs):
            P.rot(b, 4 * rear * (2 - i) + 0.8 * rung(t, H + 0.03, E))
        P.rot("vg0", -10 * rear)
        P.rot("vx0", 8 * rear)

    def skill_fn(t, P, D=2.0, H=0.9, E=1.55):
        """Liên Hoa Hải Triều: ngẩng cao, sen xoè từng cánh lệch pha, đuôi quật xuống nước (song), gồng rung, gầm há miệng."""
        nen(P, lui(t, D), 1 - 0.85 * hoat.bao(t, 0.1, 1.9, 0.25, 0.4))
        up = cv(t, [(0, 0), (0.6, 1, "io"), (0.7, 1.08), (H, 0.75, "in"), (E, 0.7), (D, 0, "io")])
        P.rot("fw0", 9 * up + 1.2 * rung(t, H, E))
        P.rot("fw1", 7 * up)
        P.rot("dau", 14 * up + 2.0 * rung(t, H, E))
        P.move("than", -10 * up, 26 * up)
        for i, b in enumerate(bk):
            P.rot(b, -(2 + 2 * i) * up)
        tail = cv(t, [(0, 0), (0.6, -1, "io"), (0.8, -1.1), (H, 1, "in"), (H + 0.1, 1.15), (E, 0.8), (D, 0, "io")])
        for i, b in enumerate(du):
            P.rot(b, (10 + 6 * i) * tail)
        P.rot("vd", 10 * tail)
        P.rot("ham", -(cv(t, [(0, 0), (0.6, 6), (H, 44, "out"), (E, 40), (D, 0, "io")]) + 4 * rung(t, H, E)))
        for i, b in enumerate(cs):
            o = ease((t - 0.35 - 0.07 * abs(i - 2)) / 0.4) * (1 - ease((t - E - 0.1) / 0.3))
            P.rot(b, (22 - 11 * i) * o + 1.5 * rung(t, H, E))
            P.scale(b, 1 + 0.12 * o, 1 + 0.12 * o)
        for i, b in enumerate(ct):
            o = ease((t - 0.45 - 0.07 * abs(i - 1.5)) / 0.4) * (1 - ease((t - E - 0.1) / 0.3))
            P.rot(b, (26 - 17 * i) * o)
        P.scale("dai", 1 + 0.15 * ease((t - 0.5) / 0.4) * (1 - ease((t - E - 0.1) / 0.3)))
        # ba cánh rời bay lên từ hoa rồi tan (phần của chính con)
        for i in range(3):
            u = (t - (H - 0.05) - 0.08 * i) / 0.7
            if 0 <= u < 1:
                P.alpha[f"cr{i}"] = 1 - ease((u - 0.6) / 0.4)
                P.move(f"cr{i}", (40 + 60 * i) * u * (1 if i != 1 else -1), 90 * u + 60 * math.sin(math.pi * u))
                P.rot(f"cr{i}", 160 * u * (1 if i % 2 else -1))
        P.rot("vg0", -16 * up)
        P.rot("vx0", 12 * up)
        P.scale("nuoc", 1 + 0.08 * cv(t, [(0, 0), (H, 0), (H + 0.1, 1, "out"), (E, 0.4), (D, 0)]), 1)

    def hit_fn(t, P, D=0.6):
        nen(P, lui(t, D), ease((t - 0.25) / 0.35))
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 0.55, "io"), (0.42, -0.1, "io"), (D, 0, "io")])
        bd = cv(t, [(0, 0), (0.07, 0.3, "out"), (0.2, 1, "io"), (0.44, -0.05, "io"), (D, 0, "io")])
        P.rot("dau", 13 * hd)
        P.rot("fw1", 5 * hd)
        P.rot("fw0", 4 * bd)
        P.move("than", -16 * bd, 4 * hd)
        P.rot("ham", -10 * hd)
        an_hien(P, "mi", t, [(0.03, 0.34)])
        for i, b in enumerate(chain):   # sóng ngược từ ngọn về gốc
            P.rot(b, (3 + 1.2 * i) * cv(t, [(0, 0), (0.07 + 0.025 * (len(chain) - 1 - i), 1, "out"), (0.35 + 0.02 * i, -0.3, "io"), (D, 0, "io")]))
        for i, b in enumerate(cs):
            P.rot(b, (9 - 4 * i) * hd)
        P.rot("vg0", 12 * hd)

    def die_fn(t, P, D=2.2):
        """giật, nhắm mắt, lả đi giữ một nhịp (ngửa, hàm trễ, cánh sen rụng), đổ nghiêng xuống nước (toé), chìm, nước tan."""
        P.rot("dau", cv(t, [(0, 0), (0.07, 14, "out"), (0.3, 6), (0.9, -26, "io"), (1.3, -30), (D, -30)]))
        P.rot("ham", -cv(t, [(0, 0), (0.07, 16, "out"), (0.3, 6), (0.9, 26, "io"), (D, 26)]))
        P.rot("fw0", cv(t, [(0, 0), (0.07, 5, "out"), (0.9, -8, "io"), (D, -8)]))
        for i, b in enumerate(bk):
            P.rot(b, cv(t, [(0, 0), (0.07, 3 + i, "out"), (0.9, -(2 + i), "io"), (D, -(2 + i))]))
        for i, b in enumerate(du):
            P.rot(b, cv(t, [(0, 0), (0.1, 8 + 4 * i, "out"), (0.6, -6, "io"), (1.0, 3, "io"), (D, 0)]))
        P.rot("than", cv(t, [(0, 0), (1.25, 0), (1.6, -34, "in"), (1.7, -30, "out"), (D, -32)]))
        P.move("than", cv(t, [(0, 0), (1.25, 0), (1.7, 30), (D, 20)]), cv(t, [(0, 0), (0.07, 10, "out"), (1.25, -6), (1.6, -60, "in"), (1.75, -50, "out"), (2.0, -520, "in"), (D, -560)]))
        an_hien(P, "mi", t, [(0.04, D + 1)])
        for i, b in enumerate(cs + ct):
            fall = ease((t - 0.5 - 0.12 * i) / 0.5)
            P.rot(b, (30 if i % 2 else -30) * fall)
            P.alpha[("sen_sau" if i < 5 else "sen_truoc")] = 1.0
        for i in range(3):
            u = (t - 0.55 - 0.15 * i) / 0.8
            if 0 <= u < 1:
                P.alpha[f"cr{i}"] = 1 - ease((u - 0.65) / 0.35)
                P.move(f"cr{i}", (50 + 40 * i) * u * (1 if i != 1 else -1), -140 * u * u + 20 * u)
                P.rot(f"cr{i}", 120 * u * (1 if i % 2 else -1))
        for i, b in enumerate(vg):
            P.rot(b, cv(t, [(0, 0), (0.07, -10, "out"), (0.9, 12, "io"), (D, 12)]))
        for i, (b, _) in enumerate(nuoc["drops"]):
            pass
        g = cv(t, [(0, 1), (1.7, 1), (D, 0.05, "io")])
        P.scale("nuoc", g, g)
        a = cv(t, [(0, 1), (1.75, 1), (2.1, 0, "io"), (D, 0)])
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a
            elif s["name"] == "mi":
                P.alpha["mi"] = a
        P.alpha["phun_lo"] = 0.0

    def aura_fn(t, P):
        aura_nuoc(nuoc, t, P)

    return [Clip("appear", 1.6, appear_fn, mem=mem),
            Clip("idle", 3.2, idle_fn, loop=True, mem=mem),
            Clip("attack", 1.0, attack_fn, ev=[(0.46, "trung", "")], mem=mem),
            Clip("cast", 1.5, cast_fn, ev=[(0.55, "phun", ""), (1.25, "het_phun", "")], mem=mem),
            Clip("skill", 2.0, skill_fn, ev=[(0.75, "gam", ""), (0.9, "song", ""), (1.55, "het_gam", "")], mem=mem),
            Clip("hit", 0.6, hit_fn, mem=mem),
            Clip("die", 2.2, die_fn, mem=mem),
            Clip("aura", 2 * TW, aura_fn, loop=True)]


# ================================================================ dạng 1: Kình Nụ
def dung1(pc, nuoc):
    global B_VIEN, B_TRONG
    k = 1
    B_VIEN, B_TRONG = BUOC[k]
    print(f"  bước lưới dạng {k}: viền {B_VIEN:.1f}, trong {B_TRONG:.1f} px (cao {CAO[k]:.0f})")
    S = SC[k]
    O = (770.0, 872.0)

    def R(x, y):
        return ((x - O[0]) * S, (O[1] - y) * S)
    sk = khung.Sk(f"{CODE}_1")
    for n, im in pc.items():
        sk.anh(n, im)
    sk.xuong("root")
    sk.xuong("move", "root")
    info = {"pc": pc}
    KQ = doc_khop(k)

    def DK(nm, mac_dinh):
        if nm in KQ and os.path.exists(os.path.join(d_inbox(k), "manh", nm + ".png")):
            q = KQ[nm]
            return Dat(*R(q["cx"], q["cy"]), goc=q["r"], neo=(0.5, 0.5))
        return mac_dinh
    info["KQ"] = KQ
    im = pc["than"]
    w, h = im.size
    dat_than = Dat(*R(712, 536), goc=-3, ti=(1.0, 1.2))   # vị trí theo concept (lưng đỡ nụ ở y≈330, bụng 780); tỉ lệ từ khớp (TI);
    # concept thân tròn hơn hạt đậu GPT vẽ (1,35 so với 1,8): kéo cao 20 %
    cx, cy = dat_than.x, dat_than.y
    sk.xuong("than", "move", cx, cy, dai=40)
    sk.xuong("hong", "than", *dat_than.mot((0.2 * w, 0.5 * h), w, h), goc=dat_than.goc, the_gioi=True, dai=30)
    sk.xuong("nguc", "than", *dat_than.mot((0.8 * w, 0.5 * h), w, h), goc=dat_than.goc + 4, the_gioi=True, dai=30)
    # đuôi: vây đuôi theo khớp, cuống theo đường cong từ đuôi thân tới chân vây
    imv = pc["vay_duoi"]
    dat_vd = DK("vay_duoi", Dat(*R(450, 430), goc=-8, neo=(0.5, 0.5)))
    vd_root = dat_vd.mot((0.5 * imv.width, 0.96 * imv.height), *imv.size)
    tail_end = dat_than.mot((0.04 * w, 0.55 * h), w, h)
    Lc, fc = duong([tuple(tail_end), tuple(0.5 * (tail_end + vd_root) + np.array([-14, 0])), tuple(vd_root)])
    imc = pc["cuong"]
    Ld = luoi.luoi_dai(imc, 3, cot_moi_dot=3, buoc=B_TRONG * 0.85, ten="cuong")
    Lm = Ld.truc[1][-1]
    kc_ = Lc / Lm
    Dd, _ = Ld.truc
    yc = float(np.mean(Dd[:, 1]))
    Vd = []
    for (x, y), s in zip(Ld.pts, Ld.s):
        p, t = fc((Lm - s) * kc_)
        n = np.array([-t[1], t[0]])
        Vd.append(p - n * ((yc - y) * kc_))
    Vd = np.asarray(Vd)
    Jd = khop_cong(fc, np.linspace(0, Lc, 4))
    du = sk.chuoi("du", "hong", Jd)
    sk.xuong("vd", "du2", *Jd[3], goc=sk.goc_tg("du2")[2], dai=30, the_gioi=True)
    info["du"] = du
    # đầu
    imh = pc["dau"]
    wh, hh = imh.size
    dat_dau = DK("dau", Dat(*R(960, 500), goc=4, neo=(0.5, 0.5)))
    goc_dau = dat_dau.goc
    neck_w = dat_dau.mot((PT[k]["neck"][0] * wh, PT[k]["neck"][1] * hh), wh, hh)
    hinge = dat_dau.mot((PT[k]["hinge"][0] * wh, PT[k]["hinge"][1] * hh), wh, hh)
    snout = dat_dau.mot((PT[k]["snout"][0] * wh, PT[k]["snout"][1] * hh), wh, hh)
    sk.xuong("dau", "nguc", *neck_w, goc=goc_dau, dai=wh * 0.8, the_gioi=True)
    gj = math.degrees(math.atan2(*(snout - hinge)[::-1]))
    sk.xuong("ham", "dau", *hinge, goc=gj, dai=float(np.hypot(*(snout - hinge))), the_gioi=True)
    imj = pc["ham"]
    jk, jt = PT[k]["jaw_knob"], PT[k]["jaw_tip"]
    tilt = math.degrees(math.atan2((jk[1] - jt[1]) * imj.height, (jt[0] - jk[0]) * imj.width))
    dj = math.hypot((jt[0] - jk[0]) * imj.width, (jt[1] - jk[1]) * imj.height)
    tj = float(np.hypot(*(snout - hinge))) * PT[k].get("jaw_scale", 1.0) / max(1e-6, dj)
    dat_ham = Dat(*hinge, goc=gj - tilt, ti=tj, neo=jk)
    print(f"  hàm: chếch sẵn {tilt:.1f}°, góc đặt {gj - tilt:.1f}°, co {tj:.3f}")
    mp = hinge + 0.86 * (snout - hinge) + np.array([0, 5])
    sk.xuong("mieng", "dau", *mp, goc=gj + 4, dai=30, the_gioi=True)
    imn = pc["nga"]
    dat_nga = DK("nga", Dat(*dat_dau.mot((PT[k]["tusk"][0] * wh, PT[k]["tusk"][1] * hh), wh, hh), goc=goc_dau + 34, neo=(0.03, 0.5)))
    tr = dat_nga.mot((0.03 * imn.width, 0.5 * imn.height), *imn.size)
    sk.xuong("nga", "dau", *tr, goc=dat_nga.goc, dai=imn.width, the_gioi=True)
    sk.xuong("mui_nga", "nga", imn.width * 0.95, 0, 0, 10)
    # vây chèo gần, vây lưng, nụ
    imf = pc["vay_cheo"]
    wf, hf = imf.size
    Lf = luoi.luoi_dai(imf, 2, cot_moi_dot=3, buoc=B_TRONG * 0.85, ten="vay_cheo")
    dat_vg = DK("vay_cheo", Dat(*R(735, 648), goc=-62, neo=(0.05, 0.5)))
    vg = sk.chuoi("vg", "nguc", dat_vg.ra(Lf.khop(2), wf, hf))
    iml = pc["vay_lung"]
    wl, hl = iml.size
    Ll = luoi.luoi_vung(iml, B_VIEN, B_TRONG, ten="vay_lung")
    dat_vl = DK("vay_lung", Dat(*R(600, 358), goc=0, neo=(0.6, 1.0)))
    Jl = dat_vl.ra([(0.6 * wl, hl), (0.42 * wl, 0.5 * hl), (0.25 * wl, 0.04 * hl)], wl, hl)
    vl = sk.chuoi("vl", "than", Jl)
    imdn = pc["de_nu"]
    dat_dn = DK("de_nu", Dat(*R(732, 352), neo=(0.5, 0.75)))
    dat_ns = DK("nu_sau", Dat(*R(732, 352), goc=4, neo=(0.5, 0.97)))
    dat_nt = DK("nu_truoc", Dat(*(np.array(R(732, 352)) + np.array([4, -4])), goc=-4, neo=(0.5, 0.97)))
    nu0 = np.array(dat_dn.mot((0.5 * imdn.width, 0.5 * imdn.height), *imdn.size))
    sk.xuong("nu", "than", *nu0, goc=96, dai=30, the_gioi=True)
    sk.xuong("nu_s", "nu", 0, 0)
    sk.xuong("nu_t", "nu", 0, 0)
    info.update(vg=vg, vl=vl)

    def sau_than():
        sk.slot("vl", vl[0], "vay_lung")
        sk.slot("de_nu", "nu", "de_nu")
        sk.slot("nu_sau", "nu_s", "nu_sau")
        sk.slot("nu_truoc", "nu_t", "nu_truoc")

    def truoc_than():
        sk.slot("vd", "vd", "vay_duoi")
        sk.slot("cuong", du[0], "cuong")
        sk.slot("than", "than", "than")
        sk.slot("long", "ham", "mieng")
        sk.slot("ham", "ham", "ham")
        sk.slot("nga", "nga", "nga")
        sk.slot("dau", "dau", "dau")
        sk.slot("mi", "dau", "mi", an=True)
        sk.slot("vg", vg[0], "vay_cheo")
        for i, nmp in enumerate(("canh_a", "canh_b", "canh_c")):
            sk.xuong(f"cr{i}", "nu", 0, 0)
            sk.slot(f"cr{i}", f"cr{i}", nmp, an=True)
        return "cr2"
    info["nuoc"] = them_nuoc(sk, nuoc, k, truoc_than, sau_than)
    # lưới thân: ba vùng
    Lt = luoi.luoi_vung(im, B_VIEN, B_TRONG, ten="than")
    Wt = trongso.vung(Lt, [("hong", [(0, 0), (0.28 * w, 0), (0.28 * w, h), (0, h)]), ("nguc", [(0.72 * w, 0), (w, 0), (w, h), (0.72 * w, h)]),
                           ("than", [(0, 0), (w, 0), (w, h), (0, h)])], dai_hoa=70 * S)
    Wt = trongso.lam_tron(Lt, Wt, 2)
    trongso.kiem(Wt, "than")
    sk.luoi_gan("than", "than", Lt, Wt, dat=dat_than)
    Wd = trongso.chuoi(Lm - Ld.s, Lm / 3, du, cha="hong", cha_hoa=0.6)
    sk.luoi_gan("cuong", "cuong", Ld, Wd, the_gioi=Vd)
    sk.manh("vd", "vay_duoi", dat_vd)
    Lh = luoi.luoi_vung(imh, B_VIEN, B_TRONG, ten="dau")
    Wh = trongso.vung(Lh, [("nguc", [(0, 0.3 * hh), (0.12 * wh, 0.4 * hh), (0.12 * wh, hh), (0, hh)]), ("dau", [(0, 0), (wh, 0), (wh, hh), (0, hh)])],
                      dai_hoa=24 * S)
    Wh = trongso.lam_tron(Lh, Wh, 1)
    trongso.kiem(Wh, "dau", cho_cung=("dau",))
    sk.luoi_gan("dau", "dau", Lh, Wh, dat=dat_dau)
    Lj = luoi.luoi_vung(imj, B_VIEN * 0.8, B_TRONG * 0.8, ten="ham")
    Wj = mieng.ham_hai_xuong(dat_ham.ra(Lj.pts, *imj.size), hinge, snout, "dau", "ham")
    sk.luoi_gan("ham", "ham", Lj, Wj, dat=dat_ham)
    mieng.long_mieng(sk, "long", "mieng", "dau", "ham", hinge, snout, duoi=-0.26)
    sk.manh("nga", "nga", dat_nga)
    if os.path.exists(os.path.join(d_inbox(k), "manh", "dau.png")):
        kq = mieng.fit_lid(imh, pc["mi"], mat=mat_cyan(imh), ten="dạng 1")
        sk.manh("mi", "mi", mieng.dat_mi(dat_dau, imh, kq))
    else:
        sk.manh("mi", "mi", Dat(*dat_dau.mot((PT[k]["eye"][0] * wh, PT[k]["eye"][1] * hh), wh, hh), goc=goc_dau))
    Wf = trongso.chuoi(Lf.s, Lf.truc[1][-1] / 2, vg, cha="nguc", cha_hoa=0.6)
    sk.luoi_gan("vg", "vay_cheo", Lf, Wf, dat=dat_vg)
    Wl = trongso.chuoi_chieu(dat_vl.ra(Ll.pts, wl, hl), Jl, vl, cha="than", cha_hoa=0.6)
    sk.luoi_gan("vl", "vay_lung", Ll, Wl, dat=dat_vl)
    sk.manh("de_nu", "de_nu", dat_dn)
    sk.manh("nu_sau", "nu_sau", dat_ns)
    sk.manh("nu_truoc", "nu_truoc", dat_nt)
    for i, nmp in enumerate(("canh_a", "canh_b", "canh_c")):
        sk.manh(f"cr{i}", nmp, Dat(*nu0, neo=(0.5, 0.5)))
    for e, m in (("trung", "viên nước rời miệng (VFX bám mieng)"), ("phun", "bắt đầu nhả bong bóng sen"), ("het_phun", "hết nhả"),
                 ("bung", "nụ bật mở: VFX mưa cánh sen"), ("het_bung", "nụ khép lại")):
        sk.su_kien(e, m)
    return sk, info


def clips1(sk, info):
    du, vg, vl, nuoc = info["du"], info["vg"], info["vl"], info["nuoc"]
    mem = [LoXo(du, k=[400, 300, 220], damp=0.6, maxang=14), LoXo(vg, k=[360, 260], damp=0.6, maxang=10), LoXo(vl, k=[400, 300], damp=0.6, maxang=8)]

    def nen(P, tt, a=1.0):
        s = song0(tt, 2.4)
        P.move("than", 0, 6.0 * a * s)
        P.scale("than", 1 - 0.015 * a * s, 1 + 0.025 * a * s)
        P.rot("nguc", 1.5 * a * song0(tt, 2.4, 0.8))
        P.rot("hong", -1.5 * a * song0(tt, 2.4, 0.8))
        P.rot("dau", (-2.0 * song0(tt, 2.4, 0.8) + 1.0 * song0(tt, 2.4, 2.4)) * a)
        song_than(P, du, tt, 2.4, np.array([4, 6, 8])[:len(du)] * a, tre=0.1, ngon_dan=False)
        P.rot("nu", 2.5 * a * song0(tt, 2.4, 1.6))
        P.rot("nu_t", 1.5 * a * song0(tt, 2.4, 2.4))
        P.rot("vg0", 6 * a * song0(tt, 2.4, 0.3))
        P.rot("vl0", 2 * a * song0(tt, 2.4, 2.0))

    def idle_fn(t, P, D=2.4):
        nen(P, t)
        P.rot("ham", -cv(t, [(0, 0), (1.5, 0), (1.6, 8, "out"), (1.75, 2), (1.9, 0, "io"), (D, 0)]))
        an_hien(P, "mi", t, [(0.7, 0.82), (0.92, 1.02)])

    def appear_fn(t, P, D=1.4):
        nen(P, lui(t, D), ease((t - 0.55) / 0.5))
        P.move("than", 0, cv(t, [(0, -420), (0.6, 36, "out"), (0.8, -10, "io"), (1.0, 0, "io"), (D, 0)]))
        g = cv(t, [(0, 0.05), (0.35, 1.0, "out"), (D, 1)])
        P.scale("nuoc", g, max(0.05, g))
        a = cv(t, [(0, 0), (0.1, 1)])
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a
        P.rot("dau", cv(t, [(0, -14), (0.6, 8, "out"), (0.9, 0, "io"), (D, 0)]))
        P.rot("ham", -cv(t, [(0, 0), (0.6, 0), (0.72, 20, "out"), (1.0, 0, "io"), (D, 0)]))

    def attack_fn(t, P, D=0.9, H=0.42):
        """Phun Nước: lùi nhẹ lấy đà, ngẩng, phụt viên nước từ miệng (đứng tại chỗ)."""
        nen(P, lui(t, D), 1 - 0.7 * hoat.bao(t, 0.1, 0.8, 0.2, 0.25))
        pull = cv(t, [(0, 0), (0.28, 1, "io"), (0.34, 1.06), (H, -0.8, "in"), (H + 0.05, -1.0), (0.62, -0.8, "io"), (D, 0, "io")])
        P.rot("nguc", -4 * pull)
        P.rot("dau", -8 * pull)
        P.move("than", cv(t, [(0, 0), (0.28, -12), (H, 18, "in"), (0.62, 14), (D, 0, "io")]), 0)
        P.scale("than", 1 + 0.04 * max(pull, 0), 1 - 0.03 * max(pull, 0))
        P.rot("ham", -cv(t, [(0, 0), (0.25, 16, "io"), (H - 0.03, 22), (H, 30), (0.55, 8), (D, 0)]))
        P.rot("vg0", -12 * pull)

    def cast_fn(t, P, D=1.3, H=0.5, E=1.05):
        """Bong Bóng Sen: ngửa tụ, há miệng nhả ba bong bóng, nụ rung."""
        nen(P, lui(t, D), 1 - 0.8 * hoat.bao(t, 0.1, 1.2, 0.2, 0.2))
        rear = cv(t, [(0, 0), (0.38, 1, "io"), (0.45, 1.06), (H, 0.5, "in"), (E, 0.4), (D, 0, "io")])
        P.rot("nguc", 5 * rear)
        P.rot("dau", 12 * rear + 1.5 * rung(t, H + 0.03, E))
        P.rot("ham", -(cv(t, [(0, 0), (0.38, 6, "io"), (H, 34, "out"), (E, 30), (D, 0, "io")]) + 3 * rung(t, H + 0.03, E)))
        P.move("than", cv(t, [(0, 0), (H, 0), (H + 0.08, -12, "out"), (E, -8), (D, 0, "io")]), 0)
        P.rot("nu", 6 * rear + 1.0 * rung(t, H + 0.03, E))

    def skill_fn(t, P, D=1.8, H=0.7, E=1.3):
        """Nụ Bung: nụ phồng 0,5 s rồi bật mở (hai lớp cánh tách, cánh rời bay lên), rung, khép lại."""
        nen(P, lui(t, D), 1 - 0.85 * hoat.bao(t, 0.1, 1.7, 0.25, 0.4))
        sw = cv(t, [(0, 0), (0.5, 1, "io"), (0.6, 1.08), (H, 0.3, "in"), (E, 0.3), (D, 0, "io")])
        op = cv(t, [(0, 0), (H - 0.05, 0), (H, 1, "out"), (E, 0.9), (D, 0, "io")])
        P.scale("nu", 1 + 0.2 * sw + 0.1 * op, 1 + 0.25 * sw)
        P.rot("nu_s", 24 * op + 1.5 * rung(t, H, E))
        P.rot("nu_t", -28 * op - 1.5 * rung(t, H, E))
        P.scale("nu_t", 1 + 0.1 * op, 1 - 0.1 * op)
        P.scale("than", 1 - 0.04 * sw, 1 + 0.06 * sw)
        P.rot("dau", -6 * sw + 8 * op)
        P.rot("ham", -(cv(t, [(0, 0), (0.5, 4), (H, 30, "out"), (E, 26), (D, 0, "io")]) + 3 * rung(t, H, E)))
        P.rot("nguc", -3 * sw + 1.0 * rung(t, H, E))
        for i in range(3):
            u = (t - H - 0.06 * i) / 0.75
            if 0 <= u < 1:
                P.alpha[f"cr{i}"] = 1 - ease((u - 0.6) / 0.4)
                P.move(f"cr{i}", (30 + 45 * i) * u * (1 if i != 1 else -1), 110 * u + 50 * math.sin(math.pi * u))
                P.rot(f"cr{i}", 200 * u * (1 if i % 2 else -1))
        for i, b in enumerate(du):
            P.rot(b, (6 + 4 * i) * sw * (1 if i % 2 else -1) * 0.6)
        P.rot("vg0", -14 * sw)

    def hit_fn(t, P, D=0.6):
        nen(P, lui(t, D), ease((t - 0.25) / 0.35))
        hd = cv(t, [(0, 0), (0.07, 1, "out"), (0.2, 0.55, "io"), (0.42, -0.12, "io"), (D, 0, "io")])
        bd = cv(t, [(0, 0), (0.07, 0.3, "out"), (0.2, 1, "io"), (0.44, -0.05, "io"), (D, 0, "io")])
        P.rot("dau", -14 * hd)
        P.rot("nguc", 6 * bd)
        P.rot("hong", -4 * bd)
        P.move("than", -12 * bd, 0)
        P.scale("than", 1 - 0.06 * hd, 1 + 0.08 * hd)
        P.rot("ham", -10 * hd)
        P.rot("nu", 14 * hd)
        an_hien(P, "mi", t, [(0.03, 0.34)])
        for i, b in enumerate(du):
            P.rot(b, (6 + 3 * i) * cv(t, [(0, 0), (0.07 + 0.03 * (len(du) - 1 - i), 1, "out"), (0.35 + 0.03 * i, -0.3, "io"), (D, 0, "io")]))
        P.rot("vg0", 12 * hd)

    def die_fn(t, P, D=2.0):
        P.rot("dau", cv(t, [(0, 0), (0.07, 14, "out"), (0.3, 6), (0.85, -24, "io"), (D, -26)]))
        P.rot("ham", -cv(t, [(0, 0), (0.07, 16, "out"), (0.3, 6), (0.85, 22, "io"), (D, 22)]))
        P.rot("nguc", cv(t, [(0, 0), (0.07, 5, "out"), (0.85, -8, "io"), (D, -8)]))
        P.rot("nu", cv(t, [(0, 0), (0.07, 8, "out"), (0.85, 38, "io"), (D, 42)]))   # nụ héo cụp
        P.rot("nu_t", cv(t, [(0, 0), (0.85, 0), (1.2, 14, "io"), (D, 14)]))
        P.rot("than", cv(t, [(0, 0), (1.15, 0), (1.5, 48, "in"), (1.6, 44, "out"), (D, 46)]))
        P.move("than", cv(t, [(0, 0), (1.15, 0), (1.6, 20), (D, 16)]), cv(t, [(0, 0), (0.07, 10, "out"), (1.15, -4), (1.5, -40, "in"), (1.62, -34, "out"), (1.85, -420, "in"), (D, -460)]))
        an_hien(P, "mi", t, [(0.04, D + 1)])
        for i, b in enumerate(du):
            P.rot(b, cv(t, [(0, 0), (0.1, 8 + 4 * i, "out"), (0.6, -6, "io"), (1.0, 3, "io"), (D, 0)]))
        g = cv(t, [(0, 1), (1.55, 1), (D, 0.05, "io")])
        P.scale("nuoc", g, g)
        a = cv(t, [(0, 1), (1.6, 1), (1.9, 0, "io"), (D, 0)])
        for s in sk.slots:
            if s["alpha"] > 0:
                P.alpha[s["name"]] = a
            elif s["name"] == "mi":
                P.alpha["mi"] = a

    def aura_fn(t, P):
        aura_nuoc(nuoc, t, P)

    return [Clip("appear", 1.4, appear_fn, mem=mem),
            Clip("idle", 2.4, idle_fn, loop=True, mem=mem),
            Clip("attack", 0.9, attack_fn, ev=[(0.42, "trung", "")], mem=mem),
            Clip("cast", 1.3, cast_fn, ev=[(0.5, "phun", ""), (1.05, "het_phun", "")], mem=mem),
            Clip("skill", 1.8, skill_fn, ev=[(0.7, "bung", ""), (1.3, "het_bung", "")], trung=0.7, mem=mem),
            Clip("hit", 0.6, hit_fn, mem=mem),
            Clip("die", 2.0, die_fn, mem=mem),
            Clip("aura", 2 * TW, aura_fn, loop=True)]


# ================================================================ soi nhanh, uốn thử
O_CONCEPT = {2: (770.0, 905.0), 1: (770.0, 872.0)}


def can3(sk, frames, ra, ds):
    """ảnh cận nền xám phóng 3× các chỗ đã sửa: ds = [(tên, clip, giây, (x, y) | tên xương, bán kính)]."""
    ve = soi.Ve(sk)
    for nm_, cl_, t_, tam, r in ds:
        fr = frames[cl_][min(len(frames[cl_]) - 1, int(round(t_ * 30)))]
        if isinstance(tam, str):
            tam = tuple(sk.the_gioi(fr)[tam][:2, 2])
        soi.anh_can(ve, fr, tam, r, os.path.join(ra, nm_ + ".png"), phong=3.0, luoi=False)


def ghi_mat_do(sk, k, ra, iou):
    """ghi số đỉnh / chiều cao và IoU vào so_sanh.md (đỉnh thân = mọi lưới trừ nước và dạng sau n_*)."""
    nuoc_slot = lambda n: n.startswith(("w", "dai_nuoc", "giot", "n_"))  # noqa: E731
    nv = sum(len(a["verts"]) for sl, d in sk.atts.items() if not nuoc_slot(sl) for a in d.values() if a["type"] == "mesh")
    nn = sum(len(a["verts"]) for sl, d in sk.atts.items() if sl.startswith(("w", "dai_nuoc", "giot")) for a in d.values() if a["type"] == "mesh")
    ho = {nm: L.ho for (sl, nm), L in sk.luoi.items() if L.ho}
    dong = ["", "## Mật độ lưới", "",
            f"- Chiều cao con (rig): {CAO[k]:.0f} px; bước viền {BUOC[k][0]:.1f} / bước trong {BUOC[k][1]:.1f} px (1,5 % / 2 % chiều cao).",
            f"- Đỉnh thân (không tính nước): {nv}; đỉnh nước: {nn}; đỉnh / chiều cao: {nv / CAO[k]:.2f}.",
            f"- Mảnh còn hở: {ho if ho else 'không (0 px mọi mảnh)'}.",
            f"- IoU mặt nạ khung 0 idle / concept: {iou:.3f} (so_concept.png).", ""]
    txt = "\n".join(dong)
    with open(os.path.join(ra, "so_sanh.md"), "a", encoding="utf-8") as f:
        f.write(txt)
    print(f"  đỉnh thân {nv} / cao {CAO[k]:.0f} = {nv / CAO[k]:.2f}; hở: {ho or 0}")


def so_concept(sk, P0, k, ra):
    """khung 0 idle vẽ đúng tỉ lệ concept (1 px rig = 1/SC px concept), đặt cạnh concept đã duyệt: bóng dáng phải khớp."""
    con = Image.open(os.path.join(d_inbox(k), "tai_ve", "L1_duyet.png")).convert("RGB")
    ox, oy = O_CONCEPT[k]
    S = SC[k]
    box = (-ox * S, (oy - con.height) * S, (con.width - ox) * S, oy * S)
    ve = soi.Ve(sk)
    a = ve.ve(P0, box, 1.0 / S, bg=(255, 255, 255), ss=2).convert("RGB")
    a = a.resize(con.size)
    mc = np.asarray(con).min(axis=2) < 236
    mr = np.asarray(a).min(axis=2) < 236
    iou = float((mc & mr).sum() / max(1, (mc | mr).sum()))
    out = Image.new("RGB", (con.width * 2 + 20, con.height), (120, 120, 120))
    out.paste(con, (0, 0))
    out.paste(a, (con.width + 20, 0))
    out = out.resize((out.width // 2, out.height // 2), Image.LANCZOS)
    from PIL import ImageDraw
    ImageDraw.Draw(out).text((con.width // 2 + 14, 6), f"IoU mat na khung 0 idle / concept = {iou:.3f}", fill=(200, 20, 20), font=anh.font(18))
    out.save(ra)
    print(f"  so_concept: IoU = {iou:.3f} -> {ra}")
    return iou


def dung_lien(k, **kw):
    """cách lai (tm07_dung.py): thân cắt từ concept một lưới liền; kw cho dạng 2: nuoc_thua, luoi_thua, sc."""
    import tm07_dung as D
    pc, nuoc, lien = D.nap_lien(k, sc=kw.get("sc"))
    return D.dung2(pc, nuoc, lien, **kw) if k == 2 else D.dung1(pc, nuoc, lien)


def soi_dang(k, ra):
    sk, info = dung_lien(k)
    ve = soi.Ve(sk)
    P = khung.Pose()
    B = soi._union([ve.bao(P)], 0.05)
    a = ve.ve(P, B, 1.0, bg=(150, 150, 150), ss=2, xuong=True)
    a.convert("RGB").save(ra)
    print("  ", ra, sk.tom_tat())
    return sk, info


def uon_thu(sk, info, ra, k):
    P = khung.Pose()
    for b in info["du"]:
        P.rot(b, 18)
    if k == 2:
        for b in info["bk"]:
            P.rot(b, 7)
        for b in info["fw"]:
            P.rot(b, -5)
        for b in info["vx"]:
            P.rot(b, 10)
    for b in info["vg"]:
        P.rot(b, -14)
    P.rot("dau", 14)
    P.rot("ham", -34)
    ve = soi.Ve(sk)
    B = soi._union([ve.bao(P)], 0.05)
    a = ve.ve(P, B, 1.4, bg=(150, 150, 150), ss=2, luoi=True, mau_luoi=(10, 10, 10, 110))
    a.convert("RGB").save(ra)
    return ra


# ================================================================ chạy
def rig2():
    t0 = time.time()
    sk, info = dung_lien(2)
    cl = clips2(sk, info)
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    print(f"dạng 2: nướng {len(cl)} clip ({time.time() - t0:.1f} s)")
    ra = os.path.join(d_inbox(2), "rig")
    tk = xuat.xuat_het(sk, cl, ra, f"{CODE}_2", "Liên Kình (dạng 2)", frames=fr, dang=2, so_dang=2, ma_goc=3244,
                       dung_yen=("attack", "cast", "skill"), tol=TOL_KHOA,
                       can=[("can_mieng_cast", "cast", 0.75, "ham", 90), ("can_mieng_skill", "skill", 1.0, "ham", 90),
                            ("can_nga_attack", "attack", 0.47, "mui_nga", 80), ("can_mi_hit", "hit", 0.12, "dau", 80),
                            ("can_duoi_hit", "hit", 0.1, "du1", 110), ("can_sen_skill", "skill", 1.0, "sen", 150),
                            ("can_vay_idle", "idle", 1.0, "vg1", 100)])
    uon_thu(sk, info, os.path.join(ra, "uon_thu.png"), 2)
    can3(sk, fr, ra, [("can3_mom", "idle", 0.0, "mieng", 70), ("can3_goc_sen_trai", "idle", 0.0, (-150, 300), 70),
                      ("can3_chop_vay_lung", "idle", 0.0, "vl1", 80), ("can3_vay_duoi_attack", "attack", 0.5, "vd", 110),
                      ("can3_vay_duoi_attack2", "attack", 0.55, "du1", 100), ("can3_vay_xa", "idle", 0.0, "vx0", 90)])
    iou = so_concept(sk, fr["idle"][0], 2, os.path.join(ra, "so_concept.png"))
    ghi_mat_do(sk, 2, ra, iou)
    return sk, info, cl, fr, tk


def rig1(sk2=None, cl2=None, fr2=None):
    t0 = time.time()
    if sk2 is None:   # dạng 2 trong rig gộp chỉ hiện ở clip evolve 2,8 s: ảnh co 0,5 (thay vì 0,72), nước và lưới thưa hơn cho nhẹ
        sk2, info2 = dung_lien(2, nuoc_thua=True, luoi_thua=1.6, sc=SC_GOP)
        cl2 = clips2(sk2, info2)
        fr2 = {"idle": hoat.nuong(sk2, cl2[1]), "aura": hoat.nuong(sk2, cl2[-1])}
    sk1, info1 = dung_lien(1)
    cl1 = clips1(sk1, info1)
    fr1 = {c.ten: hoat.nuong(sk1, c) for c in cl1}
    ve1, ve2 = soi.Ve(sk1), soi.Ve(sk2)
    bo1, bo2 = xuat.slot_aura(sk1, fr1["aura"]), xuat.slot_aura(sk2, fr2["aura"])
    hA, hB = soi.chieu_cao(ve1, fr1["idle"][0], bo1), soi.chieu_cao(ve2, fr2["idle"][0], bo2)
    M = tienhoa.gop(sk1, sk2)

    def gong(t, P):   # dạng 1 gồng: nụ phồng to, ngửa đầu, rung
        sq = cv(t, [(0, 0), (0.3, -0.06), (0.45, 0.06, "out"), (1.0, 0.05), (1.3, 0.0)])
        P.scale("than", 1 - 0.5 * sq, 1 + sq)
        P.scale("nu", 1 + cv(t, [(0, 0), (0.3, 0.05), (1.0, 0.45, "io"), (1.3, 0.6)]))
        P.rot("dau", cv(t, [(0, 0), (0.3, -6), (0.6, 12, "out"), (1.3, 14)]) + 1.5 * rung(t, 0.5, 1.3))
        P.rot("ham", -cv(t, [(0, 0), (0.6, 0), (1.0, 18, "out"), (1.3, 20)]))

    def gam(t, P, fl):   # dạng 2 gầm, sen xoè
        P.rot("n_dau", 12 * fl)
        P.rot("n_ham", -36 * fl)
        for i, b in enumerate(info2_cs):
            P.rot(b, (18 - 9 * i) * fl)
        P.scale("n_than", 1 + 0.04 * fl, 1 + 0.04 * fl)
    info2_cs = [f"n_cs{i}" for i in range(5)]
    memM = cl1[1].mem + tienhoa.doi_ten_mem(cl2[1].mem)
    ev = tienhoa.clip_tien_hoa(M, sk1, sk2, fr2["idle"][0], tiB=hA / hB, fnA=gong, fnB=gam, mem=memM)
    aura = tienhoa.gop_aura(cl1[-1], cl2[-1])
    clM = [c for c in cl1 if c.ten != "aura"] + [ev, aura]
    frM = {c.ten: fr1[c.ten] for c in cl1 if c.ten != "aura"}
    frM["evolve"] = hoat.nuong(M, ev)
    frM["aura"] = hoat.nuong(M, aura)
    _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], hA / hB)
    ra = os.path.join(d_inbox(1), "rig")
    tk = xuat.xuat_het(M, clM, ra, f"{CODE}_1", "Kình Nụ (dạng 1, gộp tiến hóa)", frames=frM, dang=1, so_dang=2, ma_goc=3244,
                       dung_yen=("attack", "cast", "skill"), tol=TOL_KHOA, noi_them={"evolve": s_ev + f" (dạng sau co {hA / hB:.3f} trong rig gộp)"},
                       can=[("can_mieng_cast", "cast", 0.7, "ham", 80), ("can_mieng_attack", "attack", 0.44, "ham", 80),
                            ("can_mi_hit", "hit", 0.12, "dau", 90), ("can_duoi_hit", "hit", 0.1, "du1", 90),
                            ("can_nu_skill", "skill", 0.9, "nu", 130)])
    uon_thu(sk1, info1, os.path.join(ra, "uon_thu.png"), 1)
    iou = so_concept(sk1, fr1["idle"][0], 1, os.path.join(ra, "so_concept.png"))
    ghi_mat_do(M, 1, ra, iou)
    print(f"dạng 1 xong {time.time() - t0:.1f} s")
    return tk


def main(a):
    if not a:
        print(__doc__)
        return
    if a[0] == "cat":
        cat(int(a[1]))
    elif a[0] == "soi":
        k = int(a[1])
        sk, info = soi_dang(k, os.path.join(d_inbox(k), "dat_thu.png"))
        uon_thu(sk, info, os.path.join(d_inbox(k), "uon_thu.png"), k)
        so_concept(sk, khung.Pose(), k, os.path.join(d_inbox(k), "so_concept.png"))
    elif a[0] == "rig":
        if a[1] == "2":
            rig2()
        else:
            rig1()
    elif a[0] == "all":
        rig2()
        rig1()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
