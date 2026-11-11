# -*- coding: utf-8 -*-
"""tm04 (Hà Bá): cắt thẳng từ concept đã duyệt các lớp của rig (cách lai, DAC_TA_LO_THUY mục 5).

Vùng từng phần: loang đều từ hạt giống kẻ tay trong vùng màu, nét mực nâu là tường, pixel còn lại lấy nhãn gần nhất (như
thuy_long_lien.labels). Mỗi lớp = phần của lớp + dải mọc thêm dưới các lớp trên (vẽ bù TELEA từ màu chính lớp, kẻ nét mực dọc mép
dải), co về tỉ lệ atlas. Ra inbox/tm04_<k>/manh/: <lớp>.png, <lớp>_lab.png (chỉ số phần, 255 = trống), cat.json, nhan.png, lop.png.
Cần cv2:

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm04_cat.py 2
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")

import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

CODE = "tm04"
INK = (43, 33, 24)
KS = {2: 0.5, 1: 0.56}  # tỉ lệ concept px -> atlas px

# ---------------------------------------------------------------- cấu hình theo dạng (toạ độ concept L1_duyet.png 1536x1024)
# phần: thứ tự cũng là ưu tiên hạt giống (phần sau đè phần trước)
PARTS = {
    1: ["chan_sx", "chan_tx", "duoi", "vay1", "vay2", "vay3", "mieng", "than", "tai_n", "tai_x", "chan_sn", "chan_tn", "ham"],
    2: ["chan_sx", "chan_tx", "giot1", "giot2", "giot3", "duoi", "vay1", "vay2", "vay3", "vay4", "mieng", "than", "tai_n",
        "tai_x", "chan_sn", "chan_tn", "giap", "ham"],
}
# lớp sau -> trước: (tên lớp, [phần], px mọc thêm dưới các lớp trên)
LAYERS = {
    1: [("chan_sx", ["chan_sx"], 34), ("chan_tx", ["chan_tx"], 34), ("duoi", ["duoi"], 26),
        ("vay", ["vay1", "vay2", "vay3"], 30), ("mieng", ["mieng"], 44), ("than", ["than", "tai_n", "tai_x"], 40),
        ("chan_sn", ["chan_sn"], 0), ("chan_tn", ["chan_tn"], 0), ("ham", ["ham"], 0)],
    2: [("chan_sx", ["chan_sx"], 70), ("chan_tx", ["chan_tx"], 70), ("duoi", ["duoi"], 45),
        ("vay", ["vay1", "vay2", "vay3", "vay4"], 45), ("mieng", ["mieng"], 80), ("than", ["than", "tai_n", "tai_x"], 90),
        ("chan_sn", ["chan_sn"], 0), ("chan_tn", ["chan_tn"], 25), ("giap", ["giap"], 0), ("ham", ["ham"], 0),
        ("giot1", ["giot1"], 0), ("giot2", ["giot2"], 0), ("giot3", ["giot3"], 0)],
}
# hạt giống: ("line", [điểm], dày) | ("poly", [điểm]) | ("pt", (x, y), bán kính)
SEEDS = {
    1: {
        "duoi": [("line", [(515, 588), (470, 560), (420, 520), (392, 460), (410, 412)], 14),
                 ("pt", (430, 390), 8), ("pt", (500, 382), 8), ("pt", (520, 420), 6), ("pt", (470, 430), 6), ("pt", (382, 402), 6)],
        "vay1": [("line", [(600, 345), (650, 335), (688, 372)], 8), ("pt", (622, 395), 7)],
        "vay2": [("line", [(740, 262), (800, 242), (850, 300)], 9), ("pt", (800, 345), 8)],
        "vay3": [("pt", (935, 345), 8), ("pt", (960, 368), 5)],
        "mieng": [("pt", (962, 640), 4), ("pt", (1030, 640), 4), ("pt", (1000, 633), 3)],
        "than": [("poly", [(560, 455), (760, 425), (760, 620), (560, 640)]),
                 ("pt", (900, 420), 8), ("pt", (990, 478), 5), ("pt", (880, 500), 4), ("pt", (1045, 492), 3),
                 ("line", [(800, 580), (900, 560), (1000, 570), (1100, 585)], 12),
                 ("pt", (978, 616), 2), ("pt", (1030, 606), 2),
                 ("line", [(600, 692), (720, 702)], 9), ("pt", (840, 640), 10)],
        "tai_n": [("pt", (812, 412), 8)],
        "tai_x": [("pt", (1035, 398), 6)],
        "chan_sx": [("pt", (556, 735), 6), ("pt", (542, 760), 3), ("pt", (572, 762), 3)],
        "chan_sn": [("line", [(650, 708), (650, 750)], 14), ("pt", (625, 772), 3), ("pt", (655, 774), 3), ("pt", (685, 772), 3)],
        "chan_tx": [("pt", (815, 738), 6), ("pt", (800, 765), 3), ("pt", (835, 765), 3)],
        "chan_tn": [("line", [(930, 716), (935, 755)], 14), ("pt", (905, 776), 3), ("pt", (935, 779), 3), ("pt", (965, 776), 3)],
        "ham": [("line", [(962, 673), (1000, 679), (1032, 673)], 6), ("pt", (918, 662), 4), ("pt", (1065, 655), 4),
                ("line", [(905, 706), (980, 713), (1058, 706)], 6)],
    },
    2: {
        "giot1": [("pt", (240, 52), 7)], "giot2": [("pt", (146, 118), 7)], "giot3": [("pt", (86, 250), 6)],
        "duoi": [("line", [(245, 455), (200, 410), (150, 350), (140, 250), (190, 150), (280, 80), (380, 60)], 20),
                 ("line", [(130, 420), (200, 330), (260, 270)], 12),
                 ("pt", (460, 110), 10), ("pt", (480, 170), 9), ("pt", (430, 200), 8), ("pt", (330, 280), 8),
                 ("pt", (350, 330), 7), ("pt", (300, 330), 6)],
        "vay1": [("line", [(425, 320), (490, 340), (540, 390)], 10), ("pt", (500, 395), 7), ("pt", (450, 310), 6)],
        "vay2": [("line", [(550, 240), (640, 260), (700, 330)], 10), ("pt", (670, 365), 8)],
        "vay3": [("line", [(720, 175), (810, 165), (880, 250)], 10), ("pt", (840, 335), 9)],
        "vay4": [("line", [(880, 85), (1000, 85), (1090, 160), (1130, 260)], 10), ("pt", (1010, 300), 10),
                 ("pt", (1080, 290), 8), ("pt", (960, 160), 10)],
        "mieng": [("pt", (1250, 682), 6), ("pt", (1280, 735), 4), ("pt", (1148, 686), 3), ("pt", (1290, 705), 3)],
        "than": [("poly", [(420, 450), (620, 425), (620, 560), (420, 560)]),                 # lưng, mông
                 ("line", [(440, 750), (590, 780)], 14), ("pt", (930, 720), 10),               # bụng
                 ("pt", (890, 600), 5), ("pt", (915, 700), 5), ("pt", (978, 772), 9), ("pt", (1030, 752), 5),  # vòng cổ
                 ("pt", (340, 485), 14), ("pt", (312, 520), 8), ("pt", (960, 600), 10), ("pt", (940, 660), 8),  # mông (cục đuôi), cổ
                 ("pt", (600, 400), 6), ("pt", (700, 395), 6), ("pt", (930, 420), 6),         # lưng trên giáp
                 ("poly", [(1010, 380), (1200, 385), (1230, 470), (1100, 495), (1030, 460)]),  # mũ đồng
                 ("pt", (1220, 530), 6),                                                       # mặt giữa hai mắt
                 ("pt", (1145, 520), 8), ("pt", (1285, 523), 6),                               # mắt
                 ("line", [(1170, 590), (1300, 585), (1380, 600)], 14),                         # mõm trên
                 ("pt", (1040, 640), 12),                                                       # má
                 ("pt", (1175, 680), 4), ("pt", (1228, 655), 2), ("pt", (1288, 652), 2), ("pt", (1320, 672), 3)],  # răng trên
        "tai_n": [("pt", (975, 452), 9), ("pt", (958, 420), 5)],
        "tai_x": [("pt", (1290, 410), 8)],
        "chan_sn": [("line", [(300, 640), (250, 780), (205, 880)], 28), ("pt", (162, 912), 7), ("pt", (212, 915), 7),
                    ("pt", (272, 913), 7)],
        "chan_tn": [("line", [(700, 650), (760, 800), (800, 905)], 28), ("pt", (740, 945), 7), ("pt", (830, 950), 7),
                    ("pt", (915, 945), 7)],
        "chan_sx": [("line", [(470, 790), (480, 860)], 18), ("pt", (440, 885), 6), ("pt", (495, 890), 6),
                    ("pt", (545, 885), 6)],
        "chan_tx": [("line", [(1180, 880), (1300, 895)], 12), ("pt", (1220, 930), 6), ("pt", (1290, 935), 6),
                    ("pt", (1350, 925), 6)],
        "giap": [("poly", [(700, 470), (840, 440), (870, 500), (800, 580), (700, 600)]),
                 ("line", [(645, 600), (700, 470), (880, 425)], 9)],
        "ham": [("line", [(1100, 822), (1250, 845), (1390, 805)], 12), ("pt", (1400, 735), 8),
                ("line", [(1075, 640), (1085, 720), (1100, 780)], 12),                         # ngà gần
                ("line", [(1445, 640), (1440, 720)], 8),                                       # ngà xa
                ("pt", (1112, 790), 8), ("pt", (1370, 785), 8),                                 # khâu đồng
                ("pt", (1166, 770), 4), ("pt", (1296, 768), 3),                                 # răng dưới
                ("line", [(1150, 725), (1200, 740), (1250, 762)], 8)],                          # lưỡi
    },
}
# giới hạn phần trong đa giác (phần lọt ra ngoài lấy nhãn gần nhất); ép vùng
_LUNG2 = [(1200, 0), (300, 0), (300, 448), (380, 446), (450, 421), (500, 394), (550, 384), (600, 371), (700, 350), (800, 337),
          (850, 334), (900, 339), (945, 347), (1000, 346), (1200, 346)]   # vây chỉ ở trên đường lưng
_LUNG1 = [(1100, 0), (500, 0), (500, 480), (560, 466), (600, 425), (650, 402), (700, 390), (800, 384), (900, 386),
          (1000, 398), (1100, 398)]
CLAMP = {
    1: {"ham": [(868, 650), (900, 618), (945, 640), (1048, 612), (1095, 618), (1105, 668), (1112, 705), (1060, 728), (950, 732),
                (870, 720)],
        "vay1": _LUNG1, "vay2": _LUNG1, "vay3": _LUNG1,
        "tai_n": [(760, 340), (872, 340), (872, 456), (760, 456)], "tai_x": [(996, 340), (1090, 340), (1090, 440), (996, 440)]},
    2: {"chan_sn": [(100, 575), (395, 575), (420, 1000), (100, 1000)],
        "giap": [(620, 640), (640, 560), (700, 470), (780, 420), (860, 410), (910, 430), (905, 560), (870, 620), (800, 640)],
        "vay1": _LUNG2, "vay2": _LUNG2, "vay3": _LUNG2, "vay4": _LUNG2},
}
OVERRIDE = {1: {}, 2: {}}
NOT_SKIN = {2: ("giap",)}
# khe giấy trắng khép kín thật ra là nền (giữa ngà xa và mõm)
HOLES = {1: [], 2: [(1335, 725)]}
# lớp không kẻ nét mực dọc mép dải vẽ bù (má, cổ lộ ra khi hàm há: trong concept không có nét ở đó)
NO_LINE = {"than", "mieng"}
SHARE_INK = {"duoi", "vay", "chan_sx", "chan_tx", "chan_sn", "chan_tn", "giap"}
HULL_CLIP = {"than": ["than"], "chan_sx": ["than"], "chan_tx": ["than"]}
# lớp chỉ được mọc trong đa giác này (lòng miệng chỉ mọc trong khoảng giữa hai hàm, không lòi ra mép mõm, sau ngà xa)
RING_IN = {1: {"mieng": [(880, 590), (1060, 590), (1075, 650), (1080, 715), (880, 715)]},
           2: {"mieng": [(1095, 600), (1335, 600), (1345, 700), (1385, 800), (1385, 830), (1095, 830)]}}
# vùng không cho lớp mọc vào (thân mọc dưới hàm nhưng không lấp khoảng miệng: há thêm phải thấy lòng miệng phía sau)
RING_EXCL = {1: {"than": [[(925, 598), (1088, 598), (1088, 690), (925, 696)]]},
             2: {"than": [[(1120, 598), (1425, 598), (1425, 795), (1300, 805), (1150, 805), (1105, 760)],
                          [(1395, 560), (1490, 560), (1490, 830), (1395, 830)]]}}               # ngà xa
# điểm đất: đáy hình, x giữa bốn bàn chân
GROUND = {2: None}


def paths(k):
    base = os.path.join(HERE, "inbox", f"{CODE}_{k}")
    return base, os.path.join(base, "tai_ve", "L1_duyet.png"), os.path.join(base, "manh")


def disk(r):
    r = max(1, int(r))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def fg_mask(rgb, light=222, sat=32):
    mn, mx = rgb.min(2).astype(np.int16), rgb.max(2).astype(np.int16)
    lite = ((mn > light) & (mx - mn < sat)).astype(np.uint8)
    n, lab = cv2.connectedComponents(lite, connectivity=4)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bg = np.isin(lab, border[border > 0]) & (lite > 0)
    fg = (~bg).astype(np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, cl, st, _ = cv2.connectedComponentsWithStats(fg, connectivity=8)
    keep = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] >= 300]
    fg = np.isin(cl, keep).astype(np.uint8)
    f = cv2.GaussianBlur(cv2.erode(fg, np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 1.0) > 0.5
    return f.astype(np.uint8)


def load(k):
    _, src, _ = paths(k)
    rgb = np.array(Image.open(src).convert("RGB"))
    fg = fg_mask(rgb)
    mn, mx = rgb.min(2).astype(np.int16), rgb.max(2).astype(np.int16)
    lite = ((mn > 222) & (mx - mn < 32) & (fg > 0)).astype(np.uint8)
    _, cl = cv2.connectedComponents(lite, connectivity=4)
    for x, y in HOLES.get(k, []):
        c = cl[y, x]
        if c > 0:
            fg[cv2.dilate((cl == c).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0] = 0
    return rgb, fg


def fill_nearest(lab, need):
    src = (lab >= 0) & ~need
    if not need.any() or not src.any():
        return lab
    _, li = cv2.distanceTransformWithLabels((~src).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(src)
    out = lab.copy()
    out[need] = lab[ys, xs][li[need] - 1]
    return out


def poly_mask(shape, pg):
    m = np.zeros(shape[:2], np.uint8)
    cv2.fillPoly(m, [np.array(pg, np.int32)], 1)
    return m > 0


def seed_map(k, fg):
    names = PARTS[k]
    mk = np.full(fg.shape, -1, np.int32)
    inner = cv2.erode(fg, np.ones((5, 5), np.uint8)) > 0
    for i, n in enumerate(names):
        for s in SEEDS[k].get(n, []):
            m = np.zeros(fg.shape, np.uint8)
            if s[0] == "line":
                cv2.polylines(m, [np.array(s[1], np.int32)], False, 1, s[2])
            elif s[0] == "poly":
                cv2.fillPoly(m, [np.array(s[1], np.int32)], 1)
            else:
                cv2.circle(m, tuple(int(v) for v in s[1]), int(s[2]), 1, -1)
            mk[(m > 0) & inner] = i
    return mk


def is_ink(rgb):
    r, g, b = (rgb[:, :, c].astype(np.int16) for c in range(3))
    return (rgb.mean(2) < 88) & (b - r < 22)


def labels(k, rgb, fg):
    names = PARTS[k]
    lab = seed_map(k, fg)
    ink = is_ink(rgb) & (fg > 0)
    dom = (fg > 0) & ~ink
    k3 = np.ones((3, 3), np.uint8)
    for _ in range(900):
        miss = dom & (lab < 0)
        g = cv2.dilate(lab.astype(np.float32) + 1, k3).astype(np.int32) - 1
        upd = miss & (g >= 0)
        if not upd.any():
            break
        lab[upd] = g[upd]
    lab = fill_nearest(lab, (fg > 0) & (lab < 0))
    lab[fg == 0] = -1
    cnt = np.stack([cv2.boxFilter((lab == i).astype(np.float32), -1, (7, 7), normalize=False) for i in range(len(names))], 0)
    lab = np.where(fg > 0, cnt.argmax(0), -1).astype(np.int32)
    for n, polys in OVERRIDE[k].items():
        for pg in polys:
            lab[poly_mask(fg.shape, pg) & (fg > 0)] = names.index(n)
    for n, pg in CLAMP[k].items():
        i = names.index(n)
        out_ = (lab == i) & ~poly_mask(fg.shape, pg)
        lab[out_] = -1
        lab = fill_nearest(lab, out_ & (fg > 0))
    # đồ đồng (giáp vai) không có màu da xanh chàm: mảng da lọt vào trả về phần bên cạnh
    for n in NOT_SKIN.get(k, ()):
        i = names.index(n)
        r, g, b = (rgb[:, :, c].astype(np.int16) for c in range(3))
        skin = (b - r > 30) & (g < 140) & (lab == i)
        skin = cv2.morphologyEx(skin.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)) > 0
        nc, cl, st, _ = cv2.connectedComponentsWithStats(skin.astype(np.uint8), connectivity=8)
        drop = np.zeros_like(skin)
        for c in range(1, nc):
            if st[c, cv2.CC_STAT_AREA] > 150:
                drop |= cl == c
        drop = (cv2.dilate(drop.astype(np.uint8), disk(3)) > 0) & (lab == i)
        lab[drop] = -1
        tmp = lab.copy()
        tmp[tmp == i] = -2
        src = tmp >= 0
        if drop.any() and src.any():
            _, li = cv2.distanceTransformWithLabels((~src).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            ys, xs = np.nonzero(src)
            lab[drop] = lab[ys, xs][li[drop] - 1]
    # lòng miệng chỉ giữ màu hồng thịt; nét mực viền miệng, chân răng trả về đầu / hàm (hàm há thì nét môi đi theo môi)
    if "mieng" in names:
        i = names.index("mieng")
        r, g = rgb[:, :, 0].astype(np.int16), rgb[:, :, 1].astype(np.int16)
        bad = (lab == i) & ~((r - g > 45) & ~is_ink(rgb))
        lab[bad] = -1
        tmp = lab.copy()
        tmp[tmp == i] = -2
        src = tmp >= 0
        if bad.any() and src.any():
            _, li = cv2.distanceTransformWithLabels((~src).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            ys, xs = np.nonzero(src)
            lab[bad] = lab[ys, xs][li[bad] - 1]
    for i, n in enumerate(names):
        nc, cl, st, _ = cv2.connectedComponentsWithStats((lab == i).astype(np.uint8), connectivity=8)
        mn = 60 if n.startswith("giot") else 400
        big = max(range(1, nc), key=lambda c: st[c, cv2.CC_STAT_AREA]) if nc > 1 else 0
        for c in range(1, nc):
            if c != big and st[c, cv2.CC_STAT_AREA] < mn:
                lab[cl == c] = -1
    lab = fill_nearest(lab, (fg > 0) & (lab < 0))
    # giọt nước rời: cả cụm hình liền chứa hạt giống thuộc giọt (cả viền mực), không để mẩu viền dính sang đuôi
    ncc, cc = cv2.connectedComponents((fg > 0).astype(np.uint8), connectivity=8)
    for i, n in enumerate(names):
        if n.startswith("giot"):
            for s_ in SEEDS[k].get(n, []):
                x, y = (int(v) for v in s_[1])
                if cc[y, x] > 0:
                    lab[cc == cc[y, x]] = i
    return lab


COLS = np.array([[230, 60, 60], [60, 160, 230], [240, 190, 40], [120, 200, 80], [200, 90, 220], [40, 200, 190],
                 [250, 130, 30], [150, 100, 60], [90, 90, 230], [230, 90, 150], [100, 230, 160], [180, 180, 40],
                 [30, 120, 90], [200, 40, 120], [120, 60, 200], [60, 60, 60], [250, 200, 200], [20, 90, 160]], np.uint8)


def label_sheet(k, rgb, lab, out):
    names = PARTS[k]
    over = rgb.copy()
    for i in range(len(names)):
        m = lab == i
        over[m] = (0.45 * rgb[m] + 0.55 * COLS[i % len(COLS)]).astype(np.uint8)
    edge = cv2.morphologyEx(lab.astype(np.float32), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
    over[edge] = (0, 0, 0)
    im = Image.fromarray(over)
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
    for i, n in enumerate(names):
        ys, xs = np.nonzero(lab == i)
        if len(xs):
            d.text((int(xs.mean()) - 20, int(ys.mean()) - 9), n, fill=(0, 0, 0), font=f, stroke_width=2, stroke_fill=(255, 255, 255))
    im.save(out)


def premul_resize(rgba, w, h):
    a = rgba[:, :, 3:4].astype(np.float32) / 255.0
    pm = np.concatenate([rgba[:, :, :3].astype(np.float32) * a, a * 255.0], 2)
    sm = cv2.resize(pm, (w, h), interpolation=cv2.INTER_AREA)
    al = sm[:, :, 3:4] / 255.0
    rgb = np.where(al > 1e-3, sm[:, :, :3] / np.maximum(al, 1e-3), 0)
    return np.dstack([np.clip(rgb, 0, 255), np.clip(sm[:, :, 3], 0, 255)]).astype(np.uint8)


def fix_drop(rgb, own):
    """giọt nước: vệt sáng trắng trong giọt (concept vẽ bóng loáng) tô về màu lam trung vị của giọt."""
    mn = rgb.min(2).astype(np.int16)
    white = own & (mn > 200)
    inner = cv2.erode(own.astype(np.uint8), disk(5)) > 0
    white &= inner
    if white.any():
        blue = own & ~white & ~is_ink(rgb)
        med = np.median(rgb[blue], 0).astype(np.uint8)
        rgb = rgb.copy()
        rgb[(cv2.dilate(white.astype(np.uint8), disk(2)) > 0) & inner & own] = med
    return rgb


def texture_tile(rgb, core, med, size=48):
    """ô vân lát được: ô vuông nằm trọn trong vùng màu gần màu chính, phản chiếu bốn phía cho liền mép."""
    near = core & (np.abs(rgb.astype(np.int16) - med.astype(np.int16)).sum(2) < 60)
    for s in (size, 32, 20):
        inner = cv2.erode(near.astype(np.uint8), np.ones((s, s), np.uint8)) > 0
        ys, xs = np.nonzero(inner)
        if len(xs):
            j = len(xs) // 2
            y0, x0 = ys[j] - s // 2, xs[j] - s // 2
            p = rgb[y0:y0 + s, x0:x0 + s]
            return np.concatenate([np.concatenate([p, p[:, ::-1]], 1), np.concatenate([p[::-1], p[::-1, ::-1]], 1)], 0)
    return None


def build(k):
    base, src, out = paths(k)
    os.makedirs(out, exist_ok=True)
    rgb, fg = load(k)
    H, W = rgb.shape[:2]
    lab = labels(k, rgb, fg)
    names = PARTS[k]
    label_sheet(k, rgb, lab, os.path.join(out, "nhan.png"))
    Image.fromarray((fg > 0).astype(np.uint8) * 255).save(os.path.join(out, "fg.png"))
    ys, xs = np.nonzero(fg)
    yg = int(ys.max())
    feet = [n for n in names if n.startswith("chan")]
    fm = np.isin(lab, [names.index(n) for n in feet]) & (np.arange(H)[:, None] > yg - 0.06 * H)
    xg = float(np.nonzero(fm)[1].mean()) if fm.any() else float(xs.mean())
    ks = KS[k]

    def S(x, y):
        return ((x - xg) * ks, (yg - y) * ks)

    above = set()
    specs = []
    for name, ps, grow in reversed(LAYERS[k]):
        specs.append((name, ps, grow, set(above)))
        above |= set(ps)
    specs.reverse()
    info = {"ks": ks, "ground": [xg, yg], "size": [W, H], "parts": names, "layers": []}
    dbg = []
    for name, ps, grow, abv in specs:
        ids = [names.index(p) for p in ps]
        own = np.isin(lab, ids) & (fg > 0)
        if name in SHARE_INK and own.any():   # lớp sau lấy luôn nét mực giáp ranh với lớp khác (nét viền chung): cử động không mất viền
            ink = is_ink(rgb) & (fg > 0)
            ext = (cv2.dilate((own & ~ink).astype(np.uint8), disk(5)) > 0) & ink & ~own
            for pg in RING_EXCL.get(k, {}).get(name, []):
                ext &= ~poly_mask(fg.shape, pg)
            own = own | ext
        if not own.any():
            print(f"  {name}: TRỐNG")
            continue
        ring = np.zeros_like(own)
        if grow and abv:
            into = np.isin(lab, [names.index(p) for p in abv if not p.startswith("giot")]) & (fg > 0)   # giọt rời: không mọc vào
            ring = (cv2.dilate(own.astype(np.uint8), disk(grow)) > 0) & into & ~own
            for pg in RING_EXCL.get(k, {}).get(name, []):
                ring &= ~poly_mask(fg.shape, pg)
            if name in RING_IN.get(k, {}):
                ring &= poly_mask(fg.shape, RING_IN[k][name])
            if name in HULL_CLIP:   # chỉ mọc trong bao lồi thân (không mọc xuống phần chân thòng dưới bụng)
                hp = np.isin(lab, [names.index(p) for p in HULL_CLIP[name]]) & (fg > 0)
                hull = cv2.convexHull(np.stack(np.nonzero(hp)[::-1], 1).astype(np.int32))
                hm = np.zeros(own.shape, np.uint8)
                cv2.fillConvexPoly(hm, hull, 1)
                ring &= cv2.erode(hm, disk(6)) > 0
        dom = own | ring
        if ring.any():
            sm = cv2.morphologyEx(dom.astype(np.uint8), cv2.MORPH_CLOSE, disk(6))
            sm = cv2.morphologyEx(sm, cv2.MORPH_OPEN, disk(8))
            dom = ((sm > 0) & (fg > 0)) | own
        dom = (cv2.morphologyEx(dom.astype(np.uint8), cv2.MORPH_CLOSE, disk(2)) > 0) & (fg > 0)
        src_rgb = fix_drop(rgb, own) if name.startswith("giot") else rgb
        tex = src_rgb.copy()
        if (dom & ~own).any():
            work = src_rgb.copy()
            core = own & ~is_ink(src_rgb)
            core = cv2.erode(core.astype(np.uint8), disk(1)) > 0          # bỏ mép nhoè của nét mực
            med = np.median(src_rgb[core if core.any() else own], 0).astype(np.uint8)
            work[~core] = med                                              # nét mực, ngoài lớp: màu chính, khỏi kéo vệt nâu
            fill = (dom & ~core).astype(np.uint8) * 255
            tex = cv2.inpaint(work, fill, 9, cv2.INPAINT_TELEA)
            tex = cv2.GaussianBlur(tex, (0, 0), 3.0)
            tile = texture_tile(src_rgb, core, med)
            if tile is not None:                                           # vân sáp thật của lớp lát lên phần vẽ bù
                th, tw = tile.shape[:2]
                tiled = np.tile(tile, (H // th + 1, W // tw + 1, 1))[:H, :W].astype(np.float32)
                tex = np.clip(tex.astype(np.float32) + 0.9 * (tiled - tiled.reshape(-1, 3).mean(0)), 0, 255).astype(np.uint8)
            edge = dom & (cv2.erode(dom.astype(np.uint8), disk(3)) == 0)
            inside = cv2.erode(fg, disk(5)) > 0
            line_ = edge & inside & ~own & (name not in NO_LINE)
            soft = np.maximum(cv2.GaussianBlur(line_.astype(np.float32), (0, 0), 0.8), line_.astype(np.float32))[..., None]
            tex = (tex * (1 - soft) + np.array(INK, np.float32) * soft).astype(np.uint8)
            tex[own] = src_rgb[own]
        a = cv2.GaussianBlur(dom.astype(np.float32), (0, 0), 0.8)
        yy, xx = np.nonzero(a > 0.02)
        x0, y0 = max(0, xx.min() - 3), max(0, yy.min() - 3)
        x1, y1 = min(W, xx.max() + 4), min(H, yy.max() + 4)
        rgba = np.dstack([tex, np.clip(a * 255, 0, 255).astype(np.uint8)])[y0:y1, x0:x1]
        w2, h2 = max(2, round((x1 - x0) * ks)), max(2, round((y1 - y0) * ks))
        small = premul_resize(rgba, w2, h2)
        # nhãn phần trong miền lớp (dải mọc thêm lấy nhãn phần gần nhất của chính lớp)
        llab = np.where(own, lab, -1)
        llab = fill_nearest(llab, dom & ~own)
        llab[~dom] = -1
        lsm = cv2.resize(llab[y0:y1, x0:x1].astype(np.int16), (w2, h2), interpolation=cv2.INTER_NEAREST)
        lsm = np.where(lsm >= 0, lsm, 255).astype(np.uint8)
        Image.fromarray(small).save(os.path.join(out, name + ".png"))
        Image.fromarray(lsm).save(os.path.join(out, name + "_lab.png"))
        rx, ry = S(x0, y0)
        info["layers"].append({"name": name, "parts": ps, "box": [int(x0), int(y0), int(x1), int(y1)], "w": w2, "h": h2,
                               "rig_tl": [round(rx, 3), round(ry, 3)], "sx": (x1 - x0) / w2, "sy": (y1 - y0) / h2,
                               "grow_px": int(ring.sum())})
        dbg.append((name, rgba, (x0, y0)))
        print(f"  {name:8s} {w2}x{h2} px atlas, mọc thêm {int(ring.sum())} px concept")
    json.dump(info, open(os.path.join(out, "cat.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    # tờ lớp trên nền xám
    sheet = np.full((H, W, 3), 150, np.uint8)
    comp = sheet.copy()
    for name, rgba, (x0, y0) in dbg:
        h, w = rgba.shape[:2]
        al = rgba[:, :, 3:4] / 255.0
        comp[y0:y0 + h, x0:x0 + w] = (rgba[:, :, :3] * al + comp[y0:y0 + h, x0:x0 + w] * (1 - al)).astype(np.uint8)
    cfg = comp.astype(np.int16) - 150
    rec = (np.abs(cfg).sum(2) > 0)
    iou = float((rec & (fg > 0)).sum() / max(1, (rec | (fg > 0)).sum()))
    Image.fromarray(np.concatenate([np.where(fg[..., None] > 0, rgb, 150).astype(np.uint8), comp], 1)).save(os.path.join(out, "lop.png"))
    # từng lớp riêng (soi dải vẽ bù)
    tiles = []
    for name, rgba, _ in dbg:
        t = np.full(rgba.shape[:2] + (3,), 150, np.uint8)
        al = rgba[:, :, 3:4] / 255.0
        t = (rgba[:, :, :3] * al + t * (1 - al)).astype(np.uint8)
        tiles.append(Image.fromarray(t))
    tw = 1600
    x = y = rowh = 0
    pos = []
    for t in tiles:
        if x + t.width > tw:
            x, y, rowh = 0, y + rowh + 10, 0
        pos.append((x, y))
        x += t.width + 10
        rowh = max(rowh, t.height)
    canvas = Image.new("RGB", (tw, y + rowh + 2), (120, 120, 120))
    for t, p in zip(tiles, pos):
        canvas.paste(t, p)
    canvas.save(os.path.join(out, "lop_rieng.png"))
    print(f"dạng {k}: IoU ghép lớp / concept = {iou:.3f}; đất ({xg:.0f}, {yg}); ks {ks}")


if __name__ == "__main__":
    build(int(sys.argv[1]) if len(sys.argv) > 1 else 2)
