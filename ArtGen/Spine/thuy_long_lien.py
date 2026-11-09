# -*- coding: utf-8 -*-
"""Thủy Long dựng từ MỘT ảnh liền (2026-11-08). Bản ghép 17 mảnh GPT vẽ rời bị người dùng chê lỗi nhiều (khe trắng giữa đầu,
mào, cổ; nắm tay vẽ lệch; viền sticker thắt vòng), dặn "không cần tách nhiều bộ phận, gen liền cũng được". Giữ nguyên
animation của thuy_long.py (tên xương như cũ), chỉ thay nguồn hình:

- Concept trọn con (ảnh liền) là hình duy nhất. Vùng từng phần (đầu, thân, tay, chân, đuôi, vũ khí...) tìm bằng watershed
  trên chính ảnh: hạt giống là mảnh đã khớp cũ co lại (dạng 1, 2) hoặc đường xương kẻ tay (dạng 3), ranh giới tự bám nét mực.
- Gộp phần thành ít lớp (đuôi, tay sau, chân sau, chân trước, thân + đầu + mào, vải, tay trước + vũ khí; dạng 3 thêm áo
  choàng). Lớp dưới mọc thêm dưới lớp trên, dải đó vẽ bù từ màu chính lớp, nên khi lớp trên cử động không lộ nền.
- Mỗi lớp một lưới; trọng số theo chuỗi xương từng phần (khoảng cách đi trong hình), phần cứng (nắm tay, bàn chân, vũ khí,
  giáp vai) bám 100%.

    D:/spine-venv/Scripts/python -I ArtGen/Spine/thuy_long_lien.py nhan <k> | rig <k> | all | show <k> <clip> t1,t2 [follow]
"""
import json
import math
import os
import pickle
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import longrig as L  # noqa: E402
import rig as riglib  # noqa: E402
import thuy_long as T  # noqa: E402

H = T.H
INK = (52, 36, 28)  # màu nét mực nâu sẫm của ảnh GPT


# cấu hình theo tướng (tướng khác dùng lại bộ dựng này thì đổi CFG, LAYERS, JD, MARKD, OVERRIDE, CLAMP: xem tam_tay.py)
CFG = {"code": T.code, "base": T.base, "clips": lambda ctx: T.clips_of(ctx), "evolve": lambda *a: T.evolve(*a),
       "beam": {1: 0.8, 2: 1.0, 3: 1.25}, "src": None}


def code(k):
    return CFG["code"](k)


def src(k):
    if CFG["src"]:
        return CFG["src"](k)
    return os.path.join(T.base(k), "tai_ve", "L1_lien.png") if k == 3 else os.path.join(T.base(k), "L1_duyet.png")


def out_dir(k):
    return os.path.join(CFG["base"](k), "rig_lien")


# lớp sau -> trước: (tên slot, [phần sau -> trước trong lớp], px mọc thêm dưới các lớp trên, tỉ lệ ảnh)
LAYERS = {k: [("tail", ["tail"], 22), ("arm_b", ["arm_b", "fist_b"], 34), ("leg_b", ["leg_b", "foot_b"], 30),
              ("leg_f", ["leg_f", "foot_f"], 30), ("crest", ["crest"], 30), ("body", ["torso", "head"], 40),
              ("cloth", ["cloth"], 16), ("arm_f", ["arm_f", "shoulder", "weapon", "hand_f"], 0)] for k in (1, 2)}
# dạng 3: giáp vai trái to đè lên ngực nên tay sau vẽ trên thân (thân mọc thêm dưới giáp vai)
LAYERS[3] = [("cape", ["cape"], 44), ("tail", ["tail"], 24), ("leg_b", ["leg_b", "foot_b"], 30),
             ("leg_f", ["leg_f", "foot_f"], 30), ("crest", ["crest"], 30), ("body", ["torso", "head"], 44),
             ("arm_b", ["arm_b", "fist_b", "shoulder_b"], 0),
             ("cloth", ["cloth"], 16), ("arm_f", ["arm_f", "shoulder", "weapon", "hand_f"], 0)]

# chuỗi: phần -> (xương, cha, độ hoà quanh khớp theo s, độ hoà vào cha ở gốc)
CHAINS = {"torso": (["spine1", "spine2", "chest"], "hip", 0.12, 0.0),
          "head": (["neck", "head"], "chest", 0.12, 0.16),
          "crest": (["crest1", "crest2", "crest3"], "head", 0.12, 0.3),
          "arm_b": (["arm_b1", "arm_b2"], "chest", 0.12, 0.12),
          "arm_f": (["arm_f1", "arm_f2"], "chest", 0.12, 0.12),
          "leg_b": (["leg_b1", "leg_b2"], "hip", 0.12, 0.08),
          "leg_f": (["leg_f1", "leg_f2"], "hip", 0.12, 0.08),
          "tail": (["tail1", "tail2", "tail3", "tail4"], "hip", 0.1, 0.1),
          "cloth": (["cloth1", "cloth2", "cloth3"], "spine1", 0.14, 0.15),
          "cape": (["cape1", "cape2", "cape3", "cape4"], "chest", 0.12, 0.2)}
RIGID = {"fist_b": "fist_b", "hand_f": "hand_f", "weapon": "weapon", "shoulder": "arm_f1",
         "shoulder_b": [("chest", 0.65), ("arm_b1", 0.35)],  # giáp vai trái to (dạng 3): chủ yếu theo ngực, tay xoay bên dưới
         "foot_b": "foot_b", "foot_f": "foot_f"}

# ép vùng sau watershed (đa giác toạ độ concept): phần -> [đa giác]
OVERRIDE = {1: {"leg_b": [[(368, 1128), (392, 1136), (446, 1060), (470, 1000), (478, 935), (460, 930), (440, 990),
                           (400, 1060), (368, 1100)]],
                "weapon": [[(698, 828), (722, 836), (700, 885), (688, 910), (668, 918), (655, 900), (668, 860), (684, 832)]],
                "head": [[(380, 120), (415, 150), (455, 170), (495, 200), (515, 235), (492, 245), (455, 210), (410, 180),
                          (385, 150)]]},  # sừng sau
            2: {"fist_b": [[(140, 835), (150, 890), (185, 930), (240, 935), (272, 905), (275, 860), (255, 830), (225, 815),
                            (190, 822), (150, 822)]],
                "head": [[(360, 110), (395, 140), (430, 160), (470, 190), (500, 235), (480, 250), (445, 210), (400, 170),
                          (365, 140)]],  # sừng sau
                "torso": [[(370, 440), (430, 415), (460, 430), (455, 490), (380, 500)]]},  # cổ giáp bên trái
            3: {}}

# khoanh vùng: phần chỉ được nằm trong đa giác của nó (hạt giống mảnh khớp cũ to hơn hình vẽ, vải ăn sang dải chân hai bên
# rồi kéo dải chân bay theo); pixel lấn ra ngoài lấy nhãn phần khác gần nhất
CLAMP = {1: {"cloth": [(462, 800), (600, 800), (604, 1000), (612, 1140), (528, 1186), (446, 1146), (458, 1000)]},
         2: {"cloth": [(398, 790), (540, 790), (544, 1000), (556, 1152), (470, 1228), (390, 1162), (396, 1000)]},
         3: {"cloth": [(482, 790), (622, 790), (614, 1130), (556, 1208), (490, 1136)]}}


def fill_nearest(lab, need):
    """pixel need lấy nhãn của pixel có nhãn (>= 0, không thuộc need) gần nhất."""
    src = (lab >= 0) & ~need
    if not need.any() or not src.any():
        return lab
    d, li = cv2.distanceTransformWithLabels((~src).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    ys, xs = np.nonzero(src)  # nhãn pixel nguồn đánh theo thứ tự quét, từ 1
    srclab = lab[ys, xs]
    out = lab.copy()
    out[need] = srclab[li[need] - 1]
    return out


# dạng 3 (ảnh vẽ lại, không có mảnh khớp cũ): khớp đọc trên ảnh kẻ lưới (toạ độ L1_lien.png 1024x1536)
J3 = {"top": 105.0,  # đỉnh sừng (lưỡi đao cao hơn đầu, không tính)
      "bones": {"hip": (510, 900), "spine1": (510, 900), "spine2": (512, 760), "chest": (512, 620), "neck": (510, 480),
                "head": (528, 405), "crest1": (450, 285), "crest2": (380, 325), "crest3": (318, 375),
                "arm_b1": (300, 560), "arm_b2": (215, 700), "fist_b": (205, 850),
                "arm_f1": (660, 590), "arm_f2": (700, 700), "hand_f": (782, 745), "weapon": (830, 722),
                "leg_b1": (372, 940), "leg_b2": (265, 1150), "foot_b": (235, 1320),
                "leg_f1": (650, 940), "leg_f2": (690, 1170), "foot_f": (690, 1325),
                "tail1": (330, 1062), "tail2": (212, 1160), "tail3": (92, 1170), "tail4": (36, 1062),
                "cloth1": (552, 800), "cloth2": (552, 940), "cloth3": (554, 1070),
                "cape1": (505, 560), "cape2": (500, 800), "cape3": (485, 1010), "cape4": (475, 1170)},
      "tips": {"tail": (88, 900), "crest": (262, 425), "cloth": (556, 1200), "cape": (470, 1345)},
      "tip": (822, 48)}
MARK3 = {  # hạt giống (toạ độ L1_lien.png): ("line", [điểm], dày) | ("poly", [điểm])
    "cape": [("line", [(350, 1262), (450, 1272), (560, 1262), (620, 1250)], 22), ("line", [(55, 1290), (160, 1285)], 14),
             ("line", [(752, 1150), (760, 1290)], 10), ("line", [(830, 1230), (870, 1300)], 10),
             ("line", [(302, 720), (306, 950)], 12)],
    "tail": [("line", [(278, 1112), (230, 1150), (120, 1180), (52, 1110), (45, 1000), (82, 930), (100, 892)], 14),
             ("line", [(200, 1050), (262, 1062)], 8)],
    "leg_b": [("line", [(360, 945), (300, 1060), (262, 1150)], 26), ("line", [(262, 1175), (242, 1290)], 20)],
    "foot_b": [("line", [(232, 1332), (182, 1400), (132, 1430)], 18), ("line", [(232, 1342), (258, 1430)], 14)],
    "leg_f": [("line", [(660, 945), (690, 1060), (690, 1160)], 26), ("line", [(692, 1192), (692, 1310)], 20)],
    "foot_f": [("line", [(690, 1342), (762, 1410), (822, 1430)], 16)],
    "crest": [("line", [(300, 330), (380, 320), (450, 300)], 10), ("line", [(300, 400), (385, 405)], 10),
              ("line", [(470, 170), (520, 220), (556, 250)], 8)],
    "torso": [("poly", [(420, 560), (640, 560), (640, 720), (430, 720)]), ("line", [(450, 770), (600, 770)], 14),
              ("line", [(330, 880), (450, 860)], 14), ("line", [(640, 860), (720, 900)], 12)],
    "head": [("poly", [(480, 300), (600, 290), (640, 350), (560, 410), (480, 380)]),
             ("line", [(300, 160), (330, 230), (400, 240), (450, 250)], 10), ("line", [(600, 140), (622, 200), (600, 240)], 10),
             ("line", [(500, 420), (510, 480)], 16)],
    "cloth": [("line", [(550, 805), (552, 1150)], 30)],
    "arm_b": [("line", [(250, 625), (215, 690), (200, 770), (205, 835)], 20)],
    "fist_b": [("line", [(190, 892), (240, 902)], 30)],
    "shoulder_b": [("poly", [(185, 525), (300, 455), (415, 475), (415, 555), (300, 605), (195, 605)])],
    "arm_f": [("line", [(672, 642), (700, 700), (748, 740)], 18)],
    "shoulder": [("poly", [(605, 495), (680, 485), (738, 560), (720, 618), (642, 618)])],
    "weapon": [("poly", [(800, 30), (880, 80), (970, 200), (1012, 365), (910, 475), (800, 455), (785, 240), (820, 170)]),
               ("poly", [(822, 470), (862, 470), (845, 680), (806, 900), (804, 1340), (780, 1340), (778, 900), (812, 680)])],
    "hand_f": [("line", [(802, 702), (850, 740)], 30)],
}


LINEAR_Y = {"cape"}    # phần chuỗi có s theo độ cao (áo choàng lộ rời rạc), không theo đường đi trong hình
FULL_SHEET = {"cape"}  # phần dựng cả tấm sau người (bao lồi các mảnh lộ ra)
WARM_FIX = {"cape"}    # phần không có màu đồng, kem: mẩu đồng lọt vào trả về phần bên cạnh (áo choàng Thủy Long)
JD = {3: J3}        # dạng -> khớp kẻ tay (dạng không có thì lấy khớp từ rig mảnh cũ)
MARKD = {3: MARK3}  # dạng -> hạt giống kẻ tay (dạng không có thì lấy mảnh khớp cũ)


# ---------------------------------------------------------------- ảnh, vùng
def load(k):
    rgb = np.array(Image.open(src(k)).convert("RGB"))
    fg = riglib.fg_mask(rgb)
    # đường đất mảnh dưới chân: mở theo chiều dọc ở dải đáy (giữ móng vuốt dày), xoá khỏi ảnh rồi tính lại nền (đường đất
    # khép kín khe giữa hai chân làm khe trắng bị coi là hình)
    rows = np.where(fg.any(1))[0]
    band = np.zeros_like(fg)
    band[max(0, rows.max() - 60):] = 1
    dark = (rgb.mean(2) < 205).astype(np.uint8)
    op = cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((13, 1), np.uint8))
    white = rgb.min(2) > 215
    up = np.zeros_like(white)
    dn = np.zeros_like(white)
    for o in (4, 5, 6, 7):  # nét đất: trên và dưới đều là giấy trắng (đế bàn chân thì trên là màu chân)
        up[o:] |= white[:-o]
        dn[:-o] |= white[o:]
    line = (dark > 0) & (op == 0) & (band > 0) & up & dn
    rgb = rgb.copy()
    rgb[cv2.dilate(line.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0] = 255
    fg = riglib.fg_mask(rgb)
    # khe trắng lớn khép kín (giữa tay và thân, đuôi và chân): cũng là nền
    mn, mx = rgb.min(2).astype(np.int16), rgb.max(2).astype(np.int16)
    lite = ((mn > 222) & (mx - mn < 32) & (fg > 0)).astype(np.uint8)
    n, cl, st, _ = cv2.connectedComponentsWithStats(lite, connectivity=4)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 3000:
            fg[cv2.dilate((cl == i).astype(np.uint8), np.ones((3, 3), np.uint8)) > 0] = 0
    fg = riglib.biggest(fg > 0, 400).astype(np.uint8)
    # viền mượt như bộ cắt cũ
    f = cv2.GaussianBlur(cv2.erode(fg, np.ones((3, 3), np.uint8)).astype(np.float32), (0, 0), 1.2) > 0.5
    return rgb, f.astype(np.uint8)


def parts_of(k):
    return [p for _, ps, _ in LAYERS[k] for p in ps]


def markers_placed(k, fg):
    """hạt giống watershed từ mảnh đã khớp ở bản cũ (co 8 px), mảnh vẽ sau đè mảnh vẽ trước."""
    P = riglib.paths(code(k))
    pl = json.load(open(os.path.join(P["rig"], "placed.json")))
    W1, H1 = pl["ref_size"]
    names = parts_of(k)
    mk = np.zeros(fg.shape, np.int32)
    for n in T.DRAW[k]:
        if n not in names:
            continue
        im = np.array(Image.open(os.path.join(P["rig"], "placed", n + ".png")))
        m = riglib.placed_mask(pl["parts"][n], im, W1, H1)
        m = cv2.erode(m, np.ones((17, 17), np.uint8)) & cv2.erode(fg, np.ones((9, 9), np.uint8))
        mk[m > 0] = 2 + names.index(n)
    return mk


def markers_drawn(k, fg):
    """hạt giống từ đường xương / vùng kẻ tay (MARK3: phần -> [("line", [(x, y)...], dày) | ("poly", [(x, y)...])])."""
    names = parts_of(k)
    mk = np.zeros(fg.shape, np.int32)
    inner = cv2.erode(fg, np.ones((7, 7), np.uint8))
    for n in names:  # thứ tự lớp: phần trước đè phần sau
        for kind, pts, *r in MARKD[k].get(n, []):
            m = np.zeros(fg.shape, np.uint8)
            if kind == "line":
                cv2.polylines(m, [np.array(pts, np.int32)], False, 1, r[0] if r else 9)
            else:
                cv2.fillPoly(m, [np.array(pts, np.int32)], 1)
            mk[(m > 0) & (inner > 0)] = 2 + names.index(n)
    return mk


def labels(k, rgb, fg):
    """vùng từng phần: loang đều (mỗi bước 1 px) từ hạt giống trong vùng màu, nét mực là tường (watershed loang dọc theo nét
    mực nên kéo viền chân theo vải); rồi nét mực lấy nhãn vùng màu gần nhất: viền giữa phần và nền thuộc phần, viền giữa hai
    phần chia đôi. Trả mảng nhãn (-1 nền, i = parts_of(k)[i])."""
    mk = markers_drawn(k, fg) if k in MARKD else markers_placed(k, fg)
    names = parts_of(k)
    lab = np.where(mk >= 2, mk - 2, -1).astype(np.int32)
    ink = (rgb.mean(2) < 72) & (fg > 0)  # chỉ nét mực nâu sẫm, vằn xanh đậm (thép sẫm #4A5866 không phải nét)
    dom = (fg > 0) & ~ink
    k3 = np.ones((3, 3), np.uint8)
    for _ in range(600):
        miss = dom & (lab < 0)
        g = cv2.dilate(lab.astype(np.float32) + 1, k3).astype(np.int32) - 1
        upd = miss & (g >= 0)
        if not upd.any():
            break
        lab[upd] = g[upd]
    lab = fill_nearest(lab, (fg > 0) & (lab < 0))  # nét mực, ô kín chưa loang tới: nhãn gần nhất (không lấy nhãn số lớn)
    for n, polys in OVERRIDE.get(k, {}).items():
        for pg in polys:
            lab[riglib.poly_mask(fg.shape, pg)] = names.index(n)
    lab[fg == 0] = -1
    # dọn: mỗi pixel theo nhãn chiếm đa số ô 7x7 (sợi viền mảnh 1-3 px về phần bên cạnh, khỏi bị lớp khác kéo theo thành
    # đường kẻ), mẩu rời < 500 px của một nhãn bỏ đi cho nhãn bên cạnh lấp
    cnt = np.stack([cv2.boxFilter((lab == i).astype(np.float32), -1, (7, 7), normalize=False) for i in range(len(names))], 0)
    lab = np.where(fg > 0, cnt.argmax(0), -1).astype(np.int32)
    for n, polys in OVERRIDE.get(k, {}).items():
        for pg in polys:
            lab[riglib.poly_mask(fg.shape, pg) & (fg > 0)] = names.index(n)
    for i in range(len(names)):
        nc, cl, st, _ = cv2.connectedComponentsWithStats((lab == i).astype(np.uint8), connectivity=8)
        for c in range(1, nc):
            if st[c, cv2.CC_STAT_AREA] < 500:
                lab[cl == c] = -1
    # sừng (kem) và vòng đồng trên sừng lọt vào vùng mào: về đầu (mào lắc, sừng thì không)
    if "crest" in names and "head" in names:
        r, g, b = (rgb[:, :, c].astype(np.int16) for c in range(3))
        cream = (r > 185) & (g > 170) & (b > 130) & (r >= b + 12)
        bronze = (r > 150) & (g > 95) & (g < 175) & (b < 110) & (r > g + 25)
        hc = (lab == names.index("crest")) & (cream | bronze)
        hc = cv2.morphologyEx(hc.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0
        lab[hc & (lab == names.index("crest"))] = names.index("head")
    # áo choàng không có viền đồng, kem: mẩu đồng (mép giáp hông) lọt vào áo choàng trả về phần bên cạnh
    if "cape" in names and "cape" in WARM_FIX:
        r, g, b = (rgb[:, :, c].astype(np.int16) for c in range(3))
        warm = (r > 150) & (r > b + 40) & (lab == names.index("cape"))
        warm = cv2.dilate(warm.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        warm &= lab == names.index("cape")
        lab[warm] = -1
        tmp = lab.copy()
        tmp[tmp == names.index("cape")] = -2  # nguồn: mọi phần trừ áo choàng
        src = tmp >= 0
        if src.any() and warm.any():
            d, li = cv2.distanceTransformWithLabels((~src).astype(np.uint8), cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
            ys, xs = np.nonzero(src)
            lab[warm] = lab[ys, xs][li[warm] - 1]
    for n, pg in CLAMP.get(k, {}).items():
        i = names.index(n)
        out_ = (lab == i) & ~riglib.poly_mask(fg.shape, pg)
        lab[out_] = -1
        lab = fill_nearest(lab, out_ & (fg > 0))
    # pixel hình chưa có nhãn (mẩu vụn đã bỏ, nền tràn vào): nhãn gần nhất
    return fill_nearest(lab, (fg > 0) & (lab < 0))


def label_sheet(k, rgb, lab, path, extra=None):
    col = np.array([[230, 60, 60], [60, 160, 230], [240, 190, 40], [120, 200, 80], [200, 90, 220], [40, 200, 190],
                    [250, 130, 40], [130, 130, 250], [160, 90, 60], [90, 220, 140], [250, 90, 160], [100, 100, 100],
                    [200, 200, 60], [60, 90, 160], [170, 40, 120], [20, 120, 60]])
    over = rgb.astype(np.float32).copy()
    m = lab >= 0
    over[m] = over[m] * 0.45 + col[lab[m] % len(col)] * 0.55
    edge = cv2.morphologyEx((lab + 1).astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)) > 0
    over[edge] = (0, 0, 0)
    im = Image.fromarray(over.astype(np.uint8))
    d = ImageDraw.Draw(im)
    F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
    for i, n in enumerate(parts_of(k)):
        ys, xs = np.nonzero(lab == i)
        if len(xs):
            d.text((int(np.median(xs)) - 20, int(np.median(ys)) - 10), n, fill=(0, 0, 0), font=F)
    if extra:
        for (x, y) in extra:
            d.ellipse([x - 6, y - 6, x + 6, y + 6], outline=(255, 0, 160), width=3)
    im.resize((im.width // 2, im.height // 2), Image.LANCZOS).save(path)


# ---------------------------------------------------------------- khoảng cách đi trong hình (nhanh)
def geo(mask, seed, maxit=4000):
    """khoảng cách loang 8 hướng trong mask từ điểm seed (điểm ngoài mask: lấy điểm trong gần nhất)."""
    ys, xs = np.nonzero(mask)
    x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    m = mask[y0:y1, x0:x1] > 0
    sx, sy = seed[0] - x0, seed[1] - y0
    j = int(np.argmin((xs - x0 - sx) ** 2 + (ys - y0 - sy) ** 2))
    d = np.full(m.shape, np.inf, np.float32)
    cur = np.zeros(m.shape, bool)
    cur[ys[j] - y0, xs[j] - x0] = True
    d[cur] = 0
    k = np.ones((3, 3), np.uint8)
    for i in range(1, maxit):
        nb = (cv2.dilate(cur.astype(np.uint8), k) > 0) & m & ~cur
        if not nb.any():
            break
        d[nb] = i
        cur |= nb
    out = np.full(mask.shape, np.inf, np.float32)
    out[y0:y1, x0:x1] = d
    return out


def at(D, p):
    """giá trị D tại p (p lọt ngoài vùng hữu hạn: điểm hữu hạn gần nhất)."""
    x, y = int(round(p[0])), int(round(p[1]))
    if 0 <= y < D.shape[0] and 0 <= x < D.shape[1] and np.isfinite(D[y, x]):
        return float(D[y, x])
    ys, xs = np.nonzero(np.isfinite(D))
    j = int(np.argmin((xs - x) ** 2 + (ys - y) ** 2))
    return float(D[ys[j], xs[j]])


def chain_w(s, bones, cuts, parent=None, blend=0.12, pb=0.0):
    k = int(sum(s >= c for c in cuts))
    ws = {bones[k]: 1.0}
    for j, c in enumerate(cuts):
        lo = cuts[j - 1] if j > 0 else 0.0
        hi = cuts[j + 1] if j + 1 < len(cuts) else 1.0
        b = min(blend, 0.45 * (c - lo), 0.45 * (hi - c))
        if b > 1e-4 and abs(s - c) < b:
            t = L.smooth01((s - c + b) / (2 * b))
            ws = {bones[j]: 1 - t, bones[j + 1]: t}
    if parent and pb > 0 and s < pb:
        wp = 0.5 * (1 - L.smooth01(s / pb))
        ws = {b_: w * (1 - wp) for b_, w in ws.items()}
        ws[parent] = ws.get(parent, 0) + wp
    ws = {b_: w for b_, w in ws.items() if w > 0.01}
    tot = sum(ws.values())
    return [(b_, w / tot) for b_, w in ws.items()]


# ---------------------------------------------------------------- khớp
def joints_from_old(k):
    """dạng 1, 2: vị trí xương lấy đúng từ rig cũ (cùng phép đổi toạ độ concept -> rig) để clip chạy y như trước."""
    Ro, ctx = T.build_rig(k)
    ks = H / (ctx.ground - ctx.top)
    tf = {"ks": ks, "feet_x": ctx.feet_x, "ground": ctx.ground, "top": ctx.top}

    def px(p):
        return (p[0] / ks + ctx.feet_x, ctx.ground - p[1] / ks)
    J = {b["name"]: px((b["wx"], b["wy"])) for b in Ro.bones}
    tips = {n: px(ctx.info[n + "_tip"]) for n in ("tail", "crest", "cloth", "cape") if n + "_tip" in ctx.info}
    J["tip"] = px(ctx.info["tip"])
    return J, tips, tf, Ro


def joints_drawn(k, fg):
    """dạng 3: khớp kẻ tay J3 (toạ độ concept); phép đổi toạ độ theo đỉnh đầu và đất."""
    J3 = JD[k]
    J = dict(J3["bones"])
    tips = dict(J3["tips"])
    J["tip"] = J3["tip"]
    rows = np.where(fg.any(1))[0]
    ground = J3.get("ground", float(rows.max()) - 8)
    top = J3.get("top", float(rows.min()))
    feet_x = (J["foot_b"][0] + J["foot_f"][0]) / 2
    return J, tips, {"ks": H / (ground - top), "feet_x": feet_x, "ground": ground, "top": top}, None


# ---------------------------------------------------------------- dựng rig
PARENT = {"move": "root", "shadow": "root", "hip": "move", "spine1": "hip", "spine2": "spine1", "chest": "spine2",
          "neck": "chest", "head": "neck", "crest1": "head", "crest2": "crest1", "crest3": "crest2",
          "arm_b1": "chest", "arm_b2": "arm_b1", "fist_b": "arm_b2", "arm_f1": "chest", "arm_f2": "arm_f1",
          "hand_f": "arm_f2", "weapon": "hand_f", "leg_b1": "hip", "leg_b2": "leg_b1", "foot_b": "leg_b2",
          "leg_f1": "hip", "leg_f2": "leg_f1", "foot_f": "leg_f2", "tail1": "hip", "tail2": "tail1", "tail3": "tail2",
          "tail4": "tail3", "cloth1": "spine1", "cloth2": "cloth1", "cloth3": "cloth2", "cape1": "chest", "cape2": "cape1",
          "cape3": "cape2", "cape4": "cape3"}


def premul_resize(rgba, w, h):
    a = rgba[:, :, 3:4].astype(np.float32) / 255
    rgb = rgba[:, :, :3].astype(np.float32) * a
    rs = cv2.resize(np.dstack([rgb, a * 255]), (w, h), interpolation=cv2.INTER_AREA)
    al = rs[:, :, 3:4] / 255
    out = np.dstack([rs[:, :, :3] / np.maximum(al, 1e-4), rs[:, :, 3:4]])
    return np.clip(out, 0, 255).astype(np.uint8)


def build_rig(k):
    rgb, fg = load(k)
    names = parts_of(k)
    lab = labels(k, rgb, fg)
    J, tips, tf, Ro = joints_drawn(k, fg) if k in JD else joints_from_old(k)
    ks, feet_x, ground = tf["ks"], tf["feet_x"], tf["ground"]

    def S(p):
        return ((p[0] - feet_x) * ks, (ground - p[1]) * ks)

    R = L.Rig(code(k))
    R.bone("root", None, 0, 0)
    for b in ["move", "shadow", "hip", "spine1", "spine2", "chest", "neck", "head", "crest1", "crest2", "crest3",
              "arm_b1", "arm_b2", "fist_b", "arm_f1", "arm_f2", "hand_f", "weapon", "leg_b1", "leg_b2", "foot_b",
              "leg_f1", "leg_f2", "foot_f", "tail1", "tail2", "tail3", "tail4", "cloth1", "cloth2", "cloth3",
              "cape1", "cape2", "cape3", "cape4"]:
        if b in ("move", "shadow"):
            R.bone(b, "root", 0, 0)
        elif b in J:
            R.bone(b, PARENT[b], *S(J[b]))
    tip, grip = S(J["tip"]), R.bw("weapon")
    R.point("tip", "weapon", *tip)
    for sd in ("b", "f"):
        R.legs[sd] = (f"leg_{sd}1", f"leg_{sd}2", f"foot_{sd}")
    R.ik_space = "root"
    info = {"tip": tip, "grip": grip}
    for n, p in tips.items():
        info[n + "_tip"] = S(p)
    axis = JD.get(k, {}).get("axis")  # súng, pháo: góc vũ khí theo trục nòng (tay cầm lệch dưới trục)
    add_fx(R, tip, grip, (S(axis[0]), S(axis[1])) if axis else None)

    # điểm đầu, các khớp giữa, điểm cuối của từng chuỗi (toạ độ concept)
    def chain_pts(part):
        bones = CHAINS[part][0]
        pts = [J[b] for b in bones]
        if part == "torso":
            end = J["neck"]
        elif part == "head":
            end = far_point(lab == names.index("head"), J["neck"])
        elif part in ("arm_b", "arm_f"):
            end = J["fist_b" if part == "arm_b" else "hand_f"]
        elif part in ("leg_b", "leg_f"):
            end = J["foot_" + part[-1]]
        else:
            end = tips[part]
        return pts, end

    # lớp: miền = phần của lớp + dải mọc thêm dưới các lớp trên; kết cấu vẽ bù dải đó
    above = set()
    layer_specs = []
    for name, ps, grow in reversed(LAYERS[k]):
        layer_specs.append((name, ps, grow, set(above)))
        above |= set(ps)
    layer_specs.reverse()
    sc = ks  # ảnh lớp lưu ở tỉ lệ rig
    stats = []
    R.slot("shadow", "shadow", "shadow")
    R.region("shadow", "shadow", "shadow", "shadow", 0, 0)
    fx_slot(R, "fx_ground")
    fx_slot(R, "fx_ring_b")
    lay_dbg = []
    for name, ps, grow, abv in layer_specs:
        ids = [names.index(p) for p in ps]
        own = np.isin(lab, ids) & (fg > 0)
        ring = np.zeros_like(own)
        if grow and abv:
            into = np.isin(lab, [names.index(p) for p in abv]) & (fg > 0)
            ring = (cv2.dilate(own.astype(np.uint8), riglib_disk(grow)) > 0) & into & ~own
        cape_tile = None
        if FULL_SHEET & set(ps):  # áo choàng: cả tấm sau người (bao lồi các mảnh lộ ra, trong hình), phần khuất phủ vân áo choàng
            hull = cv2.convexHull(np.stack(np.nonzero(own)[::-1], 1).astype(np.int32))
            full = np.zeros(own.shape, np.uint8)
            cv2.fillConvexPoly(full, hull, 1)
            ring = (full > 0) & (fg > 0) & ~own
            cape_tile = texture_tile(rgb, own)
        dom = own | ring
        # dải mọc thêm: mép mượt (không răng cưa) rồi kẻ nét mực dọc mép trong hình; lúc nghỉ dải này nằm dưới lớp trên,
        # khi lớp trên cử động thì lộ ra như phần bị che có viền vẽ tay, không thành mảng nhoè lởm chởm
        if ring.any():
            sm = cv2.morphologyEx(dom.astype(np.uint8), cv2.MORPH_CLOSE, riglib_disk(6))
            sm = cv2.morphologyEx(sm, cv2.MORPH_OPEN, riglib_disk(8))
            dom = ((sm > 0) & (fg > 0)) | own
        dom = cv2.morphologyEx(dom.astype(np.uint8), cv2.MORPH_CLOSE, riglib_disk(2)) > 0
        dom &= fg > 0
        dom = riglib.biggest(dom, 150)
        tex = rgb.copy()
        if (dom & ~own).any():
            work = rgb.copy()
            work[~own] = np.median(rgb[own], 0).astype(np.uint8)
            fill = (dom & ~own).astype(np.uint8) * 255
            if cape_tile is not None:  # mảng lớn: lát vân sáp thật của áo choàng (vẽ bù TELEA nhoè màu viền đồng vào)
                th, tw = cape_tile.shape[:2]
                reps = (fg.shape[0] // th + 1, fg.shape[1] // tw + 1, 1)
                tiled = np.tile(cape_tile, reps)[:fg.shape[0], :fg.shape[1]]
                near = cv2.inpaint(work, fill, 9, cv2.INPAINT_TELEA)  # sát mép phần lộ ra: hoà dần từ màu thật
                dd = cv2.distanceTransform((~own).astype(np.uint8), cv2.DIST_L2, 5)
                wgt = np.clip(dd / 14.0, 0, 1)[..., None]
                tex = (near * (1 - wgt) + tiled * wgt).astype(np.uint8)
            else:
                tex = cv2.inpaint(work, fill, 9, cv2.INPAINT_TELEA)
                tex = np.where((dom & ~own)[..., None], cv2.GaussianBlur(tex, (0, 0), 2.0), tex)
            edge = dom & (cv2.erode(dom.astype(np.uint8), riglib_disk(3)) == 0)
            inside = cv2.erode(fg, riglib_disk(5)) > 0  # bỏ mép thật của hình (đã có nét mực)
            line_ = edge & inside & ~own
            soft = cv2.GaussianBlur(line_.astype(np.float32), (0, 0), 0.8)[..., None]
            soft = np.maximum(soft, line_[..., None].astype(np.float32))
            tex = (tex * (1 - soft) + np.array(INK, np.float32) * soft).astype(np.uint8)
            tex[own] = rgb[own]
        a = cv2.GaussianBlur(dom.astype(np.float32), (0, 0), 0.9)
        ys, xs = np.nonzero(a > 0.02)
        x0, y0, x1, y1 = max(0, xs.min() - 3), max(0, ys.min() - 3), min(fg.shape[1], xs.max() + 4), min(fg.shape[0], ys.max() + 4)
        rgba = np.dstack([tex, np.clip(a * 255, 0, 255).astype(np.uint8)])[y0:y1, x0:x1]
        w2, h2 = max(1, round((x1 - x0) * sc)), max(1, round((y1 - y0) * sc))
        small = premul_resize(rgba, w2, h2)
        fx_, fy_ = (x1 - x0) / w2, (y1 - y0) / h2  # pixel ảnh nhỏ -> pixel concept
        ox, oy = S((x0, y0))
        pc = L.Piece(name, small, ox, oy)
        # nhãn trong miền lớp: pixel dải mọc thêm lấy nhãn phần gần nhất của chính lớp
        llab = np.where(own, lab, -1)
        for _ in range(grow + 4):
            miss = dom & (llab < 0)
            if not miss.any():
                break
            g = cv2.dilate(llab.astype(np.float32) + 1, np.ones((3, 3), np.uint8)).astype(np.int32) - 1
            llab[miss] = g[miss]
        # bản đồ s cho phần chuỗi trong lớp
        smap = {}
        for p in ps:
            if p not in CHAINS:
                continue
            pm = llab == names.index(p)
            if not pm.any():
                continue
            pts, end = chain_pts(p)
            if p in LINEAR_Y:
                yy = np.arange(pm.shape[0], dtype=np.float32)[:, None] * np.ones((1, pm.shape[1]), np.float32)
                D = np.where(pm, np.maximum(0, yy - pts[0][1]), np.inf).astype(np.float32)
            else:
                D = geo(pm, pts[0])
            Lc = max(1.0, at(D, end))
            cuts = [at(D, q) / Lc for q in pts[1:]]
            cuts = [min(0.95, max(0.05, c)) for c in cuts]
            for i in range(1, len(cuts)):
                cuts[i] = max(cuts[i], cuts[i - 1] + 0.05)
            smap[p] = (D / Lc, cuts)
        pts_, nh, tris = pc.make_mesh(8, 14)
        wts, plabs = [], []
        for u, v in pts_:
            X, Y = x0 + u * fx_, y0 + v * fy_
            xi, yi = int(min(fg.shape[1] - 1, max(0, round(X)))), int(min(fg.shape[0] - 1, max(0, round(Y))))
            li = llab[yi, xi]
            if li < 0:
                yy, xx = np.nonzero(llab >= 0)
                j = int(np.argmin((xx - X) ** 2 + (yy - Y) ** 2))
                xi, yi, li = int(xx[j]), int(yy[j]), int(llab[yy[j], xx[j]])
            p = names[li]
            plabs.append(ps.index(p) if p in ps else 0)
            if p in CHAINS and p in smap:
                Dn, cuts = smap[p]
                s = float(Dn[yi, xi]) if np.isfinite(Dn[yi, xi]) else at(Dn, (xi, yi))
                bones, par, bl, pb = CHAINS[p]
                wts.append(chain_w(min(1.0, max(0.0, s)), bones, cuts, par, bl, pb))
            else:
                rb = RIGID.get(p, "chest")
                wts.append(list(rb) if isinstance(rb, list) else [(rb, 1.0)])
        plabs = np.array(plabs)
        # tam giác vẽ theo thứ tự phần trong lớp (sau -> trước)
        depth = np.array([plabs[t].max() for t in tris]) if len(tris) else np.zeros(0)
        tris = tris[np.argsort(depth, kind="stable")]
        vw = np.array([pc.to_rig(x, y) for x, y in pts_])
        uv = np.stack([pts_[:, 0] / w2, pts_[:, 1] / h2], 1)
        R.images[name] = Image.fromarray(small)
        first = CHAINS[ps[0]][0][0] if ps[0] in CHAINS else (RIGID[ps[0]] if isinstance(RIGID[ps[0]], str)
                                                             else RIGID[ps[0]][0][0])
        R.slot(name, first, name)
        R.mesh(name, name, name, vw, uv, tris, nh, wts)
        stats.append(f"{name}: {len(pts_)} đỉnh, mọc {int(ring.sum())} px")
        lay_dbg.append((name, rgba, own[y0:y1, x0:x1], (x0, y0)))
        if name == "body":  # sau thân: hiệu ứng vòng nước trước (giữa thân và tay trước? giữ như cũ: sau mọi mảnh)
            pass
    fx_slot(R, "fx_ring_f")
    for n in ("fx_jet", "fx_slash", "fx_splash", "fx_wave", "fx_geyser", "fx_drops", "fx_tip", "fx_spark"):
        fx_slot(R, n)
    R.chain_tips = {n: info[n + "_tip"] for n in ("tail", "crest", "cloth", "cape") if n + "_tip" in info}

    ctx = T.Ctx()
    ctx.k, ctx.R, ctx.info = k, R, info
    ctx.ank = {sd: R.bw(f"foot_{sd}") for sd in ("b", "f")}
    ctx.rgb, ctx.fg, ctx.lab, ctx.tf, ctx.J = rgb, fg, lab, tf, J
    ctx.layers = lay_dbg
    print(f"dạng {k}: " + "; ".join(stats))
    return R, ctx


def texture_tile(rgb, own, size=72):
    """ô vân lát được: ô vuông nằm trọn trong phần màu trơn (không nét mực, không hoa văn sáng) của vùng own, phản chiếu
    bốn phía cho liền mép."""
    flat = own & (rgb.mean(2) > 72) & (rgb.mean(2) < 170)
    inner = cv2.erode(flat.astype(np.uint8), np.ones((size, size), np.uint8)) > 0
    ys, xs = np.nonzero(inner)
    if not len(ys):
        med = np.median(rgb[own], 0).astype(np.uint8)
        return np.tile(med, (size * 2, size * 2, 1))
    j = len(ys) // 2
    y0, x0 = ys[j] - size // 2, xs[j] - size // 2
    t = rgb[y0:y0 + size, x0:x0 + size]
    t = np.concatenate([t, t[:, ::-1]], 1)
    return np.concatenate([t, t[::-1]], 0)


def riglib_disk(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def far_point(mask, start):
    D = geo(mask, start)
    fin = np.where(np.isfinite(D), D, -1)
    y, x = np.unravel_index(int(np.argmax(fin)), D.shape)
    return float(x), float(y)


# ---------------------------------------------------------------- hiệu ứng (như thuy_long.build_rig)
FXSPEC = {}


def add_fx(R, tip, grip, axis=None):
    cx0, cy0 = R.bw("spine2")
    fxb = {"fx_ring": ("move", cx0, cy0), "fx_ground": ("move", 0.0, 0.02 * H), "fx_slash": ("move", 0.5 * H, 0.5 * H),
           "fx_splash": ("move", 0.72 * H, 0.45 * H), "fx_wave": ("move", 0.9 * H, 0.0), "fx_spark": ("weapon", tip[0], tip[1]),
           "fx_drops": ("chest", R.bw("chest")[0] + 0.12 * H, R.bw("chest")[1]), "fx_tip": ("weapon", tip[0], tip[1]),
           "fx_jet": ("weapon", tip[0], tip[1]), "fx_geyser": ("move", 0.5 * H, 0.0)}
    for b, (par, x, y) in fxb.items():
        R.bone(b, par, x, y)
    for n in T.FX:
        R.images[n] = T.fx_image(n)
    R.images["shadow"] = T.shadow_image(abs(R.bw("foot_f")[0] - R.bw("foot_b")[0]) + 0.2 * H)
    a0, a1 = axis if axis else (grip, tip)
    wa = math.degrees(math.atan2(a1[1] - a0[1], a1[0] - a0[0]))
    R.weapon_ang = wa
    FXSPEC.clear()
    FXSPEC.update({"fx_ground": ("fx_ground", "FX08", 0.95 * H, 0, 0, 0), "fx_ring_b": ("fx_ring", "FX01", 1.0 * H, 0, 0, 0),
                   "fx_ring_f": ("fx_ring", "FX01", 1.0 * H, 0, 0, 0),
                   "fx_jet": ("fx_jet", "FX09", 0.9 * H, wa, 0.42 * H * math.cos(math.radians(wa)),
                              0.42 * H * math.sin(math.radians(wa))),
                   "fx_slash": ("fx_slash", "FX02", 0.62 * H, 0, 0, 0), "fx_splash": ("fx_splash", "FX03", 0.5 * H, 0, 0, 0),
                   "fx_wave": ("fx_wave", "FX07", 0.85 * H, 0, 0, 0), "fx_geyser": ("fx_geyser", "FX09", 1.0 * H, 90, 0, 0.5 * H),
                   "fx_drops": ("fx_drops", "FX04", 0.3 * H, 0, 0, 0), "fx_tip": ("fx_tip", "FX06", 0.2 * H, 0, 0, 0),
                   "fx_spark": ("fx_spark", "FX05", 0.22 * H, 0, 0, 0)})


def fx_slot(R, slot):
    bone, img, size, rot, ox, oy = FXSPEC[slot]
    im = R.images[img]
    s = size / max(im.size)
    bx, by = R.bw(bone)
    R.slot(slot, bone, None, fx=True)
    R.region(slot, slot, img, bone, bx + ox, by + oy, im.width * s, im.height * s, rot)


# ---------------------------------------------------------------- soi
def debug_layers(ctx, path):
    """từng lớp trên nền xám (dải vẽ bù hiện rõ), tỉ lệ 1/2 concept."""
    cells = []
    F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 26)
    Hh, Ww = ctx.fg.shape
    for name, rgba, own, (x0, y0) in ctx.layers:
        im = Image.new("RGB", (Ww, Hh), (190, 196, 206))
        t = Image.fromarray(rgba)
        im.paste(t, (x0, y0), t)
        d = ImageDraw.Draw(im)
        d.text((10, 10), name, fill=(0, 0, 0), font=F)
        cells.append(np.array(im.resize((Ww // 3, Hh // 3), Image.LANCZOS)))
    Image.fromarray(np.concatenate(cells, 1)).save(path)


def portrait(ctx, out, res):
    """chân dung khung 4:5 (chân cách đáy 6%) cắt thẳng từ concept, lưu vuông 512, không bóng."""
    rgb, fg, tf = ctx.rgb, ctx.fg, ctx.tf
    hh = tf["ground"] - tf["top"]
    fh = hh / 0.86
    fw = fh * 0.8
    x0, y0 = tf["feet_x"] - fw / 2, tf["ground"] - 0.94 * fh
    a = cv2.GaussianBlur(fg.astype(np.float32), (0, 0), 0.8) * 255
    rgba = np.dstack([rgb, a.astype(np.uint8)])
    Wc, Hc = int(round(fw)), int(round(fh))
    canvas = np.zeros((Hc, Wc, 4), np.uint8)
    ax0, ay0 = int(round(x0)), int(round(y0))
    sx0, sy0, sx1, sy1 = max(0, ax0), max(0, ay0), min(rgb.shape[1], ax0 + Wc), min(rgb.shape[0], ay0 + Hc)
    canvas[sy0 - ay0:sy1 - ay0, sx0 - ax0:sx1 - ax0] = rgba[sy0:sy1, sx0:sx1]
    im = Image.fromarray(canvas)
    im.save(os.path.join(out, "chan_dung_4x5.png"))
    im.resize((512, 512), Image.LANCZOS).save(os.path.join(res, code(ctx.k) + "_portrait.png"))


def clean(baked, R):
    """bỏ khoá của xương, slot rig không có (clip dùng chung giữa các tướng: tướng thiếu mào, vải, áo choàng...)."""
    slots = {x["name"] for x in R.slots}
    for frames in baked.values():
        for P in frames:
            for b in [b for b in P.t if b not in R.bi]:
                del P.t[b]
            for d in (P.att, P.alpha):
                for x in [x for x in d if x not in slots]:
                    del d[x]
            for x in [x for x, a in P.att.items() if a is not None and a not in R.atts.get(x, {})]:
                del P.att[x]  # hình không có trong slot (mặt nhắm mắt, mặt gầm của bản ghép mảnh)
    return baked


def springs(R, prefix=""):
    """như thuy_long.springs; mào trong ảnh liền là cả bờm dọc gáy (dài hơn mảnh mào cũ) nên cứng hơn, khỏi văng ngang."""
    cfg = T.springs(R, prefix)
    c = cfg.get(prefix + "crest")
    if c:
        c["k"] = [460, 360, 280]
        c["damp"] = 0.62
        c["maxang"] = 9.0
    c = cfg.get(prefix + "cape")
    if c:
        c["k"] = [300, 240, 190, 150]
        c["damp"] = 0.6
        c["maxang"] = 12.0
    return cfg


# ---------------------------------------------------------------- dựng, nướng, xuất (như thuy_long.build_form)
def build_form(k, nxt=None, gif=True):
    R, ctx = build_rig(k)
    od = out_dir(k)
    os.makedirs(od, exist_ok=True)
    debug_layers(ctx, os.path.join(od, "lop.png"))
    names = parts_of(k)
    label_sheet(k, ctx.rgb, ctx.lab, os.path.join(od, "nhan.png"), extra=list(ctx.J.values()))
    clips = CFG["clips"](ctx)
    cfg = springs(R)
    baked = clean({n: L.bake(R, c, cfg) for n, c in clips.items()}, R)
    hgt = L.idle_height(R, baked["idle"][0])
    res_dir = os.path.join(T.RES, code(k))
    Rx = R
    if nxt:
        ctxB, RB, idleB0, hB = nxt
        M = L.merge_next(R, RB)
        M.chain_tips = dict(R.chain_tips)
        M.chain_tips.update({"n_" + n: p for n, p in RB.chain_tips.items()})
        M.legs = dict(R.legs)
        M.legs.update({"n_" + sd: tuple("n_" + b for b in leg[:3]) + ("evo",) for sd, leg in RB.legs.items()})
        M.points = dict(R.points)
        M.weapon_ang = R.weapon_ang
        cfgM = dict(cfg)
        cfgM.update(springs(M, prefix="n_"))
        ev = CFG["evolve"](ctx, ctxB, M, idleB0, hgt / hB)
        hide = {"n_" + s["name"] for s in RB.slots}
        clipsM = {}
        for n, c in clips.items():
            def fn(t, P, f0=c["fn"]):
                f0(t, P)
                for s_ in hide:
                    P.att[s_] = None
            clipsM[n] = dict(c, fn=fn)
        clipsM["evolve"] = ev
        bakedM = clean({n: L.bake(M, c, cfgM) for n, c in clipsM.items()}, M)
        Rx, clips, baked = M, clipsM, bakedM
    game = T.game_info(Rx, clips, baked)
    game["height"] = round(hgt, 2)
    game["beam"] = CFG["beam"][k]
    game.update(CFG.get("game", {}))  # tướng đứng bắn: không lao ở chiêu cuối...
    print(f"dạng {k}: {len(Rx.bones)} xương, {len(Rx.slots)} slot, cao {hgt:.0f}, trận {json.dumps(game, ensure_ascii=False)}")
    aw, ah = L.export(Rx, clips, baked, od, res_dir, game, H, gif=gif)
    print(f"  atlas {aw}x{ah}, ra {od}")
    portrait(ctx, od, res_dir)
    with open(os.path.join(od, "baked.pkl"), "wb") as fh:
        pickle.dump((Rx, {n: c["dur"] for n, c in clips.items()}, baked), fh)
    _ = names
    return ctx, R, baked["idle"][0], hgt


def show(k, clip, times, fh=520, follow=False):
    with open(os.path.join(out_dir(k), "baked.pkl"), "rb") as f_:
        R, durs, baked = pickle.load(f_)
    frames = baked[clip]
    kk = fh / (1.75 * H)
    Wb = int(1.9 * H * kk)
    imgs = []
    for t in times:
        i = min(len(frames) - 1, round(t * L.FPS))
        P = frames[i]
        mx = P.t.get("move", [0, 0, 0, 1, 1])[0] if follow else 0
        box = (Wb, fh, int((0.6 * H - mx) * kk), int(fh - 0.1 * H * kk))
        im = Image.fromarray(L.render(R, P, kk, box))
        ImageDraw.Draw(im).text((6, 6), f"{clip} {t:.2f}s", fill=(43, 33, 24))
        imgs.append(np.array(im))
    p = os.path.join(out_dir(k), f"xem_{clip}.png")
    Image.fromarray(np.concatenate(imgs, 1)).save(p)
    print(p)


def main(argv):
    step = argv[0]
    if step == "nhan":  # chỉ soi vùng watershed
        k = int(argv[1])
        rgb, fg = load(k)
        lab = labels(k, rgb, fg)
        os.makedirs(out_dir(k), exist_ok=True)
        label_sheet(k, rgb, lab, os.path.join(out_dir(k), "nhan.png"))
        print(os.path.join(out_dir(k), "nhan.png"))
    elif step == "rig":
        build_form(int(argv[1]), gif="--gif" in argv)
    elif step == "show":
        show(int(argv[1]), argv[2], [float(x) for x in argv[3].split(",")], follow="follow" in argv)
    elif step == "all":
        n3 = build_form(3)
        n2 = build_form(2, n3)
        build_form(1, n2)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
