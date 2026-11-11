# -*- coding: utf-8 -*-
"""tm09: gợi ý đọc trên concept kẻ lưới cho tm09_place.py (dò) và tm09.py (cách lai) — không cần cv2."""

# gợi ý đọc trên inbox/tm09_<k>/rig/concept_luoi.png: khung bao của bộ phận trên concept (x0, y0, x1, y1), tỉ lệ ước (sx, sy)
# hoặc None (= khung bao / cỡ mảnh), góc ước, lật, cùng_tỉ_lệ (sy = sx). Dò tỉ lệ tự do bị lệch về mảnh nhỏ (SQDIFF chuẩn hoá theo
# diện tích): chỉ dò tinh ±12 % quanh tỉ lệ ước, ±10° góc, ±25 px vị trí.
HINT = {
    2: {"dau": ((1035, 290, 1455, 470), None, -4, False, False),
        "sung": ((1040, 90, 1210, 320), (0.58, 0.58), -62, True, True),
        "sung_xa": ((890, 95, 1060, 330), (0.58, 0.58), -58, True, True),
        "than": ((490, 395, 1090, 748), None, 0, False, False),
        "go_vai": ((820, 315, 1010, 500), None, 0, False, False),
        "go_lung": ((640, 395, 830, 500), None, 0, False, False),
        "go_hong": ((420, 430, 640, 520), None, -8, False, False),
        "chuy": ((80, 230, 270, 410), None, 0, True, True)},
    1: {"dau": ((745, 215, 1455, 560), None, 0, False, False),
        "sung": ((840, 135, 1000, 270), (0.8, 0.8), -70, True, True),
        "sung_xa": ((700, 190, 860, 340), (0.78, 0.78), -40, True, True),
        "than": ((330, 470, 920, 795), None, 0, False, False),
        "go_vai": ((580, 405, 700, 505), None, 0, False, False),
        "go_lung": ((450, 445, 560, 540), None, 0, False, False),
        "go_hong": ((335, 505, 430, 575), None, 0, False, False),
        "chuy": ((65, 515, 215, 680), None, 0, True, True)},
}
# mảnh dài: (điểm gốc, điểm ngọn) trên concept; tỉ lệ dọc trục = dài cung / dài ảnh (he_cung × dây cung); độ dày đích (px concept)
TWO = {
    2: {"duoi": ((480, 600), (235, 395), 1.22, 135), "chan_tn": ((895, 565), (935, 838), 1.0, 150),
        "chan_sn": ((560, 590), (480, 838), 1.0, 185), "chan_tx": ((1075, 600), (1130, 828), 1.0, None),
        "chan_sx": ((700, 620), (700, 828), 1.0, None)},
    1: {"duoi": ((335, 655), (185, 605), 1.05, 120), "chan_tn": ((700, 700), (740, 882), 1.0, 150),
        "chan_sn": ((330, 740), (330, 882), 1.0, 170), "chan_tx": ((990, 700), (1040, 882), 1.0, None),
        "chan_sx": ((560, 740), (560, 882), 1.0, None)},
}
DRAW = ["chan_sx", "chan_tx", "duoi", "chuy", "go_vai", "go_lung", "go_hong", "sung_xa", "than", "chan_sn", "chan_tn", "dau", "sung"]
