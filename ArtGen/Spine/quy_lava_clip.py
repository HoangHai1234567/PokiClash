# -*- coding: utf-8 -*-
"""Tiểu quỷ lava (quy_lava): clip. Nền là chuyển động lấy mẫu của con gốc monster_3336, phần riêng viết thêm.

Người dùng 2026-11-13:
  idle, run  gần giống con gốc, đổi chút; ngọn lửa trên đầu phải lay như lửa thật
  attack     tay cầm khiên ĐẬP KHIÊN vào người địch
  cast       CHĨA giáo vào đối thủ rồi bắn một tia lửa (tia là VFX: rig chỉ có xương `mieng` ở mũi giáo + sự kiện phun / het_phun)
  skill      chắp hai tay CẦM GIÁO BẰNG HAI TAY, NHẢY LÊN, GIỮ giáo trên không, rồi ĐÂM THẲNG XUỐNG đối thủ
  die        ngã quỵ xuống
  appear     nhảy vào màn chơi

Xương của họ (tên đã xáo): xem_0 gốc thân; xem_16 hông; xem_17, xem_18 thân trên; xem_11 đầu (xem_3 mắt, xem_2 miệng, tóc xem_27..35, bone,
bone2, xem_13, xem_14); tay gần xem_36 (vai) > xem_7 > xem_8 (găng tay) > xem_9, xem_10, xem_6 (ngón), xem_12 (giáo) > mieng (mũi giáo,
của mình); tay xa xem_37 > xem_25 > xem_23 > xem_20 (khiên), xem_41..43 (ngón); chân l_t / r_t (đích IK, đã nướng trong mẫu).
"""
import math

import numpy as np

from quai import hoat
from quai.hoat import Clip, LoXo
from quai.khung import goc_mat
import quy_lava_rig as R

KG, S, IB, BO, B0 = R.KG, R.S, R.IB, R.BO, R.B0
TAY_XA = ("xem_37", "xem_25", "xem_23", "xem_20", "xem_41", "xem_42", "xem_43")
CHAN = ("xem_15", "xem_24", "xem_26", "xem_19", "xem_21", "xem_22", "l_t", "r_t", "xem_38", "xem_39")   # hai chân + khối đá chân
TOC = ["xem_27", "xem_28", "xem_29", "xem_30", "xem_31", "xem_32", "xem_33", "xem_34", "xem_35", "bone", "bone2", "xem_13", "xem_14"]


def chuyen_dong():
    """{clip: (dài, {xương: mảng (số khung, 5) = lệch xoay độ, dời x, y (đơn vị rig mình), tỉ lệ x, y nhân})} so với dáng gốc của mình."""
    out = {}
    for clip, v in S.items():
        fr = [dict(l=R.rieng(F)) for F in v["frames"]]
        res = {}
        for i, b in enumerate(IB):
            if b["name"] in BO:
                continue
            x0, y0, r0, sx0, sy0 = B0[i]
            Am = np.array([[F["l"][i][2] - r0, (F["l"][i][0] - x0) * KG, (F["l"][i][1] - y0) * KG, F["l"][i][3] / (sx0 or 1.0),
                            F["l"][i][4] / (sy0 or 1.0)] for F in fr])
            Am[:, 0] = np.degrees(np.unwrap(np.radians(Am[:, 0])))
            Am[:, 0] -= 360.0 * round(Am[0, 0] / 360.0)
            if np.abs(Am - np.array([0, 0, 0, 1, 1])).max() > 1e-4:
                res[b["name"]] = Am
        out[clip] = (float(v["dur"]), res)
    return out


def em(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ra(x, k=2.2):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** k


def vao(x, k=2.2):
    x = min(1.0, max(0.0, x))
    return x ** k


def moc(t, ks):
    """đường khoá: ks = [(t, v[, kiểu])]; kiểu của khoá áp cho đoạn KẾT THÚC ở khoá đó: em (mặc định), ra, vao, thang."""
    if t <= ks[0][0]:
        return float(ks[0][1])
    for a, b in zip(ks, ks[1:]):
        if t <= b[0]:
            u = (t - a[0]) / max(1e-9, b[0] - a[0])
            kieu = b[2] if len(b) > 2 else "em"
            u = {"em": em, "ra": ra, "vao": vao, "thang": lambda q: q}[kieu](u)
            return float(a[1] + (b[1] - a[1]) * u)
    return float(ks[-1][1])


def rung(t, t0, t1, hz=11.0):
    if t < t0 or t > t1:
        return 0.0
    return math.sin(2 * math.pi * hz * (t - t0)) * min(1.0, (t - t0) / 0.12) * min(1.0, (t1 - t) / 0.12)


def lam_clip(sk, info):
    CD = chuyen_dong()
    cao = info["cao"]
    ds = list(info["thu_tu"])

    def nen(P, goc, tau, lap=False, w=1.0, bo=(), chi_lay=None):
        dur, Rr = CD[goc]
        x = (tau % dur if lap else min(max(tau, 0.0), dur)) * 30.0
        for b, arr in Rr.items():
            if b in bo or (chi_lay is not None and b not in chi_lay):
                continue
            n = len(arr)
            i0 = min(int(x), n - 1)
            i1 = min(i0 + 1, n - 1)
            f = x - i0
            v = arr[i0] * (1 - f) + arr[i1] * f
            if abs(v[0]) > 1e-4:
                P.rot(b, float(v[0]) * w)
            if abs(v[1]) > 1e-4 or abs(v[2]) > 1e-4:
                P.move(b, float(v[1]) * w, float(v[2]) * w)
            if abs(v[3] - 1) > 1e-5 or abs(v[4] - 1) > 1e-5:
                P.scale(b, 1 + (float(v[3]) - 1) * w, 1 + (float(v[4]) - 1) * w)

    def lua(P, t, manh=1.0, chu_ky=0.9):
        """ngọn lửa: các xương tóc của họ lay lệch pha nhanh như lửa liếm (cộng lên chuyển động nền)."""
        for k, b in enumerate(TOC):
            ph = k * 1.31
            P.rot(b, manh * (3.0 + 1.2 * (k % 3)) * (math.sin(2 * math.pi * t / chu_ky + ph) + 0.4 * math.sin(2 * math.pi * t / (chu_ky * 0.47) + 2 * ph)))
        for k, g in enumerate(("giot1", "giot2")):
            P.move(g, 0.0, manh * 0.02 * cao * math.sin(2 * math.pi * t / (chu_ky * 1.6) + k * 2.0))

    def mo_het(P, a, bo=()):
        for sl in ds:
            if sl not in bo:
                P.alpha[sl] = a * P.alpha.get(sl, 0.0 if sl in R.AN else 1.0)      # slot ẩn sẵn (mắt nhắm, sinh đôi) giữ ẩn

    def mat(P, nham):
        P.alpha["mat_g"] = P.alpha["mat_x"] = 0.0 if nham else 1.0
        P.alpha["mat_g_nham"] = P.alpha["mat_x_nham"] = 1.0 if nham else 0.0

    # ---------------------------------------------------------------- idle: idle_01 của họ (7 s) + lửa lay
    I_DUR = CD["idle_01"][0]

    def idle(t, P):
        nen(P, "idle_01", t, True)
        lua(P, t)
        nham = any(a <= t < a + 0.12 for a in (2.3, 5.6))
        mat(P, nham)

    W_DUR = 0.72 if R.QM.DANG == 2 else CD["run_01"][0]
    L26 = sk.bones[sk.bi["xem_26"]]["length"] or 10.0
    L22 = sk.bones[sk.bi["xem_22"]]["length"] or 10.0
    CHAN_G0 = (sk.W0["xem_26"] @ np.array([L26, 0.0, 1.0]))[:2]             # ngọn chân gần ở dáng gốc
    CHAN_X0 = (sk.W0["xem_22"] @ np.array([L22, 0.0, 1.0]))[:2]

    def buoc(P, dui, cang, L, goc0, pha, nhac, sai):
        """một chân: pha 0..1 trong chu kỳ; nửa đầu chân bước (nhấc cong, đưa từ sau ra trước), nửa sau chân trụ (đứng yên, trượt về sau)."""
        if pha < 0.5:
            u = pha / 0.5
            dx = sai * (-1 + 2 * em(u))
            dy = nhac * math.sin(math.pi * u)
        else:
            u = (pha - 0.5) / 0.5
            dx = sai * (1 - 2 * u)
            dy = 0.0
        W = sk.the_gioi(P)
        dich = goc0 + np.array([dx, dy]) + (W["move"][:2, 2] - sk.W0["move"][:2, 2])
        hoat.ik_hai_doan(sk, P, dui, cang, dich, ngon=(L, 0.0))

    def walk(t, P):
        if R.QM.DANG != 2:
            nen(P, "run_01", t, True)
            lua(P, t, 1.3, 0.6)
            mat(P, False)
            return
        # dạng 2: bước dậm nặng (run_01 lon ton của con gốc hợp con bóng nhỏ, dạng 2 nhìn xấu): nhún mỗi lần chân chạm đất, thân trên lắc
        # nhẹ, đầu bù ngược, găng / giáo / khiên đung đưa trễ, chân luân phiên nhấc (giải hai khúc chân)
        nen(P, "idle_01", 0.0)
        ph = (t / W_DUR) % 1.0
        nhun = 0.5 + 0.5 * math.cos(4 * math.pi * ph)                       # 1 lúc chạm đất (pha 0 và 0,5), 0 giữa bước
        lac = math.sin(2 * math.pi * ph)
        P.move("xem_16", 0.0, -0.035 * cao * nhun + 0.012 * cao * (1 - nhun))
        P.scale("xem_0", 1 + 0.025 * nhun, 1 - 0.03 * nhun)
        P.rot("xem_18", 3.5 * lac)
        P.rot("xem_11", -2.5 * lac + 1.5 * nhun)
        P.rot("xem_7", 6.0 * math.sin(2 * math.pi * ph - 0.6))
        P.rot("xem_12", -4.0 * math.sin(2 * math.pi * ph - 0.9))
        P.rot("xem_25", -5.0 * math.sin(2 * math.pi * ph - 0.6))
        P.rot("xem_20", 3.0 * math.sin(2 * math.pi * ph - 1.0))
        buoc(P, "xem_24", "xem_26", L26, CHAN_G0, ph, 0.10 * cao, 0.07 * cao)
        buoc(P, "xem_21", "xem_22", L22, CHAN_X0, (ph + 0.5) % 1.0, 0.10 * cao, 0.07 * cao)
        lua(P, t, 1.4, 0.55)
        mat(P, False)

    def hit(t, P):
        nen(P, "hit_01", t)
        lua(P, t, 1.5, 0.5)
        mat(P, 0.04 < t < 0.3)

    # ---------------------------------------------------------------- attack: ĐẬP KHIÊN (tay xa)
    # cổ tay xa (ngọn xương xem_23) đi theo đích tính trong hệ THÂN TRÊN (xem_18) ở dáng gốc, giải hai khúc tay; khiên (xem_20) giữ góc
    # thế giới gần thẳng đứng, ngả ra sau lúc lấy đà, chúi tới lúc đập.
    W0 = sk.W0
    T18 = np.linalg.inv(W0["xem_18"])
    L23 = sk.bones[sk.bi["xem_23"]]["length"]
    CO_TAY = (W0["xem_23"] @ np.array([L23, 0.0, 1.0]))[:2]                # cổ tay xa ở dáng gốc (thế giới)
    G_KHIEN = goc_mat(W0["xem_20"])

    def tay_xa(P, dlech, goc_khien_lech=0.0, w=1.0):
        """đặt cổ tay xa ở (dáng gốc + dlech) theo thân trên, w trộn với dáng đang có; khiên giữ góc thế giới (gốc + lệch)."""
        if w <= 1e-4:
            return
        W = sk.the_gioi(P)
        dich_g = T18 @ np.r_[CO_TAY + np.asarray(dlech, float), 1.0]
        dich = (W["xem_18"] @ dich_g)[:2]
        hien = (W["xem_23"] @ np.array([L23, 0.0, 1.0]))[:2]
        hoat.ik_hai_doan(sk, P, "xem_25", "xem_23", hien + (dich - hien) * w)
        W = sk.the_gioi(P)
        cur = goc_mat(W["xem_20"])
        muon = G_KHIEN + goc_khien_lech
        d = ((muon - cur + 180.0) % 360.0) - 180.0
        P.rot("xem_20", d * w)

    D2 = R.QM.DANG == 2                                                   # dạng 2: cùng kiểu chiêu, mạnh hơn (người dùng 2026-11-13)
    A_DUR, A_TRUNG = (1.3, 0.40) if D2 else (1.0, 0.40)
    A_TRUNG2 = 0.74                                                       # dạng 2: nhát đập khiên thứ hai
    A_XA = 0.50 * cao
    if D2:
        LUI_K = [(0, 0), (0.28, 1), (0.37, 0.2, "vao"), (0.40, 0), (0.52, 0), (0.62, 0.7), (0.71, 0.15, "vao"), (0.74, 0)]
        DAP_K = [(0.28, 0), (0.40, 1, "vao"), (0.50, 0.85), (0.60, 0.25), (0.74, 1, "vao"), (0.90, 0.92), (1.14, 0)]
        MOV_K = [(0, 0), (0.28, -0.05 * cao), (0.40, A_XA, "vao"), (0.56, 0.92 * A_XA), (0.74, 1.08 * A_XA, "vao"), (0.92, 1.08 * A_XA),
                 (A_DUR - 0.04, 0)]
    else:
        LUI_K = [(0, 0), (0.28, 1), (A_TRUNG - 0.03, 0.2, "vao"), (A_TRUNG, 0)]
        DAP_K = [(0.28, 0), (A_TRUNG, 1, "vao"), (A_TRUNG + 0.16, 0.92), (0.84, 0)]
        MOV_K = [(0, 0), (0.28, -0.05 * cao), (A_TRUNG, A_XA, "vao"), (A_TRUNG + 0.18, A_XA), (A_DUR - 0.04, 0)]

    def attack(t, P):
        nen(P, "idle_01", t, True)
        lui = moc(t, LUI_K)                                                   # lấy đà: ngả ra sau, khiên kéo sát người
        dap = moc(t, DAP_K)                                                   # đẩy khiên thẳng tới (dạng 2: hai nhát)
        P.move("move", moc(t, MOV_K), 0.0)
        P.rot("xem_18", 9.0 * lui - 9.0 * dap)
        P.rot("xem_11", -5.0 * lui + 4.0 * dap)
        P.move("xem_16", 0.0, -0.035 * cao * lui)
        P.scale("xem_0", 1 + 0.06 * dap - 0.04 * lui, 1 - 0.05 * dap + 0.04 * lui)
        P.rot("xem_7", 12.0 * lui - 6.0 * dap)                                # tay gần vung ngược nhẹ
        lua(P, t, 1.0 + 1.2 * dap, 0.55)
        tay_xa(P, (-0.10 * cao * lui + 0.30 * cao * dap, 0.03 * cao * lui - 0.03 * cao * dap), 10.0 * lui - 8.0 * dap, max(lui, dap))
        mat(P, False)

    # ---------------------------------------------------------------- cast: CHĨA giáo vào đối thủ, bắn tia lửa
    # dáng chĩa giáo của skill_01 (0,24 s); mũi giáo (xương mieng) ghìm về góc thế giới C_GOC trong lúc giữ để tia bắn vào đối thủ
    C_CHIA, C_PHUN, C_HET, C_DUR = (0.34, 0.50, 1.85, 2.25) if D2 else (0.34, 0.50, 1.45, 1.85)   # dạng 2: luồng lửa giữ lâu hơn
    C_GOC = 18.0

    def cast(t, P):
        tau = moc(t, [(0, 0), (C_CHIA, 0.24, "thang"), (C_HET, 0.27, "thang"), (C_DUR, 0.0)])
        w = moc(t, [(0, 0), (0.15, 1), (C_HET + 0.05, 1), (C_DUR - 0.05, 0)])
        nen(P, "idle_01", t, True)
        nen(P, "skill_01", tau, w=w, bo=("move",) + TAY_XA + CHAN)              # tay khiên giữ dáng idle (người dùng: không đề tay khiên ra sau)
        giat = moc(t, [(C_PHUN - 0.02, 0), (C_PHUN + 0.06, 1, "ra"), (C_PHUN + 0.3, 0.35), (C_HET, 0.35), (C_HET + 0.2, 0)])
        P.move("xem_0", -0.05 * cao * giat, 0.0)
        ngam = moc(t, [(0.12, 0), (C_CHIA, 1), (C_HET, 1), (C_DUR - 0.1, 0)])
        if ngam > 1e-4:
            W = sk.the_gioi(P)
            d = ((C_GOC - goc_mat(W["mieng"]) + 180.0) % 360.0) - 180.0
            P.rot("xem_8", d * ngam)
        r = rung(t, C_PHUN, C_HET, 13.0) * 0.8
        P.rot("xem_8", r)
        lua(P, t, 1.0 + 1.2 * giat, 0.55)
        mat(P, False)

    # ---------------------------------------------------------------- skill: cầm giáo hai tay, nhảy lên, giữ trên không, đâm thẳng xuống
    # Điều khiển theo VỊ TRÍ trong hệ thân trên (xem_18, dáng gốc): điểm nắm của găng tay (gốc xương giáo xem_12) đi theo NAM_*, giải hai
    # khúc tay gần (xem_7, xem_8) tới đó; giáo giữ góc thế giới GOC_* (mũi chúc xuống); nắm tay xa giải hai khúc (xem_25, xem_23) cho tâm
    # nắm tay đặt lên cán ngay trên tay gần; bản sinh đôi nam_x2 (vẽ trước giáo) thay nam_x lúc nắm. Game xoay + co quỹ đạo cho khung dời xa
    # nhất trỏ vào đối thủ → khung đâm trúng phải dời xa nhất (đỉnh nhảy gần hơn).
    K_GOM, K_BAT, K_DINH, K_DAM, K_TRUNG, K_DUR = 0.36, 0.46, 0.82, 1.30, 1.44, 2.30
    # khung TRÚNG phải dời xa nhất (game xoay + co quỹ đạo cho khung dời xa nhất trỏ vào đối thủ): x lúc trúng > độ dời lúc giữ trên không
    K_XA = (2.2 if D2 else 1.9) * cao
    K_CAO = 1.2 if D2 else 1.02                                            # độ cao lúc giữ trên không (dạng 2 nhảy cao hơn)
    GRIP0 = W0["xem_12"][:2, 2].copy()
    NGON8 = tuple((np.linalg.inv(W0["xem_8"]) @ np.r_[GRIP0, 1.0])[:2])
    NAMX = np.mean([np.asarray(a_["V"]).mean(0) for a_ in sk.atts["nam_x"].values()], 0)
    NGON23 = tuple((np.linalg.inv(W0["xem_23"]) @ np.r_[NAMX, 1.0])[:2])
    G_GIAO = goc_mat(W0["mieng"])                                          # góc mũi giáo ở dáng gốc (≈ −37°)
    # người dùng: "đẩy giáo ra giữa hơn, layer nằm trên body nhưng nằm dưới bàn tay, 2 tay đều phải đưa ra phía trước": trục giáo ở x ≈ 15
    # (giữa hai mắt, x −19 và +65); tay gần (tầm với ~111 từ vai x −93) vươn ngang ra giữa; tay xa kéo dài thêm DAI_X và vẽ trước thân
    # nắm ngang BỤNG (găng tay không che mặt), phiến đá chạy giữa hai mắt; hai tay dài thêm (dời khuỷu dọc bắp tay) để với ra giữa
    NAM_GOM, GOC_GOM = np.array([20.0, 110.0]), -40.0                      # gom tay: hai nắm tay trước bụng, mũi chúc chéo xuống trước
    NAM_TREN, GOC_TREN = np.array([25.0, 96.0]), -90.0                    # trên không: giáo dựng giữa người, mũi thẳng xuống
    NAM_DAM, GOC_DAM = np.array([25.0, 82.0]), -90.0                      # đâm: hai tay dồn xuống, mũi cắm xuống
    DAI_X = 0.09 * cao                                                     # tay xa dài thêm
    DAI_G = 40.0                                                           # tay gần dài thêm (bắp tay bap_g giãn theo)
    XA_TREN = np.array([0.0, 0.0])                                         # nắm tay xa so với chỗ nắm của găng: (dọc cán về đuôi, lệch ra ngoài)
    if D2:
        # người dùng vẽ (2026-11-13): giáo dọc phía BÊN PHẢI thân (giữa tâm và mép phải), tay phải (tay xa) nắm cán phía ngoài bên phải ngang
        # ngực, tay trái (găng) vòng qua bụng nắm cán ngay dưới
        NAM_GOM, GOC_GOM = np.array([78.0, 125.0]), -40.0
        NAM_TREN, GOC_TREN = np.array([85.0, 129.0]), -90.0
        NAM_DAM, GOC_DAM = np.array([85.0, 113.0]), -90.0
        DAI_G = 100.0                                                       # tay trái vòng qua cả bụng
        # nắm tay xa của dạng 2 nằm NGAY Ở KHUỶU (concept vẽ vậy): tay xa chỉ với được một vòng bán kính ≈ bắp tay quanh vai; gần hơn là bộ
        # giải nhảy nghiệm. Rút bắp tay còn ~71 và đặt nắm tay phải ôm cán phía ngoài, ngay dưới-phải tay trái, đúng trong tầm.
        XA_TREN = np.array([0.13, 0.05])                                    # tay phải nắm cán TRÊN găng, lệch ra ngoài (như hình người dùng vẽ)
        DAI_X = -15.0
    NANG_LECH = np.array([0.0, float(info["nang"]) - 11.9])                # dạng 2 nâng cả con cao hơn dạng 1: các điểm nắm viết theo dạng 1
    NAM_GOM, NAM_TREN, NAM_DAM = NAM_GOM + NANG_LECH, NAM_TREN + NANG_LECH, NAM_DAM + NANG_LECH

    def uon0(dui, cang, ngon):
        """chiều gập khuỷu ở dáng gốc (giữ cố định: bộ giải tự chọn theo dáng đang có thì khuỷu lật qua lại giữa các khung)."""
        A, B = W0[dui][:2, 2], W0[cang][:2, 2]
        C = (W0[cang] @ np.r_[ngon, 1.0])[:2]
        cr = (C - A)[0] * (B - A)[1] - (C - A)[1] * (B - A)[0]
        return 1.0 if cr >= 0 else -1.0
    UON_G = uon0("xem_7", "xem_8", NGON8)
    VAI_G = W0["xem_36"][:2, 2].copy()                                      # vai gần ở dáng gốc
    UON_X = uon0("xem_25", "xem_23", NGON23)
    G_CANG_X = goc_mat(W0["xem_23"])                                        # góc thế giới cẳng tay xa ở dáng gốc

    def ep_goc(P, xuong, xem, muon):
        """xoay xương `xuong` cho góc thế giới của xương `xem` bằng `muon` (góc muốn phải liên tục theo thời gian)."""
        W = sk.the_gioi(P)
        cha = sk.bones[sk.bi[xuong]]["parent"]
        dau = 1.0 if np.linalg.det(W[cha][:2, :2]) > 0 else -1.0
        d = ((muon - goc_mat(W[xem]) + 180.0) % 360.0) - 180.0
        P.rot(xuong, dau * d)

    VAI_HA_G = np.array([14.0, -52.0])                                     # dời vai gần xuống hông trái (thế giới, dáng gốc)
    VAI_HA_X = np.array([0.0, 0.0]) if D2 else np.array([16.0, -44.0])  # dời vai xa xuống hông phải (dạng 2: tay phải nắm cao ngang ngực)

    def doi_tg(P, xuong, d):
        """dời xương một vectơ THẾ GIỚI d (đổi sang hệ cha)."""
        W = sk.the_gioi(P)
        cha = sk.bones[sk.bi[xuong]]["parent"]
        l = np.linalg.solve(W[cha][:2, :2], np.asarray(d, float))
        P.move(xuong, float(l[0]), float(l[1]))

    GRIP_XUONG = ("xem_36", "xem_37", "xem_7", "xem_8", "xem_12", "xem_25", "xem_23", "xem_20")

    GRIP_NHO = {}

    def grip(P, nam, goc, w, t=None):
        """dáng cầm giáo hai tay, trộn với dáng nền theo w: giải TRỌN dáng cầm (grip_day, w = 1) trên bản sao rồi trộn từng xương (dời, tỉ lệ
        nội suy; góc lệch × w). Giải với đích trượt dần thì khuỷu lật chiều giữa chừng (cẳng tay xa quay ~200° trong 4 khung lúc rút tay về);
        trộn góc thì đường đi liền. Góc lệch giữ LIÊN TỤC theo thời gian (t tăng dần khi nướng): lệch gần nửa vòng thì "đường ngắn nhất" đổi
        chiều giữa hai khung, nên chọn bản ±360° gần khung trước nhất."""
        if t is not None and t < GRIP_NHO.get("_t", -1.0):
            GRIP_NHO.clear()
        if t is not None:
            GRIP_NHO["_t"] = t
        if w <= 1e-4:
            return
        P1 = P.copy()
        grip_day(P1, nam, goc, 1.0)
        for b in GRIP_XUONG:
            g0 = P.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            g1 = P1.t.get(b, [0.0, 0.0, 0.0, 1.0, 1.0])
            dr = ((g1[2] - g0[2] + 180.0) % 360.0) - 180.0
            if t is not None:
                if b in GRIP_NHO:
                    dr += 360.0 * round((GRIP_NHO[b] - dr) / 360.0)
                GRIP_NHO[b] = dr
            P.t[b] = [g0[0] + (g1[0] - g0[0]) * w, g0[1] + (g1[1] - g0[1]) * w, g0[2] + dr * w,
                      g0[3] + (g1[3] - g0[3]) * w, g0[4] + (g1[4] - g0[4]) * w]

    def grip_day(P, nam, goc, w):
        """đặt điểm nắm (hệ thân trên dáng gốc), giáo theo góc thế giới goc, tay xa nắm cán dưới tay gần (gọi với w = 1)."""
        doi_tg(P, "xem_36", VAI_HA_G * w)                                   # hai vai xuống hai bên hông: tay không vắt qua mặt
        doi_tg(P, "xem_37", VAI_HA_X * w)
        W = sk.the_gioi(P)
        # điểm nắm đi theo CUNG quanh vai (góc + bán kính nội suy, quay ngược kim qua phía trước): đường thẳng từ dưới lên đầu sượt sát vai
        # làm tay gập hết cỡ và găng tay xoay vụt >100° trong một khung
        vai = VAI_G + VAI_HA_G * w
        q0, q1 = GRIP0 - vai, np.asarray(nam, float) - vai
        a0, a1 = math.atan2(q0[1], q0[0]), math.atan2(q1[1], q1[0])
        if a1 < a0:
            a1 += 2 * math.pi
        r_ = np.hypot(*q0) + (np.hypot(*q1) - np.hypot(*q0)) * w
        a_ = a0 + (a1 - a0) * w
        p_ = vai + r_ * np.array([math.cos(a_), math.sin(a_)])
        dich = (W["xem_18"] @ (T18 @ np.r_[p_, 1.0]))[:2]
        P.move("xem_8", DAI_G * w, 0.0)                                      # tay gần dài thêm (găng cứng, bắp tay giãn)
        hoat.ik_hai_doan(sk, P, "xem_7", "xem_8", dich, ngon=NGON8, uon=UON_G)
        g_ = G_GIAO + (goc - G_GIAO) * w                                     # góc giáo nội suy LIÊN TỤC rồi ép đúng
        ep_goc(P, "xem_12", "mieng", g_)
        W = sk.the_gioi(P)
        g = W["xem_12"][:2, 2]
        u = np.array([math.cos(math.radians(g_)), math.sin(math.radians(g_))])
        if D2:                                                               # tay xa nắm TRÊN găng, lệch ra ngoài bên phải cán
            dich2 = g - u * XA_TREN[0] * cao + np.array([-u[1], u[0]]) * (XA_TREN[1] * cao)
        else:
            dich2 = g + u * 0.30 * cao                                       # nắm tay xa: ngay dưới tay gần, dọc cán về phía mũi giáo
        if D2:
            # nắm tay xa của dạng 2 nằm sát khuỷu: tầm với là một vành rất hẹp quanh vai, giải hai khúc chạm biên là nhảy nghiệm. Thay bằng: bắp
            # tay chĩa thẳng vào điểm nắm + co giãn đúng độ dài (dời khuỷu dọc trục bắp tay); cẳng tay (nắm tay) giữ góc thế giới như lúc đứng
            W = sk.the_gioi(P)
            A_ = W["xem_25"][:2, 2]
            v_ = dich2 - A_
            ep_goc(P, "xem_25", "xem_25", math.degrees(math.atan2(v_[1], v_[0])))
            W = sk.the_gioi(P)
            truc = W["xem_25"][:2, 0]
            ti = float(np.hypot(*truc))
            P.move("xem_23", (float(np.hypot(*v_)) - float(np.hypot(*(W["xem_23"][:2, 2] - A_)))) / max(1e-6, ti), 0.0)
            ep_goc(P, "xem_23", "xem_23", G_CANG_X)
        else:
            P.move("xem_23", DAI_X * w, 0.0)                                 # tay xa dài hơn chút
            W = sk.the_gioi(P)
            hien2 = (W["xem_23"] @ np.r_[NGON23, 1.0])[:2]
            hoat.ik_hai_doan(sk, P, "xem_25", "xem_23", hien2 + (dich2 - hien2) * w, ngon=NGON23, uon=UON_X)
        ep_goc(P, "xem_20", "xem_20", G_KHIEN - 15.0 * w)

    def skill(t, P):
        nen(P, "idle_01", t, True)
        x = moc(t, [(K_GOM, -0.04 * cao), (K_DINH, 0.70 * K_XA, "ra"), (K_DAM, 0.80 * K_XA), (K_TRUNG, K_XA, "vao"), (K_TRUNG + 0.32, K_XA),
                    (K_DUR - 0.05, 0)])
        y = moc(t, [(K_GOM - 0.1, 0.0), (K_GOM, -0.07 * cao), (K_BAT, 0.20 * cao, "ra"), (K_DINH, (K_CAO - 0.07) * cao, "ra"), (K_DAM - 0.04, K_CAO * cao),
                    (K_TRUNG, 0.0, "vao"), (K_TRUNG + 0.32, 0.0), (K_TRUNG + 0.55, 0.22 * cao, "ra"), (K_DUR - 0.12, 0.0, "vao")])
        P.move("move", x, y)
        P.move("move", 0.0, 0.015 * cao * math.sin(2 * math.pi * (t - K_DINH) / 0.24) * moc(t, [(K_DINH, 0), (K_DINH + 0.1, 1), (K_DAM - 0.05, 1), (K_DAM, 0)]))
        nhun = moc(t, [(0.1, 0), (K_GOM, 1), (K_BAT, 0, "ra"), (K_TRUNG - 0.02, 0), (K_TRUNG + 0.06, 1, "ra"), (K_TRUNG + 0.32, 0.5), (K_TRUNG + 0.5, 0)])
        P.move("xem_16", 0.0, -0.05 * cao * nhun)
        P.scale("xem_0", 1 + 0.08 * nhun, 1 - 0.08 * nhun)
        uon = moc(t, [(K_BAT, 0), (K_DINH, 1), (K_DAM, 1.1), (K_TRUNG, -0.8, "vao"), (K_TRUNG + 0.3, -0.6), (K_DUR - 0.3, 0)])   # ngửa / gập
        P.rot("xem_18", 7.0 * uon)
        P.rot("xem_11", -3.0 * uon)
        # điểm nắm + góc giáo theo pha
        if t < K_GOM:
            u_ = em(t / K_GOM)
            nam, goc = NAM_GOM, GOC_GOM
            w = u_
        elif t < K_DINH:
            u_ = em((t - K_GOM) / (K_DINH - K_GOM))
            nam, goc, w = NAM_GOM + (NAM_TREN - NAM_GOM) * u_, GOC_GOM + (GOC_TREN - GOC_GOM) * u_, 1.0
        elif t < K_DAM:
            nam, goc, w = NAM_TREN + np.array([0.0, 0.02 * cao * math.sin(2 * math.pi * (t - K_DINH) / 0.24)]), GOC_TREN, 1.0
        elif t < K_TRUNG:
            u_ = vao((t - K_DAM) / (K_TRUNG - K_DAM), 1.6)
            nam, goc, w = NAM_TREN + (NAM_DAM - NAM_TREN) * u_, GOC_DAM, 1.0
        else:
            nam, goc = NAM_DAM, GOC_DAM
            w = moc(t, [(K_TRUNG + 0.32, 1), (K_TRUNG + (0.52 if D2 else 0.32 + (K_DUR - 0.08 - K_TRUNG - 0.32)), 0)])   # dạng 2: rút tay nhanh (khối vẽ sẵn tắt ở K_TRUNG + 0.32)
        grip(P, nam, goc, w, t)
        cam = w > 0.5
        for a_, b_ in (("nam_x", "nam_x2"), ("tay_x", "tay_x2")):          # tay xa + nắm tay xa lên trước thân và giáo lúc cầm giáo hai tay
            P.alpha[a_] = 0.0 if cam else 1.0
            P.alpha[b_] = 1.0 if cam else 0.0
        P.alpha["khien"] = 1.0 - moc(w, [(0.35, 0), (0.6, 1)])
        if D2 and "cam" in sk.si:                                           # dạng 2: đổi sang khối hai tay + giáo vẽ sẵn (bật nhảy → nhảy lùi về)
            doi = 0.28 <= t < K_TRUNG + 0.32                                 # đổi ảnh giữa lúc nhún lấy đà và lúc nhảy lùi về (khung nhanh)
            P.alpha["cam"] = 1.0 if doi else 0.0
            if doi:
                for sl in ("gang", "dot_g", "vai_g", "bap_g", "tay_x", "tay_x2", "nam_x", "nam_x2", "giao", "giao_mui", "khien"):
                    P.alpha[sl] = 0.0              # khiên đeo sau lưng lúc cầm giáo hai tay (mũi khiên thò dưới bụng)
        lua(P, t, 1.4, 0.5)
        mat(P, False)

    # ---------------------------------------------------------------- die: NGÃ QUỴ: khuỵu gối, gục, đổ sấp về trước, lửa tàn, mờ
    D_DUR = 1.9

    def die(t, P):
        nen(P, "idle_01", 0.0)
        giat = moc(t, [(0.0, 0), (0.06, 1, "ra"), (0.22, 0)])                 # giật mình lúc trúng đòn chí mạng
        quy = moc(t, [(0.12, 0), (0.42, 1, "vao"), (0.52, 0.9), (0.62, 1)])   # khuỵu gối (thân sụp xuống, lắc nảy)
        do = moc(t, [(0.72, 0), (1.05, 1, "vao"), (1.13, 0.94), (1.22, 1)])   # đổ sấp về phía trước, nảy nhẹ khi chạm đất
        P.move("xem_0", -0.03 * cao * giat, 0.0)
        P.move("xem_16", 0.0, -0.16 * cao * quy)
        P.scale("xem_0", 1 + 0.06 * quy * (1 - do), 1 - 0.07 * quy * (1 - do))
        P.rot("xem_0", -72.0 * do)                                             # lăn về trước quanh chân
        P.move("xem_0", 0.10 * cao * do, -0.06 * cao * do)
        P.rot("xem_18", 6.0 * giat - 12.0 * quy)
        P.rot("xem_11", 10.0 * giat - 16.0 * quy - 6.0 * do)
        P.rot("xem_7", 18.0 * quy + 25.0 * do)                                 # tay gần rũ, giáo chúc xuống
        P.rot("xem_12", -22.0 * quy)
        P.rot("xem_25", -25.0 * quy - 10.0 * do)                               # tay xa rũ, khiên trễ xuống
        P.rot("xem_20", 12.0 * quy)
        if do > 1e-4:                                                         # giáo đổ nằm trên đất trước mặt khi thân đổ
            W = sk.the_gioi(P)
            dg = ((-6.0 - goc_mat(W["mieng"]) + 180.0) % 360.0) - 180.0
            P.rot("xem_12", dg * do)
        tat = moc(t, [(0.15, 0), (1.25, 1)])
        lua(P, t, max(0.0, 1.0 - tat), 0.7)
        for b in TOC:
            P.scale(b, 1 - 0.6 * tat, 1 - 0.6 * tat)
        for g in ("giot1", "giot2"):
            P.alpha[g] = max(0.0, 1.0 - 2.5 * tat)
        mat(P, t > 0.06)
        mo_het(P, float(np.clip(1.0 - (t - 1.45) / 0.4, 0.0, 1.0)))

    # ---------------------------------------------------------------- appear: nhảy vào từ phía sau
    P_DUR, P_DAP = 1.3, 0.42

    def appear(t, P):
        nen(P, "idle_01", 0.0)
        x = moc(t, [(0, -1.1 * cao), (P_DAP, 0.0, "thang")])
        y = moc(t, [(0, 0.5 * cao), (0.16, 0.75 * cao, "ra"), (P_DAP, 0.0, "vao")])
        P.move("move", x, y)
        thup = moc(t, [(P_DAP - 0.02, 0), (P_DAP + 0.07, 1, "ra"), (0.7, 0.6), (1.0, 0)])
        co = moc(t, [(0, 1), (P_DAP - 0.05, 0.6), (P_DAP + 0.04, 0)])
        P.move("xem_16", 0.0, -0.10 * cao * thup)
        P.scale("xem_0", 1 + 0.10 * thup, 1 - 0.12 * thup)
        P.rot("xem_7", -25.0 * co)
        P.rot("xem_25", 30.0 * co)
        lua(P, t, 1.0 + 1.5 * co, 0.5)
        mat(P, False)
        mo_het(P, moc(t, [(0, 0), (0.08, 1)]))

    for e, m in (("trung", "khung đòn trúng"), ("phun", "bắt đầu bắn tia lửa từ mũi giáo (xương mieng)"), ("het_phun", "hết tia lửa"),
                 ("nhay", "bật nhảy (chiêu cuối)"), ("dam", "bắt đầu đâm xuống"), ("cham_dat", "chạm đất"), ("nga", "đổ gục"), ("trung2", "nhát đập khiên thứ hai (dạng 2)"),
                 ("chan_dong", "chấn động sau cú đâm: dung nham phun quanh đối thủ (dạng 2)")):
        sk.su_kien(e, m)
    clips = [Clip("appear", P_DUR, appear, ev=[(P_DAP, "cham_dat", "")]),
             Clip("idle", I_DUR, idle, loop=True),
             Clip("walk", W_DUR, walk, loop=True),
             Clip("attack", A_DUR, attack, ev=[(A_TRUNG, "trung", "")] + ([(A_TRUNG2, "trung2", "")] if D2 else []), trung=A_TRUNG),
             Clip("cast", C_DUR, cast, ev=[(C_PHUN, "phun", ""), (C_HET, "het_phun", "")], trung=C_PHUN),
             Clip("skill", K_DUR, skill, ev=[(K_BAT, "nhay", ""), (K_DAM, "dam", ""), (K_TRUNG, "trung", "")]
                  + ([(K_TRUNG + 0.12, "chan_dong", "")] if D2 else []), trung=K_TRUNG),
             Clip("hit", CD["hit_01"][0], hit),
             Clip("die", D_DUR, die, ev=[(1.05, "nga", "")])]
    return clips, {}
