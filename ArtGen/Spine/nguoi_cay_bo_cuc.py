# -*- coding: utf-8 -*-
"""Sơ đồ bố cục người cây (nguoi_cay) cho lượt concept: khối thân lấy từ dáng thủ của rig gốc (làm trơn, tô màu của mình), ĐẦU và
các lớp phủ (u rêu vai, áo lá ngực, váy lá, dây gai cẳng tay, nấm / hoa) vẽ mới bằng mã. Chỉ đưa chỗ đặt, cỡ, thứ tự chồng.

    py -3 -I ArtGen/Spine/nguoi_cay.py bo_cuc [dam_lay | mat_go]
"""
import json
import os

import cv2
import numpy as np
from PIL import Image

import nguoi_cay as N

S2, W, H, INK = N.S2, N.W, N.H, N.INK
GAN = (28, 74, 52)


def soc(can, m, mau, chu_ky=44, rong=17, xien=0.55):
    """dây quấn xoắn quanh một khúc tay: các dải xiên cách đều dọc trục dài của mảnh."""
    ys, xs = np.nonzero(m)
    P = np.stack([xs, ys], 1).astype(float)
    c = P.mean(0)
    _, _, vt = np.linalg.svd((P - c)[:: max(1, len(P) // 4000)], full_matrices=False)
    s = (P - c) @ vt[0] + xien * ((P - c) @ vt[1])
    on = (s / S2) % chu_ky < rong
    can[ys[on], xs[on]] = mau
    can[N.vien(m, 6)] = INK


def vach(can, m, y, mau=INK, day=3):
    """một vạch ngang hơi võng nằm trong mảnh m (đai rễ quấn bụng)."""
    t = np.zeros(m.shape, np.uint8)
    xs = np.nonzero(m.any(0))[0]
    x0, x1 = xs.min() / S2, xs.max() / S2
    ps = [(x, y + 7 * np.sin(np.pi * (x - x0) / (x1 - x0))) for x in np.linspace(x0, x1, 20)]
    cv2.polylines(t, [N._pts(ps)], False, 255, day * S2, cv2.LINE_AA)
    can[(t > 127) & m] = mau


def dau_dam_lay(can, P):
    # rêu rủ sau gáy (bên trái), nấp sau mũ trùm
    for x0, y0, x1, y1, d in [(628, 415, 596, 585, 30), (662, 450, 640, 612, 28), (700, 470, 690, 590, 24)]:
        N.duong(can, [(x0, y0), ((x0 + x1) / 2 - 6, (y0 + y1) / 2), (x1, y1)], d, P["reu_ru"])
    # mũ trùm rêu: vòm tròn, mép dưới lượn sóng
    m = N.mask_el((762, 372), (152, 128))
    for x in range(630, 900, 44):
        m |= N.mask_el((x, 372 + 118 * np.sqrt(max(0.05, 1 - ((x - 762) / 152.0) ** 2))), (26, 22))
    N.to(can, m, P["reu"], 6)
    # hốc mặt tối + hai mắt xếch
    N.to(can, N.mask_el((806, 398), (92, 72), -4), P["mat_nen"], 5)
    N.to(can, N.mask_poly([(748, 380), (796, 396), (792, 418), (756, 414)], 0.8), P["mat"], 0)
    N.to(can, N.mask_poly([(832, 398), (872, 384), (870, 412), (838, 418)], 0.8), P["mat"], 0)
    # chồi dương xỉ cuộn trên đỉnh đầu + hai lá non ở gốc
    th = np.linspace(0, 1.55 * np.pi, 26)
    xoan = [(700 + (46 - 20 * t / th[-1]) * np.cos(-t - 0.2), 170 + (46 - 20 * t / th[-1]) * np.sin(-t - 0.2)) for t in th][::-1]
    N.duong(can, [(742, 262), (748, 222), (746, 190)] + [xoan[-1]] + xoan[::-1][1:], 20, P["la_nhat"], 5)
    N.la(can, (742, 262), (808, 214), 34, P["la_nhat"], GAN)
    N.la(can, (738, 262), (676, 236), 30, P["la_nhat"], GAN)


def dau_mat_go(can, P):
    # mặt nạ gỗ bầu dục
    N.to(can, N.mask_el((800, 404), (104, 98), -4), P["go"], 6)
    # ba chiếc lá to làm mũ trùm, cuống ở đỉnh trán, mũi lá quét ra sau gáy (bên trái)
    N.la(can, (835, 330), (590, 498), 150, P["la"], GAN, 6)
    N.la(can, (850, 312), (566, 372), 160, P["reu"], GAN, 6)
    N.la(can, (862, 300), (600, 232), 150, P["la"], GAN, 6)
    N.la(can, (848, 300), (905, 236), 44, P["reu_ru"], GAN, 5)
    # gờ mày vỏ cây chữ V, mắt hổ phách, khe miệng
    N.to(can, N.mask_poly([(742, 352), (812, 384), (892, 356), (896, 374), (814, 408), (738, 372)], 1.2), P["re"], 4)
    N.to(can, N.mask_poly([(756, 392), (800, 410), (796, 428), (762, 422)], 0.8), P["mat"], 4)
    N.to(can, N.mask_poly([(836, 410), (878, 394), (878, 420), (842, 428)], 0.8), P["mat"], 4)
    cv2.polylines(can, [N._pts([(790, 462), (822, 456), (852, 462)])], False, INK, 5 * S2, cv2.LINE_AA)


def canh(can, goc, ngon, nhanh, P, day=15):
    """một cành khô gãy có một chạc."""
    g, t = np.array(goc, float), np.array(ngon, float)
    giua = g + (t - g) * 0.55
    N.duong(can, [tuple(giua), tuple(nhanh)], day * 0.75, P["re"], 4)
    N.duong(can, [tuple(g), tuple(giua), tuple(t)], day, P["re"], 4)


def ru(can, xs, y0, y1, P, day=22):
    """mấy dải rêu rủ thẳng xuống, dài ngắn so le."""
    for i, x in enumerate(xs):
        N.duong(can, [(x, y0), (x - 4, (y0 + y1) / 2), (x + 3, y1 - (14 if i % 2 else 0))], day, P["reu"], 4)


def bo_cuc_chien(luu=True):
    """bản 2: dáng CHIẾN, vai u khổng lồ, đầu nhỏ thụt giữa hai vai, thân rêu lục gần kín, cành khô trên vai, rêu rủ dưới tay."""
    P = N.PALS["chien"]
    _, _, atts = N.nap()
    T = N.khung_T()
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    A = {a["att"]: a for a in atts}

    def khoi(ten, mau, tron=6.0, no=0):
        m = N.bong_khung(A[ten], T, tron)
        if no:
            m = cv2.dilate(m.astype(np.uint8), N.el(no)).astype(bool)
        N.to(can, m, mau, 6)
        return m

    def tam(m):
        ys, xs = np.nonzero(m)
        return (ys.min() + ys.max()) / 2 / S2

    # 1. tay XA: bắp rêu, rêu rủ dưới bắp, cẳng gỗ quấn dây gai, nắm tay; cành khô + u rêu vai xa
    khoi("P_shouL1", P["than"])
    ru(can, [880, 912, 944], 640, 724, P)
    soc(can, khoi("P_shouL2", P["go"]), P["day"])
    khoi("P_shouL3", P["go"], no=10)
    canh(can, (938, 440), (920, 338), (972, 352), P)
    N.to(can, N.mask_el((948, 496), (122, 74), 10), P["reu"], 6)
    N.la(can, (930, 470), (1010, 416), 44, P["la"], GAN)
    # 2. chân
    khoi("P_bu2", P["la"], 3.0)
    for dui, ong, ban in [("P_tuiR1", "P_tuiR2", "P_jiaoL"), ("P_tuiL1", "P_tuiL2", "P_jiaoR")]:
        khoi(ban, P["go"], 3.0, no=5)
        khoi(dui, P["than"])
        mo = khoi(ong, P["go"])
        vach(can, mo, tam(mo) + 8, P["day"], 9)
    # 3. thân rêu sẫm, một dây leo vắt chéo, áo lá răng cưa năm chiếc
    mt = khoi("P_shenti2", P["than"])
    t = np.zeros(mt.shape, np.uint8)
    cv2.polylines(t, [N._pts([(600, 560), (700, 640), (800, 680), (884, 690)])], False, 255, 20 * S2, cv2.LINE_AA)
    can[(t > 127) & mt] = P["day"]
    can[N.vien(mt, 6)] = INK
    for g, tt, r, c in [((640, 486), (622, 590), 62, "la"), ((866, 490), (886, 584), 58, "la"), ((690, 480), (684, 622), 70, "la_nhat"),
                        ((820, 482), (834, 616), 70, "la_nhat"), ((754, 484), (758, 640), 76, "la")]:
        N.la(can, g, tt, r, P[c], GAN, 6)
    # 4. váy: sáu lá hẹp dài ngắn so le + đai dây leo
    for g, tt, r, c in [((612, 700), (584, 836), 58, "la"), ((872, 698), (900, 830), 58, "la"), ((658, 704), (654, 888), 64, "la_nhat"),
                        ((826, 704), (836, 872), 64, "la_nhat"), ((708, 706), (716, 846), 62, "la"), ((770, 706), (780, 906), 66, "la")]:
        N.la(can, g, tt, r, P[c], GAN, 6)
    N.duong(can, [(596, 694), (680, 706), (800, 706), (884, 690)], 24, P["day"], 5)
    # 5. tay GẦN: nắm tay, cẳng gỗ quấn dây gai, bắp rêu + rêu rủ; cành khô + u rêu vai gần
    khoi("P_shouR3", P["go"], no=10)
    soc(can, khoi("P_shouR2", P["go"]), P["day"])
    ru(can, [540, 572, 604], 624, 712, P)
    khoi("P_shouR1", P["than"])
    canh(can, (470, 436), (432, 322), (490, 338), P)
    canh(can, (566, 428), (584, 348), (552, 356), P, 12)
    N.to(can, N.mask_el((522, 492), (142, 84), -8), P["reu"], 6)
    N.la(can, (500, 452), (410, 420), 46, P["la"], GAN)
    # 6. đầu nhỏ, thấp, chúi về trước: mào lá răng cưa quét ra sau, gờ mày, dải hốc mắt tối, hai mắt cam, hàm bạnh
    for g, tt, r in [((760, 372), (640, 330), 52), ((780, 356), (668, 268), 56), ((806, 350), (752, 246), 52)]:
        N.la(can, g, tt, r, P["la"], GAN, 5)
    N.to(can, N.mask_poly([(712, 372), (742, 344), (806, 330), (862, 340), (892, 376), (896, 440), (880, 494), (826, 520), (760, 514),
                           (716, 474), (702, 420)], 4.0), P["than"], 6)
    N.to(can, N.mask_poly([(716, 404), (806, 420), (890, 398), (888, 436), (808, 448), (722, 440)], 1.0), P["mat_nen"], 0)
    N.to(can, N.mask_poly([(740, 414), (790, 424), (786, 440), (746, 436)], 0.6), P["mat"], 0)
    N.to(can, N.mask_poly([(828, 424), (874, 410), (872, 432), (832, 440)], 0.6), P["mat"], 0)
    N.to(can, N.mask_poly([(700, 384), (808, 408), (898, 378), (900, 402), (808, 432), (700, 408)], 1.2), P["la"], 5)
    cv2.polylines(can, [N._pts([(768, 484), (806, 474), (850, 480)])], False, INK, 5 * S2, cv2.LINE_AA)
    out = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    if luu:
        p = os.path.join(N.MAU, "bo_cuc_chien.png")
        out.save(p)
        print(p)
    return out


def bo_cuc(kieu="dam_lay", luu=True):
    if kieu == "chien":
        return bo_cuc_chien(luu)
    P = N.PALS[kieu]
    _, _, atts = N.nap()
    T = N.khung_T()
    can = np.full((H * S2, W * S2, 3), 255, np.uint8)
    A = {a["att"]: a for a in atts}
    hop = {}

    def khoi(ten, mau, tron=6.0, no=0):
        m = N.bong_khung(A[ten], T, tron)
        if no:
            m = cv2.dilate(m.astype(np.uint8), N.el(no)).astype(bool)
        N.to(can, m, mau, 6)
        ys, xs = np.nonzero(m)
        hop[ten] = [int(xs.min() / S2), int(ys.min() / S2), int(xs.max() / S2), int(ys.max() / S2)]
        return m

    # 1. tay XA (bên phải hình, nắm đấm giơ): bắp, cẳng quấn dây gai, nắm tay rễ; u rêu vai xa
    khoi("P_shouL1", P["re"])
    soc(can, khoi("P_shouL2", P["re"]), P["day"])
    khoi("P_shouL3", P["go"], no=8)
    N.to(can, N.mask_el((925, 520), (104, 56), 14), P["reu"], 6)
    if kieu == "dam_lay":
        N.la(can, (900, 492), (1010, 446), 52, P["la"], GAN)
    else:
        N.la(can, (900, 492), (1004, 440), 50, P["reu_ru"], GAN)
    # 2. chân xa, chân gần
    khoi("P_bu2", P["la"], 3.0)
    for dui, ong, ban in [("P_tuiR1", "P_tuiR2", "P_jiaoL"), ("P_tuiL1", "P_tuiL2", "P_jiaoR")]:
        khoi(ban, P["go"], 3.0, no=4)
        khoi(dui, P["reu"])
        mo = khoi(ong, P["re"])
        vach(can, mo, (hop[ong][1] + hop[ong][3]) / 2 + 8, P["day"], 9)
    # 3. thân: bụng rễ bện có hai đai, áo lá ngực bốn chiếc
    mt = khoi("P_shenti2", P["re"])
    vach(can, mt, 652)
    vach(can, mt, 690)
    for g, t, r, c in [((652, 474), (640, 612), 86, "la"), ((858, 478), (876, 602), 78, "la"), ((722, 466), (722, 636), 96, "reu" if kieu == "mat_go" else "la"),
                       ((792, 468), (806, 630), 96, "la")]:
        N.la(can, g, t, r, P[c], GAN, 6)
    # 4. váy lá: năm chiếc lá dài rủ từ đai dây leo
    for g, t, r, c in [((618, 700), (598, 852), 74, "la"), ((866, 698), (884, 846), 74, "la"), ((678, 704), (690, 902), 88, "reu"),
                       ((806, 704), (818, 888), 88, "reu"), ((742, 706), (756, 866), 84, "la")]:
        N.la(can, g, t, r, P[c], GAN, 6)
    N.duong(can, [(596, 694), (680, 706), (800, 706), (884, 690)], 24, P["day"], 5)
    # 5. tay GẦN (bên trái hình, buông thấp): nắm tay, cẳng quấn dây gai, bắp; u rêu vai gần + nấm / hoa
    khoi("P_shouR3", P["go"], no=8)
    soc(can, khoi("P_shouR2", P["re"]), P["day"])
    khoi("P_shouR1", P["re"])
    N.to(can, N.mask_el((528, 522), (118, 62), -10), P["reu"], 6)
    if kieu == "dam_lay":
        N.nam(can, (474, 462), 26, P)
        N.nam(can, (560, 468), 22, P)
        N.nam(can, (518, 440), 34, P)
    else:
        for x, y, r in [(486, 452, 24), (540, 440, 30)]:
            N.duong(can, [(x, y + r + 26), (x, y)], 10, P["day"], 4)
            N.to(can, N.mask_el((x, y), (r, r * 0.9)), P["nam"], 4)
    # 6. đầu
    (dau_dam_lay if kieu == "dam_lay" else dau_mat_go)(can, P)
    out = Image.fromarray(can).resize((W, H), Image.LANCZOS)
    if luu:
        os.makedirs(N.MAU, exist_ok=True)
        p = os.path.join(N.MAU, f"bo_cuc_{kieu}.png")
        out.save(p)
        json.dump(hop, open(os.path.join(N.MAU, "bo_cuc_hop.json"), "w"), indent=0)
        print(p)
    return out
