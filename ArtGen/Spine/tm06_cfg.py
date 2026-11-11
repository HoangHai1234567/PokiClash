# -*- coding: utf-8 -*-
"""tm06: gợi ý đặt mảnh trên concept (dùng chung cho tm06_place.py và bản thử không cv2)."""

# gợi ý trên concept (inbox/tm06_<k>/rig/concept_luoi.png): bb = khung bao CẢ mảnh (kể cả phần bị che, ước), r = góc ước (độ,
# ngược kim như mắt nhìn), lat = lật ngang, deu = cùng tỉ lệ hai chiều, img = tên ảnh (dùng lại một ảnh), ds = biên dò tỉ lệ,
# dr = biên dò góc, win = biên dò vị trí (px concept)
HINT = {
    1: {
        "dau": dict(bb=(740, 225, 1170, 455), r=-3, deu=True, s=0.85, ds=0.04, gamma=1.3),
        "ham": dict(bb=(930, 405, 1150, 500), r=0, deu=False, s=(0.48, 0.42), ds=0.12, dr=8),
        "than": dict(bb=(745, 400, 1000, 835), r=0, deu=False, ds=0.1, dr=6),
        "duoi": dict(bb=(298, 585, 800, 865), r=-3, deu=False, s=(0.58, 0.56), ds=0.07, gamma=1.3),
        "tay_n": dict(bb=(950, 495, 1140, 615), r=10, deu=True, s=0.5, ds=0.06, dr=12, gamma=1.3),
        "tay_x": dict(bb=(640, 420, 830, 615), r=0, lat=True, deu=True, s=0.52, ds=0.06, dr=12, gamma=1.3),
        "chan_t": dict(bb=(608, 640, 805, 878), r=0, deu=True, ds=0.12),
        "chan_p": dict(bb=(888, 655, 1102, 878), r=0, deu=True, ds=0.12),
        "bau": dict(bb=(445, 362, 697, 697), r=0, deu=True, ds=0.1),
        "nut": dict(bb=(497, 325, 577, 385), r=0, deu=True, s=0.42, ds=0.15, dr=12),
    },
    2: {
        "dau": dict(bb=(1080, 390, 1410, 600), r=0, deu=True, s=0.60, ds=0.06),
        "ham": dict(bb=(1090, 550, 1395, 650), r=-4, deu=False, s=(0.66, 0.66), ds=0.06, dr=6, gamma=1.25),
        "than": dict(bb=(300, 400, 1120, 700), r=0, deu=False, s=(0.80, 0.97), ds=0.06, dr=4),
        "duoi": dict(bb=(110, 320, 610, 640), r=5, deu=False, s=(0.86, 1.08), ds=0.12),
        "binh": dict(bb=(528, 295, 905, 568), r=0, deu=True),
        "nap": dict(bb=(650, 160, 905, 335), r=0, deu=True),
        "chan1": dict(bb=(300, 585, 520, 805), r=0, deu=True),
        "chan2": dict(bb=(548, 640, 735, 800), r=0, deu=True),
        "chan3": dict(bb=(790, 590, 1030, 808), r=0, deu=True),
        "chan4": dict(bb=(1150, 600, 1390, 805), r=0, deu=True),
    },
}
# mảnh dài vẽ duỗi thẳng nằm ngang (gốc trái): (ảnh, điểm gốc, điểm ngọn, bề dày đích px concept hoặc None = theo tỉ lệ dài)
TWO = {
    1: {
        "mang_n1": ("mang1", (808, 322), (664, 164), 84, False),
        "mang_n2": ("mang2", (805, 350), (580, 258), 80, False),
        "mang_n3": ("mang3", (805, 380), (624, 414), 72, False),
        "mang_x1": ("mang2", (1010, 300), (1016, 170), 58, False),
        "mang_x2": ("mang3", (1076, 318), (1100, 232), 48, False),
    },
    2: {
        "mang_n1": ("mang1", (1110, 465), (946, 266), 90),
        "mang_n2": ("mang2", (1108, 480), (887, 357), 85),
        "mang_n3": ("mang3", (1105, 495), (878, 457), 80),
        "mang_x1": ("mang3", (1236, 462), (1160, 382), 50, False),
        "mang_x2": ("mang2", (1272, 470), (1225, 300), 60, False),
        "mang_x3": ("mang2", (1305, 478), (1368, 352), 58, False),
    },
}
# thứ tự vẽ (sau → trước) để ghép thử
DRAW = {
    1: ["duoi", "bau", "nut", "tay_x", "than", "chan_t", "chan_p", "mang_x1", "mang_x2", "mang_n1", "mang_n2", "mang_n3",
        "mieng", "ham", "dau", "tay_n"],
    2: ["chan2", "duoi", "mang_x1", "mang_x2", "mang_x3", "than", "chan1", "chan3", "chan4", "binh", "nap", "mang_n1", "mang_n2",
        "mang_n3", "ham", "dau"],
}
# nối: mảnh A kéo dài (giữ đầu kia) cho mép của nó chui dưới mảnh B ít nhất n px (ngang): (A, mép A, B, mép B, n)
NOI = {1: [], 2: [("than", "phai", "dau", "trai", 60)]}
