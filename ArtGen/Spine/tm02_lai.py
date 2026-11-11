# -*- coding: utf-8 -*-
"""tm02 (Thạch Giải) cách lai (đặc tả mục 5): mọi lớp CẮT THẲNG TỪ CONCEPT đã duyệt (nhà đá, vành cửa, san hô, rong, thân, cằm,
mắt + cuống, râu, càng + ngón động, chân). Tờ GPT chỉ cho mắt nhắm (mí) và lòng miệng (tm02.py nạp).

    D:/spine-venv/Scripts/python -I ArtGen/Spine/tm02_lai.py <k>

Gán nhãn: nét mực (nâu đen: tối và B - R nhỏ; màu xanh than của ngón càng, đá bazan KHÔNG phải mực) là tường; mỗi cụm màu nhận
nhãn của đa giác / dải (đường giữa + bán kính) chiếm đa số; cụm vắt qua hai bộ phận thì chia theo từng điểm ảnh. Nét mực: lớp
TRƯỚC giành viền của nó (loang 10 px theo thứ tự trước → sau), phần còn lại theo nhãn gần nhất.
Lớp dưới mọc thêm dưới các lớp trên (GROW, ≥ 30 px), vẽ bù bằng inpaint màu chính lớp (nét mực của lớp không làm nguồn), kẻ nét
mực dọc mép phần mọc thêm; nhà đá dưới thân lấp màu lòng cửa tối.
Ra inbox/tm02_<k>/manh_lai/<lớp>.png (RGBA, cắt sát) + lai.json (gốc cắt trong concept, đường giữa các dải) + nhan.png (soi).
"""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8")
CODE = "tm02"
INK = (43, 33, 24)

# ---------------------------------------------------------------- cấu hình dạng 2 (concept 1536 × 1024)
# mỗi lớp: "pg" đa giác, hoặc "cl" đường giữa (gốc → ngọn) + "r" bán kính; thứ tự = vẽ sau → trước
P2 = {
    "chan0": {"cl": [(345, 715), (285, 735), (240, 770), (215, 820), (195, 890)], "r": 38},
    "chan1": {"cl": [(480, 740), (430, 770), (405, 820), (385, 880), (365, 940)], "r": 40},
    "chan2": {"cl": [(690, 735), (645, 770), (620, 840), (600, 920), (585, 1000)], "r": 44},
    "thap": {"pg": [(285, 640), (315, 450), (345, 290), (378, 168), (420, 140), (470, 190), (545, 235), (565, 300), (630, 330), (700, 365),
                    (790, 415), (812, 470), (780, 520), (700, 700), (650, 790), (560, 805), (420, 775), (315, 735), (285, 690)]},
    "sh0": {"pg": [(262, 145), (295, 72), (345, 82), (378, 168), (350, 205), (300, 175)]},
    "sh1": {"pg": [(352, 95), (372, 40), (440, 22), (490, 70), (495, 112), (440, 160), (392, 182), (366, 130)]},
    "sh2": {"pg": [(448, 165), (478, 118), (525, 128), (565, 180), (548, 232), (482, 236), (452, 205)]},
    "sh3": {"pg": [(525, 262), (556, 238), (606, 246), (642, 290), (612, 338), (568, 338), (538, 302)]},
    "sh4": {"pg": [(612, 322), (648, 303), (692, 318), (708, 352), (684, 394), (640, 394), (618, 362)]},
    "rong0": {"cl": [(345, 188), (300, 232), (262, 300), (240, 380), (226, 435), (236, 485), (245, 525)], "r": 20},
    "rong1": {"cl": [(352, 200), (332, 262), (304, 320), (292, 380), (298, 420), (300, 458)], "r": 18},
    "rau0": {"cl": [(940, 522), (936, 450), (905, 330), (830, 225), (720, 155), (630, 128), (553, 124)], "r": 13},
    "rau1": {"cl": [(926, 522), (917, 450), (875, 352), (790, 268), (700, 228), (620, 214), (533, 214)], "r": 13},
    "cang2_tay": {"cl": [(860, 775), (930, 755), (1000, 725), (1060, 705), (1120, 680), (1160, 665)], "r": 34},
    "cang2_ngon": {"pg": [(1165, 700), (1215, 680), (1300, 668), (1385, 660), (1395, 680), (1330, 715), (1250, 745), (1195, 752), (1165, 740)],
                   "truc": [(1186, 718), (1250, 702)], "r": 26},
    "cang2": {"pg": [(1105, 655), (1140, 610), (1210, 588), (1290, 578), (1360, 590), (1408, 628), (1395, 645), (1320, 625), (1250, 640),
                     (1205, 690), (1192, 748), (1140, 750), (1110, 715)]},
    "chan3": {"cl": [(905, 760), (950, 790), (990, 840), (1030, 900), (1055, 955)], "r": 42},
    "mat0": {"pg": [(826, 432), (858, 414), (918, 420), (922, 470), (902, 500), (898, 534), (866, 534), (864, 502), (834, 482)]},
    "mat1": {"pg": [(952, 414), (1000, 402), (1054, 414), (1054, 470), (1024, 502), (972, 534), (946, 530), (952, 494)]},
    "cang1_tay": {"pg": [(1040, 575), (1072, 522), (1090, 470), (1118, 444), (1186, 448), (1172, 500), (1122, 560), (1092, 610),
                         (1062, 642), (1046, 628)], "truc": [(1040, 640), (1075, 580), (1110, 515), (1150, 465)], "r": 34},
    "cang1_ngon": {"pg": [(1212, 152), (1265, 132), (1340, 146), (1392, 196), (1390, 248), (1345, 222), (1285, 210), (1250, 255), (1214, 248)],
                   "truc": [(1236, 198), (1300, 172)], "r": 40},
    "cang1": {"pg": [(1028, 292), (1058, 200), (1108, 158), (1170, 148), (1235, 142), (1258, 205), (1254, 282), (1305, 296), (1398, 288),
                     (1394, 332), (1342, 404), (1272, 432), (1200, 452), (1150, 462), (1090, 432), (1048, 384)]},
    "than": {"pg": [(632, 560), (660, 518), (720, 498), (800, 500), (900, 505), (1000, 518), (1052, 560), (1046, 628), (1022, 650), (1000, 670),
                    (960, 740), (900, 782), (820, 802), (740, 792), (680, 762), (648, 702), (626, 622)]},
    "ham": {"pg": [(928, 642), (950, 632), (985, 642), (1016, 632), (1022, 646), (1006, 662), (970, 670), (938, 664)]},
    "vanh": {"pg": [(556, 482), (640, 444), (722, 432), (800, 452), (806, 482), (722, 468), (652, 488), (616, 540), (600, 620), (604, 700),
                    (628, 768), (600, 802), (568, 762), (553, 682), (552, 580)]},
}
# lớp dưới mọc thêm (px concept) dưới các lớp trên: (px, [lớp trên], tuỳ chọn)
#   tuỳ chọn: "truc" = dải mọc theo trục lùi về gốc (ống liền, không phải cục tròn); "khep" = bán kính khép mép (đường viền
#   trơn đoán được thay vì theo hình lớp trên); "vien": False = không kẻ nét mực mép; "cat" = đa giác giới hạn; "toi" = lấp màu lòng cửa
G2 = {
    "cang2_tay": (36, ["chan3", "than", "ham", "cang2"], {"truc": True}),
    "cang2_ngon": (34, ["cang2"], {"truc": True}),
    "chan0": (40, ["thap", "vanh"], {"truc": True}), "chan1": (40, ["thap", "vanh"], {"truc": True}),
    "chan2": (44, ["thap", "vanh", "than"], {"truc": True}), "chan3": (40, ["than", "ham"], {"truc": True}),
    "thap": (30, ["sh0", "sh1", "sh2", "sh3", "sh4", "rong0", "rong1"], {"khep": 31}),
    "thap#toi": (90, ["than", "mat0", "mat1", "rau0", "rau1", "cang2_tay", "chan3", "cang1_tay"], {"toi": True, "cat": "elip",
                                                                                                "elip": ((712, 630), (128, 168))}),
    "than": (0, ["ham", "vanh"], {}),
    "rong0": (24, ["rong1"], {"khep": 15}),
    "rau0": (30, ["than", "mat0", "mat1"], {"truc": True}), "rau1": (30, ["than", "mat0", "mat1"], {"truc": True}),
    "mat0": (22, ["than"], {"khep": 11}), "mat1": (22, ["than"], {"khep": 11}),
    "cang1_tay": (40, ["than", "ham", "cang1"], {"truc": True}),
    "cang1_ngon": (44, ["cang1"], {"truc": True}),
}
TOI2 = (600, 600, 640, 690)   # ô lấy màu lòng cửa tối

# thứ tự vẽ nhãn (sau đè trước): khối lớn trước để chân, càng, mắt giành phần chồng; "ep" = ép theo đa giác từng điểm ảnh
PRI2 = ["thap", "than"] + [n for n in P2 if n not in ("thap", "than", "vanh", "ham")] + ["vanh", "ham"]
# lọc màu: cụm gán vào lớp này mà màu không đúng thì trả về lớp dự phòng (đa giác san hô, rong ôm cả mẩu đá)
LOC2 = {**{f"sh{i}": ("do", "thap") for i in range(5)}, "rong0": ("xanh", "thap"), "rong1": ("xanh", "thap")}
# mắt nhắm làm từ chính mắt concept: (tâm tròng, bán kính, ô lấy màu nắp mí)
MAT2 = {"mat0": ((872, 470), 38, (850, 424, 900, 438)), "mat1": ((1003, 462), 42, (985, 414, 1040, 428))}
CFG = {2: dict(P=P2, G=G2, toi=TOI2, pri=PRI2, ep=["ham"], loc=LOC2, mat=MAT2)}

# ---------------------------------------------------------------- cấu hình dạng 1 (concept 1536 × 1024)
# hai càng là một lớp liền mỗi càng (ngón động bẻ bằng trọng số lưới, không cắt); thứ tự: chân, tảng đá, rong, râu, [mặt nạ],
# càng nhỏ, mắt, thân, cằm, càng búa (đè trước mặt), vành cửa
P1 = {
    "chan0": {"cl": [(402, 704), (390, 760), (375, 820), (358, 884)], "r": 36},
    "chan1": {"cl": [(522, 704), (518, 770), (512, 840), (506, 912)], "r": 38},
    "chan2": {"cl": [(664, 712), (660, 780), (652, 850), (646, 912)], "r": 38},
    "chan3": {"cl": [(776, 712), (790, 778), (802, 840), (812, 905)], "r": 38},
    "thap": {"pg": [(318, 520), (330, 440), (360, 340), (420, 290), (480, 250), (560, 228), (640, 236), (700, 258), (748, 300), (765, 360),
                    (712, 392), (650, 410), (606, 480), (592, 580), (604, 690), (570, 722), (440, 724), (360, 694), (322, 612)]},
    "rong0": {"cl": [(506, 302), (482, 252), (452, 186), (402, 146), (352, 145), (322, 163)], "r": 19},
    "rong1": {"cl": [(504, 304), (456, 270), (396, 242), (332, 230), (286, 248)], "r": 19},
    "rong2": {"cl": [(502, 308), (450, 300), (390, 302), (346, 320), (318, 343)], "r": 19},
    "rau0": {"cl": [(882, 458), (876, 380), (852, 292), (782, 210), (682, 160), (592, 150), (512, 188)], "r": 12},
    "rau1": {"cl": [(892, 458), (898, 380), (930, 292), (990, 222), (1060, 186), (1110, 182)], "r": 12},
    "cang2_tay": {"pg": [(984, 540), (1030, 514), (1066, 470), (1112, 478), (1084, 530), (1042, 572), (996, 584)],
                  "truc": [(990, 572), (1040, 536), (1095, 490)], "r": 24},
    "cang2": {"pg": [(1052, 470), (1058, 420), (1080, 384), (1120, 362), (1152, 368), (1162, 392), (1196, 382), (1198, 432), (1182, 482),
                     (1140, 498), (1098, 498)]},
    "mat0": {"pg": [(754, 342), (800, 322), (872, 328), (888, 382), (872, 432), (816, 446), (802, 504), (774, 504), (770, 446), (756, 400)]},
    "mat1": {"pg": [(903, 342), (950, 320), (1012, 328), (1028, 386), (1012, 432), (956, 446), (952, 518), (924, 518), (922, 442), (903, 396)]},
    "than": {"pg": [(662, 560), (668, 470), (706, 438), (800, 444), (900, 450), (992, 468), (1004, 540), (986, 620), (942, 650), (880, 660),
                    (800, 660), (720, 650), (680, 622)]},
    "ham": {"pg": [(844, 627), (880, 636), (914, 624), (926, 640), (906, 651), (862, 653), (844, 642)]},
    "cang1_tay": {"pg": [(680, 600), (730, 596), (800, 610), (832, 648), (975, 646), (986, 726), (840, 726), (800, 724), (744, 724), (698, 690),
                         (678, 650)], "truc": [(690, 640), (760, 662), (860, 684), (975, 690)], "r": 38},
    "cang1": {"pg": [(964, 690), (990, 620), (1050, 574), (1130, 558), (1210, 568), (1272, 598), (1302, 640), (1272, 662), (1200, 652),
                     (1180, 690), (1210, 712), (1266, 704), (1278, 740), (1232, 792), (1150, 824), (1060, 822), (990, 782)]},
    "vanh": {"pg": [(636, 394), (700, 378), (762, 382), (764, 410), (702, 404), (664, 430), (634, 500), (626, 600), (640, 690), (662, 702),
                    (620, 706), (594, 682), (586, 600), (594, 500), (612, 430)]},
}
G1 = {
    "chan0": (40, ["thap", "vanh"], {"truc": True}), "chan1": (40, ["thap", "vanh"], {"truc": True}),
    "chan2": (40, ["thap", "vanh", "than"], {"truc": True}), "chan3": (40, ["than", "thap", "vanh", "cang1_tay"], {"truc": True}),
    "thap": (30, ["rong0", "rong1", "rong2"], {"khep": 31}),
    "thap#toi": (130, ["vanh", "than", "mat0", "mat1", "rau0", "rau1", "cang1_tay"], {"toi": True, "cat": "elip",
                                                                                   "elip": ((700, 560), (112, 166))}),
    "rong0": (24, ["rong1", "rong2"], {"khep": 15}), "rong1": (24, ["rong2"], {"khep": 15}),
    "rau0": (30, ["than", "mat0", "mat1"], {"truc": True}), "rau1": (30, ["than", "mat0", "mat1"], {"truc": True}),
    "cang2_tay": (34, ["than", "cang2"], {"truc": True}),
    "mat0": (22, ["than"], {"khep": 11}), "mat1": (22, ["than"], {"khep": 11}),
    "than": (0, ["ham", "vanh", "cang1_tay"], {}),
    "cang1_tay": (36, ["cang1", "vanh"], {"truc": True}),
}
PRI1 = ["thap", "than"] + [n for n in P1 if n not in ("thap", "than", "vanh", "ham")] + ["vanh", "ham"]
LOC1 = {"rong0": ("xanh", "thap"), "rong1": ("xanh", "thap"), "rong2": ("xanh", "thap")}
MAT1 = {"mat0": ((818, 398), 45, (790, 330, 850, 346)), "mat1": ((964, 398), 45, (935, 328, 995, 344))}
CFG[1] = dict(P=P1, G=G1, toi=(46, 50, 64), pri=PRI1, ep=["ham"], loc=LOC1, mat=MAT1)


def path(k, *a):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}", *a)


def fg_mask(rgb):
    """nền trắng loang từ mép; khe trắng kín > 1500 px cũng là nền."""
    light = (rgb.min(2) > 236).astype(np.uint8)
    H, W = light.shape
    n, cc, st, _ = cv2.connectedComponentsWithStats(light, connectivity=4)
    bg = np.zeros((H, W), bool)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w >= W or y + h >= H or a > 200:
            bg |= cc == i
    return ~bg


def ink_mask(rgb, fg):
    r, g, b = (rgb[..., i].astype(np.int32) for i in range(3))
    lum = (r + g + b) / 3
    return fg & (lum < 88) & ((b - r) < 10)


def paint_labels(cfg, shape):
    """ảnh nhãn từ đa giác / dải, vẽ sau → trước (lớp trước đè)."""
    names = list(cfg["P"])
    L = np.zeros(shape, np.int32)
    for n in cfg.get("pri", names):
        i = names.index(n) + 1
        d = cfg["P"][n]
        if "pg" in d:
            cv2.fillPoly(L, [np.array(d["pg"], np.int32)], i)
        else:
            cv2.polylines(L, [np.array(d["cl"], np.int32)], False, i, thickness=2 * d["r"])
            for p in d["cl"][-1:]:
                cv2.circle(L, tuple(int(v) for v in p), d["r"], i, -1)
    return L, names


def label(rgb, cfg):
    H, W = rgb.shape[:2]
    fg = fg_mask(rgb)
    ink = ink_mask(rgb, fg)
    PL, names = paint_labels(cfg, (H, W))
    lab = np.zeros((H, W), np.int32)
    free = (fg & ~ink).astype(np.uint8)
    n, cc = cv2.connectedComponents(free, connectivity=4)
    flat_cc = cc.ravel()
    flat_pl = PL.ravel()
    order = np.argsort(flat_cc, kind="stable")
    sc = flat_cc[order]
    starts = np.searchsorted(sc, np.arange(n + 1))
    split = 0
    for c in range(1, n):
        idx = order[starts[c]:starts[c + 1]]
        if len(idx) == 0:
            continue
        v = flat_pl[idx]
        cnt = np.bincount(v, minlength=len(names) + 1)
        cnt[0] = 0
        if cnt.sum() == 0:
            continue
        best = int(cnt.argmax())
        if len(idx) > 400 and cnt[best] < 0.8 * cnt.sum():
            # cụm vắt qua nhiều bộ phận: chia theo điểm ảnh (chỗ ngoài mọi đa giác lấy nhãn chiếm đa số)
            vv = np.where(v > 0, v, best)
            lab.ravel()[idx] = vv
            split += 1
        else:
            lab.ravel()[idx] = best
    # lọc màu
    for ln, (kind, fb) in cfg.get("loc", {}).items():
        i, j = names.index(ln) + 1, names.index(fb) + 1
        mm = (lab == i).astype(np.uint8)
        nn, c3 = cv2.connectedComponents(mm, connectivity=4)
        for c in range(1, nn):
            pm = c3 == c
            mc = rgb[pm].mean(0)
            ok = (mc[0] > mc[1] + 45) if kind == "do" else (mc[1] > mc[0] + 25 and mc[1] > mc[2] - 10)
            if not ok:
                lab[pm] = j
    # ép theo đa giác (vùng không có nét mực ngăn, như cằm liền mặt)
    for ne in cfg.get("ep", []):
        i = names.index(ne) + 1
        pm = np.zeros((H, W), np.uint8)
        cv2.fillPoly(pm, [np.array(cfg["P"][ne]["pg"], np.int32)], 1)
        lab[(pm > 0) & fg & ~ink & (rgb.min(2) < 150)] = i   # bỏ điểm sáng (nanh kem đè lên môi dưới)
    # nét mực (và mẩu chưa nhãn): nhãn gần nhất; nét nằm GIỮA hai vùng (cả hai cách không quá gần nhất + 6 px, tức là ranh chung)
    # thì về lớp vẽ TRƯỚC, nên lớp trước giữ trọn viền; viền ngoài giáp nền trắng vẫn của chính vùng đó
    k3 = np.ones((3, 3), np.uint8)
    rest = fg & (lab == 0)
    best_d = np.full((H, W), 1e9, np.float32)
    D = {}
    for i in range(1, len(names) + 1):
        src = (lab != i).astype(np.uint8)
        if src.all():
            continue
        D[i] = cv2.distanceTransform(src, cv2.DIST_L2, 3)
        best_d = np.minimum(best_d, D[i])
    pick = np.zeros((H, W), np.int32)
    for i in sorted(D):                       # tăng dần = từ sau ra trước: lớp sau cùng thoả điều kiện thắng
        ok = rest & (D[i] <= best_d + 6.0)
        pick[ok] = i
    lab[rest] = pick[rest]
    # mẩu vụn (< 120 px) của một nhãn nằm tách khỏi khối chính: theo nhãn bao quanh
    for i in range(1, len(names) + 1):
        m = (lab == i).astype(np.uint8)
        nn, c2, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
        if nn <= 2:
            continue
        big = 1 + int(np.argmax(st[1:, 4]))
        for j in range(1, nn):
            if j != big and st[j, 4] < 120:
                pm = c2 == j
                ring = (cv2.dilate(pm.astype(np.uint8), k3, iterations=2) > 0) & ~pm & fg
                vals = lab[ring]
                vals = vals[vals != i]
                if len(vals):
                    lab[pm] = np.bincount(vals).argmax()
    print(f"nhãn: {len(names)} lớp, {n - 1} cụm màu, {split} cụm chia theo điểm ảnh")
    return lab, names, fg, ink


def save_nhan(rgb, lab, names, out):
    n = len(names)
    hsv = np.zeros((n + 1, 1, 3), np.uint8)
    for i in range(1, n + 1):
        hsv[i, 0] = ((i * 47) % 180, 200 if i % 2 else 140, 250 if i % 3 else 190)
    pal = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)[:, 0].astype(np.float64)
    pal[0] = 255
    vis = (0.25 * rgb + 0.75 * pal[lab])
    edge = (cv2.dilate(lab.astype(np.float32), np.ones((3, 3))) != cv2.erode(lab.astype(np.float32), np.ones((3, 3))))
    vis[edge] = 0
    vis = vis.astype(np.uint8)
    im = Image.fromarray(vis)
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
    for i, n in enumerate(names, 1):
        ys, xs = np.where(lab == i)
        if len(xs):
            d.text((int(np.median(xs)) - 20, int(np.median(ys)) - 9), n, fill=(0, 0, 0), font=f)
    im.save(out)


def build_layers(k):
    cfg = CFG[k]
    rgb = np.array(Image.open(path(k, "tai_ve", "L1_duyet.png")).convert("RGB"))
    H, W = rgb.shape[:2]
    lab, names, fg, ink = label(rgb, cfg)
    out = path(k, "manh_lai")
    os.makedirs(out, exist_ok=True)
    save_nhan(rgb, lab, names, os.path.join(out, "nhan.png"))
    idx = {n: i for i, n in enumerate(names, 1)}
    if len(cfg["toi"]) == 3:          # màu lòng cửa cho thẳng (concept không có mảng tối đủ lớn để lấy mẫu)
        toi = np.array(cfg["toi"], np.uint8)
    else:
        x0, y0, x1, y1 = cfg["toi"]
        toi = np.median(rgb[y0:y1, x0:x1].reshape(-1, 3), 0).astype(np.uint8)
    info = {"size": [W, H], "lop": {}}
    k3 = np.ones((3, 3), np.uint8)
    for n in names:
        m = lab == idx[n]
        # nét mực chung với lớp TRƯỚC (đã về lớp trước) chép thêm vào lớp này: mỗi lớp giữ trọn viền khi lệch nhau
        own = m & ~ink
        dup = set()
        for key, (px, over, opt) in cfg["G"].items():
            if key.split("#")[0] == n:
                dup |= {idx[o] for o in over if idx[o] > idx[n]}
        if own.any() and dup:
            # chỉ chép viền chung với các lớp trên mà lớp này thật sự nằm dưới (khai trong G), kẻo mẩu viền ma của lớp bên cạnh
            dn = cv2.distanceTransform((~own).astype(np.uint8), cv2.DIST_L2, 3)
            m = m | (ink & (dn <= 7.5) & np.isin(lab, list(dup)))
        col = rgb.copy()
        alpha = m.copy()
        grow_all = np.zeros((H, W), bool)
        no_edge = np.zeros((H, W), bool)
        for key, (px, over, opt) in cfg["G"].items():
            if key.split("#")[0] != n:
                continue
            over_m = np.zeros((H, W), bool)
            bad = [o for o in over if idx[o] <= idx[n]]
            if bad:
                print(f"  ! {n}: bỏ {bad} (lớp vẽ sau nó, mọc dưới đó sẽ che chúng)")
            for o in [o for o in over if idx[o] > idx[n]]:
                over_m |= lab == idx[o]
            d = cfg["P"][n]
            ax = d.get("truc") or d.get("cl")
            if opt.get("truc") and ax:
                # ống nối dài theo trục lùi về gốc, bề dày = bề dày lớp ở gốc
                p0, p1 = np.array(ax[0], float), np.array(ax[1], float)
                u = (p0 - p1) / (np.linalg.norm(p0 - p1) + 1e-9)
                dist = cv2.distanceTransform((~m).astype(np.uint8), cv2.DIST_L2, 3)
                r = d.get("r") or 30
                tube = np.zeros((H, W), np.uint8)
                cv2.line(tube, tuple(int(v) for v in p0 + u * 6), tuple(int(v) for v in p0 + u * px), 1, thickness=int(2 * r))
                cv2.circle(tube, tuple(int(v) for v in p0 + u * px), int(r), 1, -1)
                near = (tube > 0) | (dist <= 8)
            else:
                near = cv2.dilate(m.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * px + 1, 2 * px + 1))) > 0
            if opt.get("khep"):
                rk = int(opt["khep"])
                ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * rk + 1, 2 * rk + 1))
                pad = rk + 2
                mm = np.pad(m.astype(np.uint8), pad)
                closed = cv2.morphologyEx(mm, cv2.MORPH_CLOSE, ker)[pad:-pad, pad:-pad] > 0
                near &= closed | (cv2.dilate(m.astype(np.uint8), k3, iterations=6) > 0)
            if opt.get("cat"):
                cm = np.zeros((H, W), np.uint8)
                if opt["cat"] == "elip":
                    (ex, ey), (ea, eb) = opt["elip"]
                    cv2.ellipse(cm, (int(ex), int(ey)), (int(ea), int(eb)), 0, 0, 360, 1, -1)
                else:
                    cv2.fillPoly(cm, [np.array(opt["cat"], np.int32)], 1)
                near &= cm > 0
            grow = near & over_m & ~alpha
            # chỉ giữ phần mọc thêm liền với lớp (dải rời vô dụng, lại lộ khi lớp lệch)
            nn, cc2 = cv2.connectedComponents((grow | alpha).astype(np.uint8), connectivity=8)
            keep = np.unique(cc2[alpha])
            grow &= np.isin(cc2, keep[keep > 0])
            if not grow.any():
                continue
            if opt.get("toi"):
                noise = np.random.RandomState(3).randint(-6, 7, (H, W, 1))
                col[grow] = np.clip(toi[None, :].astype(int) + noise[grow], 0, 255).astype(np.uint8)
            else:
                # inpaint từ màu của chính lớp: nguồn = điểm ảnh lớp, bỏ nét mực sát chỗ mọc thêm
                src_bad = grow | (ink & (cv2.dilate(grow.astype(np.uint8), k3, iterations=9) > 0)) | ~alpha
                bx = np.where(grow | m)
                ya, yb = max(0, bx[0].min() - 8), min(H, bx[0].max() + 9)
                xa, xb = max(0, bx[1].min() - 8), min(W, bx[1].max() + 9)
                sub = col[ya:yb, xa:xb].copy()
                msk = src_bad[ya:yb, xa:xb].astype(np.uint8) * 255
                med = np.median(rgb[m & ~ink].reshape(-1, 3), 0).astype(np.uint8) if (m & ~ink).any() else np.array(INK, np.uint8)
                outside = (~alpha & ~grow)[ya:yb, xa:xb]
                sub[outside] = med
                fixed = cv2.inpaint(sub, msk, 7, cv2.INPAINT_TELEA)
                g2 = grow[ya:yb, xa:xb]
                sub2 = col[ya:yb, xa:xb]
                sub2[g2] = fixed[g2]
                col[ya:yb, xa:xb] = sub2
            alpha |= grow
            grow_all |= grow
            if opt.get("vien") is False:
                no_edge |= grow
        if grow_all.any():
            # mép phần mọc thêm: làm trơn, kẻ nét mực (lúc nghỉ khuất dưới lớp trên)
            a8 = alpha.astype(np.uint8) * 255
            a8 = cv2.GaussianBlur(a8, (0, 0), 1.6)
            sm = a8 > 127
            sm = (sm & ~m & grow_all) | m
            edge = sm & ~(cv2.erode(sm.astype(np.uint8), k3, iterations=4) > 0) & grow_all & ~no_edge
            col[edge] = INK
            alpha = sm
        ys, xs = np.where(alpha)
        if len(xs) == 0:
            print("  trống:", n)
            continue
        bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
        a = (alpha[by0:by1, bx0:bx1] * 255).astype(np.uint8)
        im = np.dstack([col[by0:by1, bx0:bx1], a])
        Image.fromarray(im, "RGBA").save(os.path.join(out, n + ".png"))
        d = cfg["P"][n]
        info["lop"][n] = {"x0": int(bx0), "y0": int(by0), "w": int(bx1 - bx0), "h": int(by1 - by0), "dt": int(m.sum()),
                          "mo": int(grow_all.sum())}
        if "cl" in d:
            info["lop"][n]["cl"] = d["cl"]
        print(f"  {n:11s} {bx1 - bx0:4d}×{by1 - by0:<4d} điểm {int(m.sum()):6d}  mọc thêm {int(grow_all.sum()):5d}")
    json.dump(info, open(os.path.join(out, "lai.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # kiểm: ghép lại mọi lớp (chỉ phần gốc, đúng thứ tự) phải trùng concept
    comp = np.full((H, W, 3), 255, np.uint8)
    for n in names:
        if n not in info["lop"]:
            continue
        t = info["lop"][n]
        im = np.array(Image.open(os.path.join(out, n + ".png")))
        a = im[..., 3:4] / 255.0
        sl = (slice(t["y0"], t["y0"] + t["h"]), slice(t["x0"], t["x0"] + t["w"]))
        comp[sl] = (comp[sl] * (1 - a) + im[..., :3] * a).astype(np.uint8)
    diff = np.abs(comp.astype(int) - np.where(fg[..., None], rgb, 255).astype(int)).max(2)
    print(f"ghép lại so concept: lệch > 40 ở {int((diff > 40).sum())} điểm ảnh ({(diff > 40).sum() / fg.sum() * 100:.2f}% hình)")
    Image.fromarray(comp).save(os.path.join(out, "ghep_lai.png"))


def mat_nham(k):
    """mắt nhắm (mí) làm từ chính lớp mắt đã cắt: tròng (vùng kín chứa tâm, lấp cả con ngươi, chấm sáng) tô màu nắp mí lấy hạt
    từ nắp mí thật (vân sáp giữ), kẻ một nét mực cong xuống ở nửa dưới. Ra <mắt>_nham.png cùng cỡ, cùng gốc với <mắt>.png: phủ kín
    đúng tròng (in số điểm tròng còn hở)."""
    cfg = CFG[k]
    out = path(k, "manh_lai")
    info = json.load(open(os.path.join(out, "lai.json"), encoding="utf-8"))
    rgb = np.array(Image.open(path(k, "tai_ve", "L1_duyet.png")).convert("RGB"))
    for n, (c, r, box) in cfg["mat"].items():
        t = info["lop"][n]
        im = np.array(Image.open(os.path.join(out, n + ".png")).convert("RGBA"))
        h, w = im.shape[:2]
        sub = im[..., :3]
        a = im[..., 3] > 0
        fgl = a
        inkl = ink_mask(sub, fgl)
        cx, cy = c[0] - t["x0"], c[1] - t["y0"]
        # tròng = bao lồi của vùng màu ấm (cam) + con ngươi + chấm sáng nằm trong đĩa quanh tâm, nới 2 px tới nét viền
        yy, xx = np.mgrid[0:h, 0:w]
        disk = (xx - cx) ** 2 + (yy - cy) ** 2 <= (1.25 * r) ** 2
        warm = (sub[..., 0] > 150) & (sub[..., 0] > sub[..., 2] + 60) & disk & fgl
        nn, cc = cv2.connectedComponents(warm.astype(np.uint8), connectivity=8)
        if nn > 1:
            big = 1 + int(np.argmax([np.sum(cc == i) for i in range(1, nn)]))
            warm = cc == big
        blue = (sub[..., 2].astype(int) > sub[..., 0].astype(int) + 40) & fgl
        white = (sub.min(2) > 205) & ((xx - cx) ** 2 + (yy - cy) ** 2 <= (1.0 * r) ** 2)
        dark = (sub.max(2) < 110) & ((xx - cx) ** 2 + (yy - cy) ** 2 <= (0.82 * r) ** 2)
        cam = (sub[..., 0].astype(int) > sub[..., 2].astype(int) + 45) & (sub[..., 0] > 85) & disk & fgl
        warm = warm | ((white | dark | cam) & ~blue)
        pts = np.column_stack(np.where(warm))[:, ::-1].astype(np.int32)
        hull = cv2.convexHull(pts)
        ball = np.zeros((h, w), np.uint8)
        cv2.fillPoly(ball, [hull], 1)
        hull_m = ball > 0
        ball = (cv2.dilate(ball, np.ones((3, 3), np.uint8), iterations=8) > 0) & fgl & ~(cv2.erode(blue.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0)
        # giữ nét viền tròng (mực sát mép bao lồi), chỉ con ngươi tối bên trong mới bị phủ
        dedge = cv2.distanceTransform(hull_m.astype(np.uint8), cv2.DIST_L2, 3)
        ball &= ~(inkl & (dedge < 6))
        reg = warm
        x0, y0, x1, y1 = box
        cap = rgb[y0:y1, x0:x1].reshape(-1, 3)
        rng = np.random.RandomState(11)
        pick = cap[rng.randint(0, len(cap), int(ball.sum()))]
        lid = sub.copy()
        lid[ball] = pick
        lid = np.where(ball[..., None], cv2.GaussianBlur(lid, (0, 0), 1.3), sub)
        th = max(3, int(round(r * 0.14)))
        cv2.ellipse(lid, (int(cx), int(cy - 0.05 * r)), (int(0.72 * r), int(0.42 * r)), 0, 18, 162, INK, th, cv2.LINE_AA)

        def con_ho(L_):
            L_ = L_.astype(int)
            return (((L_[..., 0] > 150) & (L_[..., 0] > L_[..., 2] + 60)) | (L_.min(2) > 225)) & fgl & disk

        left = con_ho(lid)
        if left.any():   # mẩu cam sót (sát mép nắp mí, khử răng cưa): tô nốt màu mí
            lid[left] = np.median(cap, 0).astype(np.uint8)
        res = np.dstack([lid, im[..., 3]])
        Image.fromarray(res, "RGBA").save(os.path.join(out, n + "_nham.png"))
        # kiểm phủ: mọi điểm cam / trắng của tròng phải đã đổi màu
        print(f"  {n}_nham: tròng {int(ball.sum())} px, còn hở {int(con_ho(lid).sum())} px (đã tô nốt {int(left.sum())})")


if __name__ == "__main__":
    build_layers(int(sys.argv[1]))
    mat_nham(int(sys.argv[1]))
