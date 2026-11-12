# -*- coding: utf-8 -*-
"""Sơ đồ bố cục của kiếm sĩ rừng (kiem_si): khối từng part của rig ở dáng thủ idle giây 0, tô phẳng theo nhóm màu của THIẾT KẾ MÌNH; mũ
(mảnh làm nên bóng dáng) vẽ mới bằng mã cho từng hướng, không dùng hình bóng mũ sừng của con gốc. Chỉ để GPT lấy chỗ đặt, cỡ, thứ tự chồng.

Ba hướng ĐỀ XUẤT của Claude (2026-11-12), chờ người dùng chọn:
  khi_non   khỉ ronin đội nón lá (kasa), giáp nan tre, áo tơi lá, đuôi khỉ cuộn sau lưng; hai chân
  khi_mu    voọc tướng quân lông than, ria trắng, mũ kabuto sơn lục có mào là một chiếc lá to; hai chân
  giap_rong bộ giáp cũ không người mặc, dây leo và rễ cây chui vào điều khiển: mặt nạ gỗ, mào nhánh cây, bốn chân rễ
"""
import os

import cv2
import numpy as np
from PIL import Image

import kiem_si as G

W, H, S2, INK = G.W, G.H, G.S2, G.INK

HUONG = {
    "khi_non": dict(long=(150, 92, 56),          # lông khỉ nâu hung #965C38
                    da=(226, 180, 138),          # da mặt, bàn tay, bàn chân #E2B48A
                    giap=(207, 174, 107),        # giáp nan tre #CFAE6B
                    go=(92, 62, 42),             # gỗ sẫm: bao tay, viền giáp #5C3E2A
                    day=(47, 90, 58),            # dây bện lục sẫm #2F5A3A
                    vai=(62, 107, 69),           # vải quần lục #3E6B45
                    ao_la=(94, 148, 64),         # áo tơi lá #5E9440
                    mu=(216, 190, 122),          # nón lá rơm #D8BE7A
                    mao=(94, 148, 64),
                    nhan=(217, 98, 43),          # màu nhấn: tua, dây quấn chuôi #D9622B
                    vo=(70, 48, 36),             # vỏ kiếm #463024
                    mat=(240, 170, 50)),
    "khi_mu": dict(long=(64, 62, 58),            # lông voọc than #403E3A
                   da=(214, 176, 140),
                   giap=(76, 122, 63),           # giáp sơn lục rêu #4C7A3F
                   go=(207, 174, 107),           # viền tre #CFAE6B
                   day=(224, 160, 48),           # dây bện hổ phách #E0A030
                   vai=(92, 62, 42),
                   ao_la=(47, 107, 74),          # áo tơi lá sẫm #2F6B4A
                   mu=(47, 90, 58),              # mũ sơn lục sẫm #2F5A3A
                   mao=(124, 176, 72),           # mào lá #7CB048
                   nhan=(224, 160, 48),
                   vo=(70, 48, 36),
                   mat=(240, 170, 50)),
    "giap_rong": dict(long=(70, 128, 62),        # bó dây leo #46803E
                      da=(128, 88, 54),          # rễ, ngón cành #805836
                      giap=(122, 96, 66),        # giáp gỗ cũ #7A6042
                      go=(207, 174, 107),        # viền tre #CFAE6B
                      day=(47, 90, 58),
                      vai=(70, 128, 62),
                      ao_la=(124, 164, 74),      # áo rêu / lá #7CA44A
                      mu=(92, 70, 50),           # mũ gỗ sẫm #5C4632
                      mao=(128, 88, 54),
                      nhan=(200, 90, 50),        # tua đỏ gạch bạc màu #C85A32
                      vo=(70, 48, 36),
                      mat=(246, 217, 62)),
}

# part của con gốc → nhóm màu của mình (None = bỏ khỏi sơ đồ)
NHOM = {
    "P_shengzi_da2": None, "P_ke": None, "P_shengzi_da1": "duoi", "P_keR": "ao_la", "P_keL": "ao_la",
    "P_tuiL_H2": "da", "P_tuiL_H1": "long", "P_tuiL_Q1": "long", "P_tuiL_Q2": "da",
    "P_tuiR_H1": "long", "P_tuiR_H2": "da", "P_tuiR_Q1": "long", "P_tuiR_Q2": "da",
    "P_shenti1": "vai", "P_shenti2": "long", "P_shenti2_2": "giap",
    "P_shenti_sheng1": "day", "P_shenti_sheng2": "day", "P_shenti_sheng3": "day",
    "P_jianjiaL_G1": "nhan", "P_jianjiaR_G1": "nhan", "P_jianjiaR_G2": "nhan", "P_jianjiaR_G3": "nhan",
    "P_shouL1": "long", "P_shouL2_2": "long", "P_shouL2": "go", "P_shouR1": "long", "P_shouR2_2": "long", "P_shouR2": "go",
    "P_jianjiaL1": "giap", "P_jianjiaL2": "giap", "P_jianjiaR1": "giap", "P_jianjiaR2": "giap",
    "W_daoB_4": "giap", "W_daoB_3": None, "W_daoB_2": "vo", "W_daoB_1": "nhan",
    "W_daoA_5": "giap", "W_daoA_4": None, "W_daoA_3": None, "W_daoA_1": "vo", "W_daoA_2": "nhan",
    "P_shouL3_1": "da", "P_shouL3_2": "da", "P_shouL3_3": "da", "P_shouL3_4": "da",
    "P_shouR3_1": "da", "P_shouR3_2": "da", "P_shouR3_3": "da", "P_shouR3_4": "da",
    "P_tou2": "long", "P_tou": "da", "P_toukui2": None, "P_yanjing1": "mat", "P_toukui": "mu",
}
NHO = ("P_tui", "P_jianjiaL_G", "P_jianjiaR_G", "P_shouL3", "P_shouR3", "P_yanjing", "W_daoA_5", "W_daoB_4", "P_shouL2_2", "P_shouR2_2")
HAI_CHAN_BO = ("P_tuiR_Q1", "P_tuiR_Q2", "P_tuiL_H1", "P_tuiL_H2")          # hướng khỉ: chỉ còn chân sau (R_H) và chân trước (L_Q)


def _pts(ps):
    return (np.array(ps, float) * S2).astype(np.int32)


def mask_poly(ps, tron=3.0):
    m = np.zeros((H * S2, W * S2), np.uint8)
    cv2.fillPoly(m, [_pts(ps)], 255, cv2.LINE_AA)
    if tron:
        m = cv2.GaussianBlur(m, (0, 0), tron * S2)
    return m > 127


def mask_el(c, ax, goc=0.0):
    m = np.zeros((H * S2, W * S2), np.uint8)
    cv2.ellipse(m, (int(c[0] * S2), int(c[1] * S2)), (int(ax[0] * S2), int(ax[1] * S2)), goc, 0, 360, 255, -1, cv2.LINE_AA)
    return m > 127


def to(can, m, mau, net=6):
    can[m] = mau
    if net:
        can[G.vien(m, net)] = INK


def la(can, goc, mui, rong, mau, gan=None, net=5, cong=0.0):
    """một chiếc lá nhọn hai đầu: goc = cuống, mui = mũi lá, rong = bề rộng lớn nhất; cong = độ võng (px) của sống lá."""
    g, t = np.array(goc, float), np.array(mui, float)
    d = t - g
    L = np.hypot(*d)
    u = d / L
    n = np.array([-u[1], u[0]])
    tr, du = [], []
    for s in np.linspace(0, 1, 17):
        c = g + u * L * s + n * cong * np.sin(np.pi * s)
        tr.append(c + n * rong / 2 * np.sin(np.pi * s) ** 0.75)
        du.append(c - n * rong / 2 * np.sin(np.pi * s) ** 0.75)
    m = mask_poly(tr + du[::-1], 0.8)
    to(can, m, mau, net)
    if gan is not None:
        gs = [g + u * L * s + n * cong * np.sin(np.pi * s) for s in np.linspace(0.08, 0.88, 9)]
        cv2.polylines(can, [_pts(gs)], False, gan, 3 * S2 // 2, cv2.LINE_AA)
    return m


def duong(can, ps, day, mau, net=5):
    """một dải cong (đuôi, cành): đường gấp khúc làm trơn, bề dày day."""
    m = np.zeros((H * S2, W * S2), np.uint8)
    cv2.polylines(m, [_pts(ps)], False, 255, int(day * S2), cv2.LINE_AA)
    m = cv2.GaussianBlur(m, (0, 0), 1.5 * S2) > 127
    to(can, m, mau, net)
    return m


# ---------------------------------------------------------------- mũ của mình (toạ độ pixel khung concept; đầu ở x 916–1087, y 379–588)
def non_la(can, P):
    """nón lá hình chóp rộng vành (kasa), chúc về trước che trán: vành elip + chóp."""
    c, ax, goc = (925, 372), (318, 86), 7
    vanh = mask_el(c, ax, goc)
    chop = mask_poly([(898, 92), (628, 338), (1238, 410)], 2.0)
    m = vanh | chop
    to(can, m, P["mu"], 6)
    a = np.deg2rad(goc)
    for k in (-0.82, -0.5, -0.15, 0.2, 0.55, 0.85):                                  # nan nón toả từ chóp xuống vành
        q = (c[0] + ax[0] * k * np.cos(a), c[1] + ax[0] * k * np.sin(a) + ax[1] * 0.75 * np.sqrt(max(0, 1 - k * k)))
        cv2.line(can, tuple(_pts([(898, 100)])[0]), tuple(_pts([q])[0]), P["go"], 2 * S2, cv2.LINE_AA)
    to(can, mask_el((898, 98), (26, 20)), P["nhan"], 5)                                # nút chóp
    la(can, (760, 250), (640, 150), 60, P["ao_la"], P["day"])                         # hai chiếc lá giắt trên nón
    la(can, (790, 232), (720, 110), 52, P["ao_la"], P["day"])


def mu_kabuto(can, P, kieu):
    """mũ kabuto: bát mũ tròn + tấm che gáy xoè ra sau + lưỡi trai chúc về trước; mào là chiếc lá to (khi_mu) hoặc nhánh cây (giap_rong)."""
    if kieu == "khi_mu":
        la(can, (1010, 300), (1330, 70), 150, P["mao"], P["mu"], 6, cong=-46)          # mào lá to quét lên phải (vẽ trước, nấp sau bát mũ)
        la(can, (990, 270), (1150, 40), 84, P["mao"], P["mu"], 6, cong=-20)
    else:
        for ds, day in [([(1000, 290), (1090, 210), (1150, 120), (1250, 70)], 34), ([(1090, 210), (1070, 120), (1100, 50)], 24),
                        ([(1150, 120), (1250, 150), (1320, 120)], 24)]:
            duong(can, ds, day, P["mao"], 5)
        for g, t in [((1250, 70), (1330, 30)), ((1100, 50), (1060, -6)), ((1320, 120), (1392, 150)), ((1180, 96), (1196, 30))]:
            la(can, g, (t[0], max(8, t[1])), 40, P["ao_la"], None, 4)
    gay = mask_poly([(700, 150), (612, 250), (622, 392), (800, 450), (880, 300)], 5.0)   # tấm che gáy ba tầng
    to(can, gay, P["mu"], 6)
    for y0 in (0.36, 0.68):
        ps = [(690 - 78 * y0, 170 + 150 * y0 + 60), (860 - 40 * y0, 300 + 100 * y0)]
        cv2.line(can, tuple(_pts([ps[0]])[0]), tuple(_pts([ps[1]])[0]), P["go"], 3 * S2, cv2.LINE_AA)
    bat = mask_el((885, 262), (215, 196)) & (np.arange(H * S2)[:, None] < 372 * S2)
    to(can, bat, P["mu"], 6)
    trai = mask_poly([(790, 330), (1010, 300), (1130, 420), (1060, 470), (930, 420), (800, 392)], 4.0)   # lưỡi trai
    to(can, trai, P["mu"], 6)
    to(can, mask_poly([(705, 318), (1010, 280), (1022, 316), (712, 360)], 2.0), P["go"], 5)   # đai mũ
    if kieu == "giap_rong":
        to(can, mask_el((800, 110), (90, 34), -12), P["ao_la"], 5)                     # mảng rêu trên đỉnh mũ


def duoi(can, P, kieu):
    if kieu == "giap_rong":                                                          # chùm dương xỉ sau lưng
        for g, t, r, c in [((640, 420), (430, 150), 120, -30), ((640, 420), (540, 96), 100, -14), ((640, 420), (400, 300), 96, -30)]:
            la(can, g, t, r, P["ao_la"], P["day"], 5, cong=c)
        return
    ds = [(690, 470), (600, 400), (520, 300), (486, 196), (520, 126), (590, 110), (624, 160), (590, 206), (556, 190)]
    duong(can, ds, 44, P["long"], 6)                                                 # đuôi khỉ dài cuộn móc ở ngọn


def bo_cuc(kieu="khi_non", luu=True):
    P = HUONG[kieu]
    _, _, atts = G.nap()
    T = G.khung_T()
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    hop = {}
    khi = kieu.startswith("khi")
    for a in atts:
        ten = a["slot"]
        nh = NHOM.get(ten)
        if nh is None or (khi and ten in HAI_CHAN_BO):
            continue
        if nh == "duoi":
            duoi(can, P, kieu)
            continue
        if nh == "mu":
            if kieu == "khi_non":
                non_la(can, P)
            else:
                mu_kabuto(can, P, kieu)
            continue
        nho = ten.startswith(NHO)
        m = G.bong_khung(a, T, 2.2 if nho else 5.0)
        if not m.any():
            continue
        if ten == "P_tou" and kieu == "khi_mu":                                       # vành ria trắng quanh mặt voọc
            to(can, cv2.dilate(m.astype(np.uint8), G.el(16)).astype(bool), (237, 230, 210), 5)
        if ten == "P_tou" and kieu == "giap_rong":
            P = dict(P, da=(214, 190, 150))                                          # mặt nạ gỗ nhạt
        to(can, m, P[nh], 4 if nho else 6)
        P = HUONG[kieu]
        ys, xs = np.nonzero(m)
        hop[ten] = [int(xs.min() / S2), int(ys.min() / S2), int(xs.max() / S2), int(ys.max() / S2)]
        if ten in ("P_keL",):                                                        # áo tơi: vài sống lá
            for g, t in [((700, 480), (470, 800)), ((760, 520), (620, 836)), ((860, 500), (940, 830))]:
                cv2.line(can, tuple(_pts([g])[0]), tuple(_pts([t])[0]), P["day"], 2 * S2, cv2.LINE_AA)
        if ten == "P_jianjiaR1":                                                     # huy hiệu tròn trên tấm vai gần
            to(can, mask_el((585, 400), (86, 80), -30), P["go"], 5)
            la(can, (548, 440), (628, 352), 60, P["ao_la"] if kieu != "khi_mu" else P["mao"], P["day"] if kieu != "khi_mu" else P["mu"], 4)
    out = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    if luu:
        os.makedirs(G.MAU, exist_ok=True)
        out.save(os.path.join(G.MAU, f"bo_cuc_{kieu}.png"))
        print(os.path.join(G.MAU, f"bo_cuc_{kieu}.png"))
    return out
