# -*- coding: utf-8 -*-
"""Kiếm sĩ rừng (kiem_si): rig trên bộ xương của con gốc monster_3620 (bọ hung samurai hai kiếm). Mảnh của mình là MẢNH CỨNG / lưới ô nhỏ
đặt theo concept đã duyệt (voọc tướng quân); chuyển động nền lấy mẫu từ clip của họ (<scan>/sample_goc.json, runtime Spine thật đã giải
IK chân), phần riêng viết thêm ở kiem_si_clip.py.

- DÁNG GỐC của rig mình = khung 0 idle_01 của họ (thế thủ gù), vì concept vẽ theo dáng đó; mọi khoá là lệch so với dáng này.
- Xương của họ: giữ thân, đầu, mũ, hai tay, hai tấm vai, giáp ngực, các xương kiếm, HAI chân (chân gần-sau Rh, chân xa-trước Lq); bỏ hai
  chân còn lại, cánh cứng, chùm lông, tua, ngón tay (mảnh của mình không dùng).
- Xương của mình (tiền tố x_): đuôi 5 đốt, áo tơi lá 3 đốt, hai lá mào, bốn tua, váy (lò xo + gió).
- Hai thanh kiếm đặt ĐÚNG chỗ kiếm của rig gốc ở mọi slot của họ (trong vỏ / trên tay xa / giắt hông), bật tắt theo đúng mẫu khung.
- Ảo ảnh của chiêu cuối: ảnh chụp chính con này ở dáng chém, nhuộm lục, trên xương `ao_*` con của `far` (chỗ đối thủ, game dời).

    kiem_si_rig.py                    dựng, xuất inbox/kiem_si_1/rig/ (JSON Spine, atlas, .atomik, tờ khung, xem.html)
    kiem_si_rig.py soi <clip> <giây,giây,...> [tỉ lệ] [xuong]   khung lớn nền xám → rig/soi_<clip>.png
    kiem_si_rig.py tinh               dáng gốc cạnh concept → rig/soi_tinh.png
Chạy qua quai/khoa.py nang. Xương và chuyển động nền là của nhà phát hành game tham khảo: dùng nội bộ."""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh, khung, hoat, xuat, soi  # noqa: E402
from quai import luoi as LU  # noqa: E402
from quai.hoat import LoXo  # noqa: E402
import kiem_si as KS  # noqa: E402
import kiem_si_manh as KM  # noqa: E402

TEN = f"kiem_si_{KS.K}"
RA = os.path.join(KS.BASE, "rig")
SCAN = KS.scan()
KG = 0.36                    # đơn vị rig con gốc → đơn vị rig của mình
PXU = 0.56                   # pixel ảnh atlas cho mỗi đơn vị rig con gốc
I = json.load(open(os.path.join(SCAN, "info.json"), encoding="utf-8"))
S = json.load(open(os.path.join(SCAN, "sample_goc.json"), encoding="utf-8"))
A0 = json.load(open(os.path.join(SCAN, "att_idle0.json"), encoding="utf-8"))
AG = json.load(open(os.path.join(SCAN, "att_goc.json"), encoding="utf-8"))
IB = I["bones"]
TENX = [b["name"] for b in IB]
SLOT_HO = [s["name"] for s in I["slots"]]
B0 = np.array([f[:5] for f in S["idle_01"]["frames"][0]["l"]], float)      # dáng gốc của mình = khung 0 idle của họ (x, y, góc, sx, sy)
TIEU_DE = "Kiếm sĩ rừng (kiem_si_1): voọc tướng quân, tướng thứ 8 đảo Mộc"
# xương của họ không dùng: bóng, hai chân bỏ (Rq: bone14-15, Lh: bone8-9), cánh cứng, hai chùm lông, bốn chuỗi tua, ngón tay, đích IK tay
BO = {"root", "shadow", "bone8", "bone9", "Lh", "bone14", "bone15", "Rq", "bone10", "bone11", "bone12", "bone13", "bone34", "bone35", "bone36", "bone37", "bone38",
      "bone39", "bone40", "bone41", "shouL", "shouL2", "bone53", "bone53b",
      "bone53c", "bone54", "bone53b2", "bone53c2", "bone55", "bone53b3", "bone53c3", "bone56", "bone53b4", "bone53c4"}
TAY = {"g": dict(don="bone21", bap="bone22", cang="bone23", nam="bone24"), "x": dict(don="bone17", bap="bone18", cang="bone19", nam="bone20")}
CHAN = {"s": "Rh", "t": "Lq"}             # bàn chân + giáp ống chân bám cứng xương đích của họ; đùi là lưới giãn từ hông xuống
# cặp (mảnh của mình, hình của họ) để khớp khung concept với hệ toạ độ rig gốc (tâm khung bao)
NEO = [("vai_g", "P_jianjiaR1"), ("cang_g", "P_shouR2"), ("cang_x", "P_shouL2"), ("vai_x", "P_jianjiaL1")]
# điểm concept (px) ↔ gốc xương của họ: hai lòng bàn chân ↔ hai đích chân
NEO_DIEM = [((482, 1000), "Rh"), ((950, 1002), "Lq")]
# mảnh chi: hai khớp (tỉ lệ khung ảnh mảnh: u ngang, v dọc từ trên) → gốc xương của nó và gốc xương con
HAI = {"cang_g": ((0.30, 0.42), (0.90, 0.70), "bone23", "bone24"), "cang_x": ((0.55, 0.12), (0.42, 0.90), "bone19", "bone20")}
MOT = {}
# mảnh THÂN vẽ đúng khung part của họ (kiem_si_part.py): tên của mình → slot của họ. Đặt bằng phép affine ảnh vùng → thế giới của chính
# part đó, bám đúng xương (trọng số) của nó: thân kín như con gốc, bắp tay nối tấm vai với bao tay.
KP = {"gu": "P_ke", "ao": "P_keR", "lung": "P_keL", "bung": "P_shenti1", "khuyu_x": "P_shouL2_2", "bap_x": "P_shouL1", "than": "P_shenti2",
      "co": "P_tou2", "khuyu_g": "P_shouR2_2", "bap_g": "P_shouR1",
      # BÀN TAY tách ngón đúng như con gốc (tờ Q của kiem_si_part.py): mỗi tay một khối lòng bàn tay + ba ngón, mỗi ngón một xương của họ;
      # tay gần: r33, r34 SAU kiếm, r32 (lòng bàn tay), r31 TRƯỚC kiếm; tay xa: l34 (lòng bàn tay), l33 SAU kiếm, l32, l31 TRƯỚC kiếm
      "r32": "P_shouR3_2", "r31": "P_shouR3_1", "r33": "P_shouR3_3", "r34": "P_shouR3_4",
      "l34": "P_shouL3_4", "l31": "P_shouL3_1", "l32": "P_shouL3_2", "l33": "P_shouL3_3"}
# bàn tay hai mảnh: bên → (xương bàn tay, slot kiếm nó nắm, các slot bàn tay của họ (lấy tâm), ảnh bốn ngón, ảnh lòng bàn tay)
TAY2 = {}                     # bản bàn tay hai mảnh tự chế (tờ M_T): bỏ, người dùng trả "lỗi nặng"; nay dùng tám part tay của họ
NGON_KHOP, NGON_THO = 16.0, 30.0   # px concept: khớp ngón nhô khỏi mép kiếm phía cổ tay; đầu ngón thò khỏi mép kiếm bên kia
LONG_RONG, LONG_LECH = 1.0, 0.16  # lòng bàn tay: bề rộng so với hàng ngón; tâm lệch về phía cổ tay (× chiều cao lòng bàn tay)
# thứ tự vẽ sau → trước (theo thứ tự slot của họ; kp_* = mảnh theo khung part; *_n = lớp ngón tay phủ ra trước kiếm)
THU = ["duoi", "kp_gu", "kp_ao", "kp_lung", "ban_t", "dui_t", "ong_t", "ban_s", "dui_s", "ong_s", "kp_bung", "hong", "tua_x", "kp_khuyu_x", "kp_bap_x",
       "kp_than", "vay", "giap", "cang_x", "vai_x", "dai", "kp_l34", "kp_l33", "kp_r33", "kp_r34", "kp_l32", "kp_l31", "kp_co", "dau", "la_nho", "la_to", "mu", "kp_r32", "kp_r31",
       "kp_khuyu_g", "kp_bap_g", "cang_g", "tua_g1", "tua_g2", "tua_g3", "vai_g"]
# mảnh cứng → xương
XUONG = {"vai_g": "bone43", "vai_x": "bone45", "cang_x": "bone19", "ong_s": "Rh", "ong_t": "Lq", "mu": "bone6", "cang_g": "bone23",
         "ban_s": "Rh", "ban_t": "Lq", "dau": "bone7", "nam_g": "bone24", "nam_x": "bone20", "nam_g_n": "bone24", "nam_x_n": "bone20",
         "giap": "bone16", "dai": "bone3"}
DUI = {"dui_s": "Rh", "dui_t": "Lq"}        # đùi: đầu trên theo hông (bone3), đầu dưới theo đích chân
# mảnh mềm một trục của mình: tên → (xương cha, số đốt, độ cứng lò xo, giới hạn góc)
MEM = {"la_nho": ("bone6", 2, (300, 210), 12), "la_to": ("bone6", 2, (260, 180), 14),
       "tua_g1": ("bone43", 2, (170, 120), 34), "tua_g2": ("bone43", 2, (170, 120), 34), "tua_g3": ("bone43", 2, (170, 120), 34),
       "tua_x": ("bone45", 2, (170, 120), 34)}
# chuỗi dọc đường khớp đọc trên tờ mảnh (px concept): đuôi (gốc dưới → chóp cuộn), áo tơi (nút buộc → mép lá dưới trái), váy
DUOI_J = [(505, 465), (470, 350), (410, 240), (405, 140), (500, 68), (595, 150)]
AO_J = [(625, 560), (540, 680), (440, 800), (350, 930)]
VAY_TREN = 662                 # mép trên của váy sau khi kéo dài (px concept): nấp dưới đai thừng (đai ở y ≈ 640–690)
VAY_J = [(778, 672), (778, 810), (778, 945)]
# kiếm: slot của họ → (ảnh của mình, vẽ ngay TRƯỚC mảnh nào của mình trong thứ tự vẽ)
KIEM = [("W_daoB_3", "luoi_b"), ("W_daoB_6", "luoi_b"), ("W_daoB_2", "vo_b"), ("W_daoB_1", "chuoi_b"), ("W_daoB_5", "chuoi_b"),
        ("W_daoA_4", "luoi_a"), ("W_daoA_9", "luoi_a"), ("W_daoA_7", "luoi_a"), ("W_daoA_11", "chuoi_a"), ("W_daoA_6", "chuoi_a"),
        ("W_daoA_1", "vo_a"), ("W_daoA_12", "vo_a"), ("W_daoA_2", "chuoi_a")]
# CẢ nắm tay vẽ TRƯỚC kiếm (kiếm chui qua lòng nắm tay, ló ra hai bên). Bản hai lớp (cả nắm tay sau kiếm + nửa ngón tay trước kiếm)
# chỉ che nửa dưới vỏ kiếm: ở cỡ thật trông như vỏ kiếm nằm ĐÈ LÊN bàn tay (người dùng: "tay trái ôm kiếm bị lỗi nằm dưới kiếm")
KIEM_TRUOC = {"W_daoB_3": "dai", "W_daoB_6": "dai", "W_daoB_2": "dai", "W_daoB_1": "kp_l34", "W_daoB_5": "kp_l34", "W_daoA_4": "kp_l32",
              "W_daoA_9": "kp_l32", "W_daoA_7": "kp_l32", "W_daoA_11": "kp_l32", "W_daoA_6": "kp_l32", "W_daoA_1": "kp_l32",
              "W_daoA_12": "kp_l32", "W_daoA_2": "kp_l32"}   # lòng bàn tay SAU kiếm dài, bốn ngón TRƯỚC kiếm dài
ZERO5 = (0.0, 0.0, 0.0, 1.0, 1.0)


def mat_ho(b):
    return np.array([[b["a"], b["b"], b["x"]], [b["c"], b["d"], b["y"]], [0.0, 0.0, 1.0]])


W_I0 = {b["name"]: mat_ho(b) for b in A0["bones"]}       # thế giới khung 0 idle của họ
W_G = {b["name"]: mat_ho(b) for b in AG["bones"]}        # thế giới dáng gốc của họ


def truc_kiem(slot):
    """hai đầu trục dài (giữa mép trái ảnh → giữa mép phải ảnh) của hình kiếm trong slot của họ, thế giới khung 0 idle (đơn vị con gốc)."""
    a = next(q for q in AG["atts"] if q["slot"] == slot)
    P = np.array(a["xy"], float).reshape(-1, 2)          # BL, UL, UR, BR ở dáng gốc
    M = W_I0[a["bone"]] @ np.linalg.inv(W_G[a["bone"]])
    P = (M @ np.c_[P, np.ones(4)].T).T[:, :2]
    return (P[0] + P[1]) / 2, (P[2] + P[3]) / 2, float(np.hypot(*(P[1] - P[0]))), a["bone"]


def khop_khung(dat):
    """khung concept (px, y xuống) ↔ thế giới rig gốc (y lên): px = ox + s·X, py = oy − s·Y (bình phương tối thiểu trên các cặp NEO)."""
    by = {a["slot"]: a for a in A0["atts"] if a["cur"]}
    R, b = [], []
    for m, h in NEO:
        P = np.array(by[h]["xy"], float).reshape(-1, 2)
        X, Y = (P[:, 0].min() + P[:, 0].max()) / 2, (P[:, 1].min() + P[:, 1].max()) / 2
        Aff = np.array(dat[m]["A"], float)
        w, hh = dat[m]["co"]
        c = Aff @ np.array([w / 2, hh / 2, 1.0])
        R += [[X, 1, 0], [-Y, 0, 1]]
        b += [c[0], c[1]]
    for (cx, cy), xb in NEO_DIEM:
        X, Y = W_I0[xb][:2, 2]
        R += [[X, 1, 0], [-Y, 0, 1]]
        b += [cx, cy]
    (s, ox, oy), *_ = np.linalg.lstsq(np.array(R, float), np.array(b, float), rcond=None)
    lech = np.array(R) @ np.array([s, ox, oy]) - np.array(b)
    print(f"khớp khung concept: {s:.3f} px / đơn vị con gốc; lệch từng mốc (px): " +
          ", ".join(f"{m} {math.hypot(lech[2 * i], lech[2 * i + 1]):.0f}" for i, m in enumerate([q[0] for q in NEO] + [q[1] for q in NEO_DIEM])))
    return float(s), float(ox), float(oy)


def dung(nang=None):
    dat = json.load(open(os.path.join(KM.MANH, "dat.json"), encoding="utf-8"))
    dat.pop("_thu_tu")
    dat["hong"] = dict(dat["than"])              # khối hông + bụng lông (mảnh thân đặt theo concept): nối ngực với váy và hai chân
    # váy: kéo dài lên cho mép trên chui dưới đai thừng (bản lề ở đai). Trên concept mép trên của váy ở y = 795, cách đai ~100 px và nấp sau
    # hai bao tay; lúc tay giơ lên chém thì váy lộ ra như một vạt rời treo lửng (người dùng: "phần quần/váy chưa khớp lúc chém")
    (_, _, gx_), (_, _, gy_) = dat["vay"]["A"]
    hv_ = dat["vay"]["co"][1]
    dat["vay"]["A"] = [[1.0, 0.0, gx_], [0.0, (gy_ + hv_ - VAY_TREN) / hv_, float(VAY_TREN)]]
    thu_tu = list(THU)
    s, ox, oy = khop_khung(dat)
    tg = lambda p: np.stack([(np.asarray(p, float)[..., 0] - ox) / s, (oy - np.asarray(p, float)[..., 1]) / s], -1)   # noqa: E731
    px = lambda w: np.stack([ox + s * np.asarray(w, float)[..., 0], oy - s * np.asarray(w, float)[..., 1]], -1)      # noqa: E731

    sk = khung.Sk(TEN)
    sk.xuong("root")
    sk.xuong("move", "root")                     # game đo độ dời thân trên xương này (lao, nhảy)
    for i, b in enumerate(IB):
        if b["name"] in BO:
            continue
        cha = TENX[b["parent"]]
        x, y, r, sx, sy = B0[i]
        sk.xuong(b["name"], "move" if cha == "root" else cha, x * KG, y * KG + ((nang or 0.0) if cha == "root" else 0.0), goc=r,
                 dai=b["len"] * KG, sx=sx, sy=sy)
    sai = max(np.hypot(sk.W0[b["name"]][0, 2] / KG - b["x"], (sk.W0[b["name"]][1, 2] - (nang or 0.0)) / KG - b["y"]) for b in A0["bones"]
              if b["name"] not in BO)
    print(f"dáng gốc so khung 0 idle của họ: lệch lớn nhất {sai:.2f} đơn vị")
    goc_x = lambda b: (sk.W0[b][:2, 2] - np.array([0.0, nang or 0.0])) / KG       # gốc xương, đơn vị con gốc   # noqa: E731

    def diem_anh(t, uv):
        """điểm theo tỉ lệ khung ảnh của mảnh t → px concept."""
        Aff = np.array(dat[t]["A"], float)
        w, h = dat[t]["co"]
        return Aff @ np.array([uv[0] * w, uv[1] * h, 1.0])

    # kiếm: affine ảnh → px concept đưa trục ảnh (mép trái → mép phải) trùng trục kiếm của họ ở từng slot
    kiem = []
    for sl, a in KIEM:
        q0, q1, _, xb = truc_kiem(sl)
        if a.startswith("chuoi"):                # chuôi của mình có kiếm cách to ở đầu trái: lùi cả chuôi về phía miệng vỏ cho kiếm cách che
            q0, q1 = q0 - 0.08 * (q1 - q0), q1 - 0.08 * (q1 - q0)     # khe giữa miệng vỏ và chuôi (ở rig gốc do khâu kiếm W_dao*_5 che)
        w, h = dat[a]["co"]
        t = "k_" + sl[5:]
        dat[t] = dict(anh=a, co=[w, h], nhom="kiem",
                      A=KM.aff_hai_diem((KM.PAD, h / 2), (w - KM.PAD, h / 2), px(q0), px(q1)))
        XUONG[t] = xb
        kiem.append((t, sl))
    for a in KM.KIEM:
        dat.pop(a, None)

    # BÀN TAY HAI MẢNH kẹp thanh kiếm, như con gốc (tờ mổ <scan>/mo/tay_idle0_*.jpg): lòng bàn tay nằm SAU kiếm ở phía cổ tay; bốn ngón dài
    # vắt NGANG QUA cả thân kiếm ở phía TRƯỚC, khớp ngón ở phía cổ tay, đầu ngón thò sang bên kia. (Ba bản trước đều bị trả: nắm tay một cục
    # đặt cạnh kiếm; hai lớp cắt đôi nắm tay chỉ che nửa kiếm; cả nắm tay phủ lên kiếm: "phần bàn tay không ôm vào kiếm, bạn xem con gốc".)
    by0 = {a["slot"]: a for a in A0["atts"] if a["cur"]}
    anh_them = {}
    for ben, (xb, sl, ds, a_ngon, a_long) in TAY2.items():
        q0, q1, _, _ = truc_kiem(sl)
        P = np.concatenate([np.array(by0[q]["xy"], float).reshape(-1, 2) for q in ds])
        tam = (P.min(0) + P.max(0)) / 2
        u = (q1 - q0) / np.hypot(*(q1 - q0))
        T = q0 + u * float((tam - q0) @ u)       # chỗ nắm: điểm trên trục kiếm gần tâm bàn tay của họ nhất
        dk = dat["k_" + sl[5:]]
        Ak = np.array(dk["A"], float)
        pk_ = np.linalg.solve(Ak[:, :2], px(T) - Ak[:, 2])
        al = np.asarray(Image.open(os.path.join(KM.MANH, dk["anh"] + ".png")).convert("RGBA"))[..., 3]
        cot_ = al[:, int(np.clip(round(pk_[0]), 0, al.shape[1] - 1))] > 120
        pk_[1] = float(np.nonzero(cot_)[0].mean())                       # sống giữa thật của ảnh kiếm ở chỗ nắm
        day_px = float(cot_.sum()) * float(np.hypot(*Ak[:, 1]))          # bề dày kiếm ở chỗ nắm (px concept)
        T_px = Ak[:, :2] @ pk_ + Ak[:, 2]
        a_px = Ak[:, 0] / np.hypot(*Ak[:, 0])
        n_px = np.array([-a_px[1], a_px[0]])
        if (px(W_I0[xb][:2, 2]) - T_px) @ n_px < 0:                      # n_px chĩa về phía cổ tay (gốc xương bàn tay)
            n_px = -n_px
        g = math.atan2(-n_px[1], -n_px[0]) - math.pi / 2                 # ảnh +y (khớp ngón → đầu ngón) → −n_px (từ cổ tay sang bên kia kiếm)
        R_ = np.array([[math.cos(g), -math.sin(g)], [math.sin(g), math.cos(g)]])
        wn, hn = Image.open(os.path.join(KM.MANH, a_ngon + ".png")).size
        dai = day_px + NGON_KHOP + NGON_THO                               # ngón dài hơn bề dày kiếm: khớp nhô phía cổ tay, đầu ngón thò bên kia
        k = dai / (hn - 2 * KM.PAD)
        tam_ = T_px + n_px * (day_px / 2 + NGON_KHOP - dai / 2)
        tp = tam_ - k * (R_ @ np.array([wn / 2, hn / 2]))
        dat["ngon_" + ben] = dict(anh=a_ngon, co=[wn, hn], nhom="tay", A=[[float(k * R_[0, 0]), float(k * R_[0, 1]), float(tp[0])],
                                                                         [float(k * R_[1, 0]), float(k * R_[1, 1]), float(tp[1])]])
        wl, hl = Image.open(os.path.join(KM.MANH, a_long + ".png")).size
        kl = (wn - 2 * KM.PAD) * k * LONG_RONG / (wl - 2 * KM.PAD)       # lòng bàn tay rộng hơn hàng ngón một chút
        tam_ = T_px + n_px * (day_px / 2 + LONG_LECH * hl * kl)
        tp = tam_ - kl * (R_ @ np.array([wl / 2, hl / 2]))
        dat["long_" + ben] = dict(anh=a_long, co=[wl, hl], nhom="tay", A=[[float(kl * R_[0, 0]), float(kl * R_[0, 1]), float(tp[0])],
                                                                         [float(kl * R_[1, 0]), float(kl * R_[1, 1]), float(tp[1])]])
        XUONG["ngon_" + ben] = XUONG["long_" + ben] = xb
        if nang is not None:
            print(f"  bàn tay {ben}: kiếm dày {day_px:.0f} px ở chỗ nắm, ngón dài {dai:.0f} px (ảnh × {k:.2f}), lòng bàn tay ảnh × {kl:.2f}")

    # phép chỉnh từng mảnh (thế giới con gốc → thế giới con gốc)
    SUA, lin = {}, {}

    def chi(P0, P1, Q0, Q1):
        """mảnh chi đặt theo hai khớp P0 → Q0, P1 → Q1: xoay theo trục xương; CHỈ đoạn giữa hai khớp co giãn theo độ dài xương, phần ngoài
        hai khớp (hai đầu tròn) và bề ngang giữ nguyên cỡ."""
        dp, dq = P1 - P0, Q1 - Q0
        L, Lb = float(np.hypot(*dp)), float(np.hypot(*dq))
        up, uq = dp / L, dq / Lb
        np_, nq = np.array([-up[1], up[0]]), np.array([-uq[1], uq[0]])

        def f(w):
            w = np.asarray(w, float).reshape(-1, 2)
            s_ = (w - P0) @ up
            n_ = (w - P0) @ np_
            S_ = np.where(s_ < 0, s_, np.where(s_ <= L, s_ * Lb / L, Lb + (s_ - L)))
            return Q0 + S_[:, None] * uq + n_[:, None] * nq
        return f, Lb / L, math.degrees(math.atan2(dq[1], dq[0]) - math.atan2(dp[1], dp[0]))

    for t, (u0, u1, b0, b1) in HAI.items():
        f, k, a = chi(tg(diem_anh(t, u0)), tg(diem_anh(t, u1)), goc_x(b0), goc_x(b1))
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        SUA[t], lin[t] = f, np.array([[ca, -sa], [sa, ca]])
        d0 = np.hypot(*(tg(diem_anh(t, u0)) - goc_x(b0)))
        if nang is not None:
            print(f"  {t:8s} đoạn giữa co {k:.2f}  xoay {a:+6.1f}°  khớp gốc lệch trước khi chỉnh {d0:.0f}")
    for t, (u0, b0, theo) in MOT.items():
        R_ = lin[theo] if theo else np.eye(2)
        d_ = goc_x(b0) - R_ @ tg(diem_anh(t, u0))
        SUA[t] = (lambda w, R_=R_, d_=d_: (R_ @ np.asarray(w, float).reshape(-1, 2).T).T + d_)

    def the_gioi(t, pts_anh):
        """điểm ảnh (px ảnh gốc của mảnh) → thế giới rig mình."""
        Aff = np.array(dat[t]["A"], float)
        P = np.asarray(pts_anh, float).reshape(-1, 2)
        c = (Aff[:, :2] @ P.T).T + Aff[:, 2]
        w = tg(c)
        if t in SUA:
            w = SUA[t](w)
        return w * KG + np.array([0.0, nang or 0.0])

    def px_tg(p):
        """điểm concept (px) → thế giới rig mình."""
        return tg(np.array(p, float)) * KG + np.array([0.0, nang or 0.0])

    import kiem_si_part as KP_
    _, imgs_ho, _ = KS.nap()
    # xương của mình
    mem_ds = []
    for t, (cha, n, k, mx) in MEM.items():
        g, m = px_tg(dat[t]["goc"]), px_tg(dat[t]["ngon"])
        J = [g + (m - g) * q / n for q in range(n + 1)]
        ten = sk.chuoi("x_" + t + "_", cha, J)
        mem_ds.append(LoXo(ten, k=k, damp=0.5, maxang=mx))
    # đuôi bám cụm lưng trên (bone33, chỗ chùm lông P_shengzi_da1 của họ bám): gốc đuôi luôn nấp sau gù lưng / áo tơi. Bám hông (bản đầu)
    # thì lúc thân chúi xuống (chiêu cuối) các mảnh lưng dạt đi, gốc đuôi chìa ra lơ lửng (người dùng: "đuôi bị lỗi, hở to luôn")
    # (bản 3) bám bone33 vẫn hở: lúc rút hai kiếm, áo tơi (bone31) lật lên như cánh, gốc đuôi thò ra dưới mép áo tơi. Nay đuôi bám CHÍNH
    # xương áo tơi bone31: gốc đuôi nằm trong lòng mảng áo tơi (vẽ đè lên đuôi) ở mọi dáng, đuôi tung lên cùng áo tơi.
    duoi = sk.chuoi("x_duoi_", "bone31", [px_tg(p) for p in DUOI_J])
    a_ao = by0[KP["ao"]]
    M_ao, _ = KP_.aff_uv(a_ao)
    al_ao = np.asarray(Image.open(os.path.join(KM.MANH, "kp_ao.png")).convert("RGBA"))[..., 3]
    wr_, hr_ = imgs_ho[a_ao["region"]].size
    for q_, p_ in enumerate(DUOI_J[:3]):
        w_ = tg(np.array(p_, float))
        r_ = np.linalg.solve(M_ao[:, :2], w_ - M_ao[:, 2])
        u_, v_ = r_[0] / wr_, r_[1] / hr_
        trong = 0 <= u_ < 1 and 0 <= v_ < 1 and al_ao[int(v_ * al_ao.shape[0]), int(u_ * al_ao.shape[1])] > 120
        if nang is not None:
            print(f"  khớp đuôi {q_} ở ({u_:.2f}, {v_:.2f}) của khung áo tơi: {'TRONG' if trong else 'NGOÀI'} mảng áo tơi")
    ao = ["bone31"]                              # áo tơi lá = nửa cánh cứng P_keR của họ (xương bone31, đã có chuyển động của họ)
    vay = sk.chuoi("x_vay_", "bone3", [px_tg(p) for p in VAY_J])
    mem_ds += [LoXo(duoi, k=(340, 260, 200, 160, 130), damp=0.5, maxang=16), LoXo(vay, k=(240, 170), damp=0.5, maxang=20)]

    ti_anh = PXU / s                             # ảnh atlas = ảnh mảnh × ti_anh
    da_nap = set()

    def nap(a):
        if a not in da_nap:
            g = anh_them[a] if a in anh_them else Image.open(os.path.join(KM.MANH, a + ".png"))
            ti_ = ti_anh * (0.42 if a.startswith("tay_") else 1.0)       # mảnh bàn tay vẽ to gấp ~3 lần cỡ dùng: thu bớt cho nhẹ atlas
            im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(g.width * ti_)), max(2, round(g.height * ti_))), Image.LANCZOS).convert("RGBA"))
            sk.anh(a, im)
            da_nap.add(a)
        return sk.images[a]

    def gan(slot, t, cot, hang, ts, an=False, xuong_slot=None):
        """lưới ô cot × hang đỉnh phủ cả ảnh của mảnh t; ts(u, v, điểm thế giới) → {xương: w} (u, v ∈ [0, 1] theo ảnh)."""
        a = dat[t]["anh"]
        im = nap(a)
        w0, h0 = dat[t]["co"]
        L = LU.luoi_o(im.width, im.height, cot, hang)
        uv = np.asarray(L.pts, float) / np.array([im.width, im.height], float)
        V = the_gioi(t, uv * np.array([w0, h0], float))
        W = [ts(float(u), float(v), V[i]) for i, (u, v) in enumerate(uv)]
        b0 = xuong_slot or max(W[0], key=W[0].get)
        sk.slot(slot, b0, t, an=an)
        sk.luoi_gan(slot, a, L, W, the_gioi=V, ten=t)

    def muot(x):
        x = min(1.0, max(0.0, x))
        return x * x * (3 - 2 * x)

    def ts_chuoi(ten, J, cha=None, hoa=0.5):
        """trọng số theo vị trí chiếu lên đường khớp J (thế giới): mỗi đỉnh hoà hai đốt kề quanh khớp; trước khớp đầu thì hoà vào cha."""
        J = np.asarray(J, float)
        seg = np.hypot(*(J[1:] - J[:-1]).T)
        cum = np.r_[0.0, np.cumsum(seg)]

        def f(u, v, p):
            best, sb = 1e18, 0.0
            for i in range(len(J) - 1):
                d = J[i + 1] - J[i]
                q = float(np.clip((p - J[i]) @ d / (seg[i] ** 2), 0.0, 1.0))
                e = float(np.hypot(*(p - (J[i] + q * d))))
                if e < best:
                    best, sb = e, cum[i] + q * seg[i]
            i = int(np.clip(np.searchsorted(cum, sb, side="right") - 1, 0, len(ten) - 1))
            r = (sb - cum[i]) / seg[i]
            d_ = {}
            w_truoc = muot((hoa - r) / (2 * hoa)) if r < hoa else 0.0          # gần khớp đầu đốt: hoà với đốt trước
            w_sau = muot((r - (1 - hoa)) / (2 * hoa)) if r > 1 - hoa else 0.0  # gần khớp cuối đốt: hoà với đốt sau
            if i > 0 and w_truoc > 0:
                d_[ten[i - 1]] = w_truoc
            elif i == 0 and cha and w_truoc > 0:
                d_[cha] = w_truoc
            if i < len(ten) - 1 and w_sau > 0:
                d_[ten[i + 1]] = w_sau
            d_[ten[i]] = 1.0 - sum(d_.values())
            return d_
        return f

    def gan_khung(t):
        """mảnh vẽ đúng khung ảnh vùng của part họ: đặt bằng affine ảnh vùng → thế giới khung 0 idle của part đó; một xương thì ô cứng,
        nhiều xương thì lưới 5 × 5 lấy trọng số của các đỉnh lưới họ (nghịch đảo bình phương khoảng cách)."""
        a = by0[KP[t[3:]]]
        M, sai = KP_.aff_uv(a)
        wr, hr = imgs_ho[a["region"]].size
        g = Image.open(os.path.join(KM.MANH, t + ".png"))
        ti = float(np.hypot(*M[:, 0])) * PXU                                  # px atlas cho mỗi px ảnh vùng của họ
        im = anh.loang_mau(g.convert("RGBa").resize((max(2, round(wr * ti)), max(2, round(hr * ti))), Image.LANCZOS).convert("RGBA"))
        sk.anh(t, im)
        ws = a.get("w")
        ten_x = sorted({TENX[b] for v in ws for b, _ in v})
        n = 2 if len(ten_x) == 1 else 5
        L = LU.luoi_o(im.width, im.height, n, n)
        uv = np.asarray(L.pts, float) / np.array([im.width, im.height], float)
        Pr = uv * np.array([wr, hr], float)
        V = (np.c_[Pr, np.ones(len(Pr))] @ M.T) * KG + np.array([0.0, nang or 0.0])
        if n == 2:
            W = [{ten_x[0]: 1.0}] * 4
        else:
            uvh, _ = KS.luoi(a)
            W = []
            for p in Pr:
                d2 = ((uvh - p) ** 2).sum(1) + 4.0
                acc = {}
                for (v, k_) in zip(ws, 1.0 / d2 ** 2):
                    for b, ww in v:
                        acc[TENX[b]] = acc.get(TENX[b], 0.0) + ww * k_
                tong = sum(acc.values())
                W.append({b: v / tong for b, v in acc.items() if v / tong > 0.02})
                tong = sum(W[-1].values())
                W[-1] = {b: v / tong for b, v in W[-1].items()}
        sk.slot(t, ten_x[0], t)
        sk.luoi_gan(t, t, L, W, the_gioi=V, ten=t)
        if nang is not None:
            print(f"  {t:12s} khung part {KP[t[3:]]:12s} xương {ten_x}  affine lệch {sai:.1f}")

    sk.xuong("dat", "root")
    ds_slot = []
    kiem_theo = {}
    for t, sl in kiem:
        kiem_theo.setdefault(KIEM_TRUOC[sl], []).append((t, sl))
    cur_ho = {a["slot"]: a["cur"] for a in AG["atts"]}
    for t in thu_tu:
        for tk_, sl in kiem_theo.get(t, []):                                  # kiếm vẽ ngay trước mảnh này
            gan(tk_, tk_, 2, 2, lambda u, v, p, b=XUONG[tk_]: {b: 1.0}, an=not I["slots"][SLOT_HO.index(sl)]["att"])
            ds_slot.append(tk_)
        if t.startswith("kp_"):
            gan_khung(t)
        elif t == "hong":                        # nửa trên theo ngực, nửa dưới theo hông (váy và đùi nấp dưới mép nó)
            def ts_hong(u, v, p):
                q = muot((v - 0.30) / 0.35)
                return {"bone5": 1.0} if q <= 0 else ({"bone3": 1.0} if q >= 1 else {"bone5": 1 - q, "bone3": q})
            gan(t, t, 4, 7, ts_hong)
        elif t == "duoi":
            gan(t, t, 9, 12, ts_chuoi(duoi, [px_tg(p) for p in DUOI_J]))
        elif t == "vay":
            gan(t, t, 4, 6, ts_chuoi(vay, [px_tg(p) for p in VAY_J], cha="bone3"))
        elif t in DUI:
            def ts_dui(u, v, p, d=DUI[t]):
                q = muot((v - 0.3) / 0.4)
                return {"bone3": 1.0} if q <= 0 else ({d: 1.0} if q >= 1 else {"bone3": 1 - q, d: q})
            gan(t, t, 3, 6, ts_dui)
        elif t in MEM:
            n = MEM[t][1]
            ten = [f"x_{t}_{q}" for q in range(n)]
            g, m = px_tg(dat[t]["goc"]), px_tg(dat[t]["ngon"])
            gan(t, t, 3, 7, ts_chuoi(ten, [g + (m - g) * q / n for q in range(n + 1)]))
        else:
            o = 9 if t in HAI else 2             # mảnh chi: lưới 9 × 9 để theo được phép co riêng đoạn giữa
            gan(t, t, o, o, lambda u, v, p, b=XUONG[t]: {b: 1.0})
        ds_slot.append(t)
    del cur_ho

    if nang is None:                             # lượt đo: bàn chân của mình thấp hơn gốc rig bao nhiêu thì nâng cả con lên chừng ấy
        day = min(float(a_["V"][:, 1].min()) for sl_ in ("ban_s", "ban_t") for a_ in sk.atts[sl_].values())
        print(f"đáy bàn chân ở y = {day:.1f}: nâng cả con {-day:.1f}")
        return dung(nang=-day)
    # chiều cao game: đỉnh bát mũ (không tính núm tre, lá mào)
    w_mu, h_mu = dat["mu"]["co"]
    cao = float(the_gioi("mu", [[w_mu * 0.6, h_mu * 0.14]])[0][1])
    sk.xuong("far", "root", 0.9 * cao + 60.0, 0.45 * cao)                    # chỗ đối thủ (game dời tới tâm thân đối thủ)
    tk = sk.tom_tat()
    print(f"{tk['xuong']} xương, {tk['slot']} slot, {tk['dinh']} đỉnh; chiều cao game {cao:.0f}")
    return sk, dict(dat=dat, thu_tu=ds_slot, cao=cao, mem=mem_ds, kiem=kiem, duoi=duoi, ao=ao, vay=vay, nang=nang, px_tg=px_tg, the_gioi=the_gioi)


def ve_tinh(sk, info):
    """dáng gốc của rig cạnh concept đã duyệt (cùng cỡ) → rig/soi_tinh.png."""
    ve = soi.Ve(sk)
    P = khung.Pose()
    Bx = soi._union([ve.bao(P)], 0.04)
    C = Image.open(KM.DUYET).convert("RGB")
    sc = C.height / (Bx[3] - Bx[1]) * 0.86
    im = ve.ve(P, Bx, sc, bg=(255, 255, 255), ss=2).convert("RGB")
    out = Image.new("RGB", (C.width + im.width + 10, max(C.height, im.height)), (255, 255, 255))
    out.paste(C, (0, 0))
    out.paste(im, (C.width + 10, 0))
    os.makedirs(RA, exist_ok=True)
    pth = os.path.join(RA, "soi_tinh.png")
    out.save(pth)
    print(pth, out.size)


def ve_khung(sk, clips, ten, ts, sc=1.0, xuong=False):
    c = [x for x in clips if x.ten == ten][0]
    fr = hoat.nuong(sk, c)
    ve = soi.Ve(sk)
    Ps = [fr[min(len(fr) - 1, int(round(t * 30)))] for t in ts]
    Bx = soi._union([ve.bao(P) for P in Ps], 0.04)
    ims = []
    for P in Ps:
        im = ve.ve(P, Bx, sc, bg=(150, 150, 150), ss=2).convert("RGB")
        if xuong:
            W = sk.the_gioi(P)
            d = ImageDraw.Draw(im)
            x0, y0, x1, y1 = Bx
            for b in sk.bones:
                px_ = (W[b["name"]][0, 2] - x0) * sc
                py_ = (y1 - W[b["name"]][1, 2]) * sc
                d.ellipse([px_ - 3, py_ - 3, px_ + 3, py_ + 3], outline=(255, 0, 0), width=2)
        ims.append(im)
    cot = min(len(ims), 6)
    hang = (len(ims) + cot - 1) // cot
    out = Image.new("RGB", (ims[0].width * cot, ims[0].height * hang), (150, 150, 150))
    for i, im in enumerate(ims):
        out.paste(im, ((i % cot) * im.width, (i // cot) * im.height))
    os.makedirs(RA, exist_ok=True)
    pth = os.path.join(RA, f"soi_{ten}.png")
    out.save(pth)
    print(pth, out.size)


def main(a):
    sk, info = dung()
    if a and a[0] == "tinh":
        ve_tinh(sk, info)
        return
    import kiem_si_clip as KC
    clips, them = KC.lam_clip(sk, info)
    if a and a[0] == "soi":                    # soi <clip> <giây,giây,...> [tỉ lệ] [xuong]
        ve_khung(sk, clips, a[1], [float(x) for x in a[2].split(",")], float(a[3]) if len(a) > 3 else 1.0, "xuong" in a)
        return
    xuat.xuat_het(sk, clips, RA, TEN, TIEU_DE, dang=KS.K, so_dang=1, dung_yen=("skill",), lao=("cast",), far=("skill",), cao=info["cao"],
                  ma_goc=None, tol={"rotate": 0.05, "translate": 0.12, "scale": 0.001}, khop_idle=0.2, noi_them=them)


if __name__ == "__main__":
    main(sys.argv[1:])
