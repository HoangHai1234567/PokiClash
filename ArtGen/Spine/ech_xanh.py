# -*- coding: utf-8 -*-
"""Dòng ếch xanh (mã tạm `ech_xanh`, tướng thứ 2 đảo Thủy, 2026-11-11): sửa concept, cắt mảnh, dựng rig, clip.

    py -3 -I ArtGen/Spine/ech_xanh.py bo_chan_xa     bỏ chân sau bên kia khỏi bản người dùng chọn -> tai_ve/L1_sua.png (+ _soi_sua.png)
    py -3 -I ArtGen/Spine/ech_xanh.py cat 1|2        cắt concept dạng k -> inbox/ech_xanh_<k>/manh/ (mảnh, manh.json, _soi.png)
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/ech_xanh.py rig 1|2   dựng rig một dạng (không có evolve) -> inbox/ech_xanh_<k>/rig/
    py -3 -I ArtGen/Spine/quai/khoa.py nang -- py -3 -I ArtGen/Spine/ech_xanh.py all       dạng 2 rồi dạng 1 gộp dạng 2 (clip evolve)

Dạng mới cần toạ độ riêng trong CAT[k] (hạt giống, vùng khuất, nét kẻ nối) và RIG[k] (khớp), đọc trên ảnh concept kẻ lưới.

Người dùng chọn `L1_concept_2.png` (có hai tay trước) và dặn: chân sau bên kia phải bị thân che lúc nghỉ (để lộ trông như thừa
chân), chỉ lộ ra trong animation nào khiến nó lộ. Sửa bằng mã chứ không nhờ GPT vẽ lại (vẽ lại thì lệch dáng cả con): xoá vùng
xanh của chân đó cùng viền mực riêng của nó, giữ viền bụng và bàn tay xa.
Ghi chú thiết kế, mổ xẻ con gốc: inbox/ech_xanh_ghichu.md.
"""
import json
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
CODE = "ech_xanh"


def d_inbox(k):
    return os.path.join(HERE, "inbox", f"{CODE}_{k}")


def load(p):
    return np.array(Image.open(p).convert("RGB"))


def masks(im):
    """Mực (nâu sẫm), xanh lá, kem, trắng nền."""
    r, g, b = [im[..., i].astype(int) for i in range(3)]
    lum = (r + g + b) / 3
    ink = lum < 110
    green = (g > r + 25) & (g > b + 40) & ~ink
    cream = (r > 225) & (g > 210) & (b < 235) & (b > 150) & (r - b > 18) & ~ink
    return ink, green, cream


def comp_at(mask, x, y):
    n, lab = cv2.connectedComponents(mask.astype(np.uint8), connectivity=4)
    if lab[y, x] == 0:
        raise SystemExit(f"hạt giống ({x}, {y}) không nằm trong vùng")
    return lab == lab[y, x]


def dil(m, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.dilate(m.astype(np.uint8), k) > 0


# chân sau bên kia trong L1_concept_2.png: khối xanh bên phải dưới, phía sau bàn tay xa (đọc trên ảnh cắt cận)
FAR_LEG_BOX = (1075, 700, 1240, 890)          # x0, y0, x1, y1: mọi vùng xanh có tâm trong ô này, trừ bàn tay xa
FAR_HAND_SEED = (1000, 880)                    # một điểm xanh trong bàn tay xa (giữ)
BELLY_SEED = (800, 760)                        # một điểm kem trong bụng (giữ viền bụng)


def bo_chan_xa():
    src = os.path.join(d_inbox(1), "tai_ve", "L1_concept_2.png")
    im = load(src)
    ink, green, cream = masks(im)
    n, lab, st, cen = cv2.connectedComponentsWithStats(green.astype(np.uint8), connectivity=4)
    hand_id = lab[FAR_HAND_SEED[1], FAR_HAND_SEED[0]]
    if hand_id == 0:
        raise SystemExit("hạt giống bàn tay xa không nằm trong vùng xanh")
    x0, y0, x1, y1 = FAR_LEG_BOX
    leg = np.zeros(green.shape, bool)
    for i in range(1, n):
        cx, cy = cen[i]
        if i != hand_id and x0 <= cx <= x1 and y0 <= cy <= y1 and st[i, cv2.CC_STAT_AREA] > 30:
            leg |= lab == i
            print(f"  vùng chân xa: tâm ({cx:.0f}, {cy:.0f}), {st[i, cv2.CC_STAT_AREA]} px")
    # ngón của bàn tay xa cũng là các vùng xanh riêng (nét mực ngăn): giữ mọi vùng xanh chạm bàn tay sau khi nới 9 px
    hand = lab == hand_id
    grown = dil(hand, 9)
    for i in range(1, n):
        m = lab == i
        if i != hand_id and (m & grown).any() and (m & leg).any():
            # vùng vừa sát bàn tay vừa trong ô chân: thuộc bàn tay nếu tâm thấp hơn và lệch trái
            cx, cy = cen[i]
            if cx < 1085:
                leg &= ~m
                hand |= m
    belly = comp_at(cream, *BELLY_SEED)
    belly = cv2.morphologyEx(belly.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8)) > 0
    keep = dil(belly, 9) | dil(hand, 9)                   # viền mực của bụng và của bàn tay xa
    erase = dil(leg, 16) & ~keep                           # 16 px: lấy cả viền mực và quầng khử răng cưa của nó
    # mẩu mực rời còn sót quanh chân (nối với vùng xoá, không thuộc viền giữ): xoá nốt
    rest = ink & dil(erase, 4) & ~keep
    erase |= rest
    out = im.copy()
    out[erase] = np.median(im[:60, :60].reshape(-1, 3), axis=0).astype(np.uint8)   # màu giấy của chính ảnh (không hẳn 255)
    # làm mềm mép vừa cắt để không răng cưa: mép giữa vùng xoá và vùng giữ lấy trung bình 3x3 một lần
    edge = dil(erase, 1) & ~erase
    blur = cv2.GaussianBlur(out, (3, 3), 0)
    out[edge] = blur[edge]
    dst = os.path.join(d_inbox(1), "tai_ve", "L1_sua.png")
    Image.fromarray(out).save(dst)
    print("xoá", int(erase.sum()), "px ->", dst)
    # ảnh soi: trước / sau / vùng xoá tô hồng, phóng 2 lần quanh chỗ sửa
    bx0, by0, bx1, by1 = 880, 640, 1300, 940
    a = im[by0:by1, bx0:bx1]
    b = out[by0:by1, bx0:bx1]
    c = a.copy()
    c[erase[by0:by1, bx0:bx1]] = (255, 120, 200)
    sheet = np.concatenate([a, c, b], axis=1)
    sheet = cv2.resize(sheet, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    Image.fromarray(sheet).save(os.path.join(d_inbox(1), "_soi_sua.png"))


# ================================================================ CẮT MẢNH TỪ CONCEPT (cách lai) ================================================================
# Mọi mảnh cắt thẳng từ concept đã duyệt (khớp concept 100 % ở dáng nghỉ). Phần bị che (bụng dưới lưỡi, dưới tay; thân dưới đùi;
# gốc lưỡi dưới môi; cổ tay xa dưới bụng) vẽ bù bằng vân sáp lát từ chỗ sạch của chính ảnh + nét mực kẻ nối theo đường đã đọc trên
# ảnh kẻ lưới. Toạ độ trong CAT và manh.json là pixel concept (1536 x 1024, y xuống).
GRAY = (150, 150, 150)
MUC = 15                      # nét mực dày ~13 px concept: nới vùng tô chừng này là lấy trọn nét

CAT = {
    1: dict(
        seed_than=(540, 600), seed_chan=(420, 745), seed_tay=(640, 750), seed_tay_x=(1040, 872),
        hop_chan=[(290, 640), (548, 640), (548, 915), (290, 915)], hop_tay_x=[(960, 780), (1135, 780), (1135, 915), (960, 915)],
        # tay gần liền màu với thân (không có nét mực ở vai): cắt theo đa giác, cạnh đầu là đường vai
        poly_tay=[(550, 655), (615, 603), (668, 640), (700, 700), (720, 780), (728, 825), (790, 850), (790, 915), (565, 915),
                  (565, 850), (588, 835), (582, 800), (568, 760), (555, 700)],
        vai=[(550, 655), (615, 603)],
        # phần thân xanh khuất dưới tay / dưới đùi (lớp thân mọc thêm vào đây)
        an_tay=[(543, 650), (615, 603), (606, 650), (586, 700), (566, 737), (546, 737)],
        an_chan=[(332, 640), (334, 680), (340, 710), (352, 745), (375, 780), (410, 808), (455, 828), (500, 840), (544, 737),
                 (560, 660), (350, 640)],
        net_than=[[(332, 640), (334, 680), (340, 710), (352, 745), (375, 780), (410, 808), (455, 828), (500, 840)]],
        # phần bụng kem khuất (dưới dải thân xanh, dưới tay và bàn tay, góc dưới đùi) và nét đáy bụng nối qua chỗ bàn tay che
        an_bung=[(565, 600), (640, 575), (740, 700), (800, 860), (820, 878), (790, 877), (760, 876.5), (720, 875.5), (680, 873),
                 (640, 869.5), (600, 864), (572, 859), (556, 856), (540, 851.5), (520, 846), (500, 840), (545, 740)],
        net_bung=[[(500, 840), (520, 846), (540, 851.5), (556, 856), (572, 859), (600, 864), (640, 869.5), (680, 873),
                   (720, 875.5), (760, 876.5), (790, 877), (820, 878)]],      # tâm nét đo trên concept ở hai đoạn còn lộ
        goc_luoi=44,          # gốc lưỡi mọc thêm lên trên, khuất dưới môi trên (px)
        co_tay_x=90,          # cổ tay xa mọc thêm lên trên, khuất dưới bụng (px)
    ),
    # dạng 2: con to gần kín khung, nét mực dày ~15 px, xanh đậm (đốm xanh sẫm tối gần bằng mực nên ngưỡng mực thấp hơn)
    2: dict(
        muc=18, net_day=15, nguong_muc=82, vach=(125, 195), do_nhat=200,
        seed_than=(300, 500), seed_chan=(270, 720), seed_tay=(580, 750), seed_tay_x=(1180, 920),
        hop_chan=[(60, 570), (457, 570), (457, 992), (60, 992)], hop_tay_x=[(1040, 790), (1385, 790), (1385, 992), (1040, 992)],
        poly_tay=[(459, 607), (668, 607), (696, 660), (715, 720), (727, 800), (727, 850), (790, 872), (835, 910), (840, 995), (480, 995),
                  (485, 905), (523, 860), (495, 800), (476, 750), (464, 700), (459.5, 660)],
        vai=[(459, 607), (668, 607)],
        an_tay=[(452, 600), (668, 607), (610, 655), (545, 700), (485, 737), (450, 737)],
        an_chan=[(143.5, 520), (138, 560), (137, 600), (140, 650), (152, 710), (175, 770), (215, 820), (275, 860), (345, 885), (410, 897),
                 (430, 902), (456, 737), (462, 625), (160, 520)],
        net_than=[[(143.5, 520), (138, 560), (137, 600), (140, 650), (152, 710), (175, 770), (215, 820), (275, 860), (345, 885), (410, 897),
                   (430, 902)]],
        an_bung=[(470, 480), (600, 470), (760, 720), (840, 900), (850, 933), (820, 930), (780, 930.5), (720, 931), (660, 931), (600, 929),
                 (540, 925.5), (500, 922.5), (476, 915), (452, 908), (430, 902), (456, 737), (470, 620)],
        net_bung=[[(430, 902), (452, 908), (476, 915), (500, 922.5), (540, 925.5), (600, 929), (660, 931), (720, 931), (780, 930.5),
                   (820, 930), (850, 933)]],
        goc_luoi=62, co_tay_x=130,
    ),
}


def _gian(m, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.dilate(m.astype(np.uint8), k) > 0


def _co(m, r):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    return cv2.erode(m.astype(np.uint8), k) > 0


def _lap_lo(m):
    pad = np.pad((~m).astype(np.uint8), 1, constant_values=1)
    n, lab = cv2.connectedComponents(pad, connectivity=4)
    return m | ((pad[1:-1, 1:-1] > 0) & (lab[1:-1, 1:-1] != lab[0, 0]))


def _poly(shape, pts):
    m = np.zeros(shape, np.uint8)
    cv2.fillPoly(m, [np.round(np.array(pts, float) * 8).astype(np.int32)], 1, shift=3)
    return m > 0


def _duong(pts, buoc=2.0):
    """đường cong trơn (Catmull-Rom) qua các điểm, lấy mẫu dày."""
    P = np.array(pts, float)
    Q = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(1, len(Q) - 2):
        n = max(2, int(np.hypot(*(Q[i + 1] - Q[i])) / buoc))
        for u in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * Q[i]) + (-Q[i - 1] + Q[i + 1]) * u + (2 * Q[i - 1] - 5 * Q[i] + 4 * Q[i + 1] - Q[i + 2]) * u * u
                              + (-Q[i - 1] + 3 * Q[i] - 3 * Q[i + 1] + Q[i + 2]) * u ** 3))
    out.append(P[-1])
    return np.array(out)


NET_DAY = 12.5


def _net(shape, pts, day=None):
    """độ phủ 0..1 của một nét bút trơn qua các điểm (khử răng cưa)."""
    m = np.zeros(shape, np.uint8)
    C = np.round(_duong(pts) * 16).astype(np.int32)
    cv2.polylines(m, [C], False, 255, thickness=int(round(day or NET_DAY)), lineType=cv2.LINE_AA, shift=4)
    return m.astype(np.float32) / 255.0


def _nen(a, nguong=236):
    w = (a.min(2) >= nguong).astype(np.uint8)
    n, lab = cv2.connectedComponents(w, connectivity=4)
    mep = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    return np.isin(lab, mep[mep != 0]) & (w > 0)


def _tai(mask, x, y, ket_noi=4):
    n, lab = cv2.connectedComponents(mask.astype(np.uint8), connectivity=ket_noi)
    if lab[y, x] == 0:
        raise SystemExit(f"hạt giống ({x}, {y}) không nằm trong vùng")
    return lab == lab[y, x]


def _van(a, ok, s=72):
    """vân sáp lát kín cả ảnh từ một ô sạch s x s nằm trọn trong `ok` (ô gần tâm vùng nhất), nối liền mép bằng cách trộn với chính
    nó dịch nửa ô."""
    ii = cv2.integral(ok.astype(np.uint8))
    full = (ii[s:, s:] - ii[:-s, s:] - ii[s:, :-s] + ii[:-s, :-s]) == s * s
    ys, xs = np.nonzero(full)
    if not len(xs):
        raise SystemExit("không có ô sạch để lấy vân")
    oy, ox = np.nonzero(ok)
    i = int(np.argmin((xs + s / 2 - ox.mean()) ** 2 + (ys + s / 2 - oy.mean()) ** 2))
    T = a[ys[i]:ys[i] + s, xs[i]:xs[i] + s].astype(np.float32)
    w1 = 0.5 - 0.5 * np.cos(2 * np.pi * (np.arange(s) + 0.5) / s)
    w = np.minimum(1.0, 1.6 * np.outer(w1, w1) ** 0.5)[..., None]
    Ts = T * w + np.roll(T, (s // 2, s // 2), axis=(0, 1)) * (1 - w)
    H, W = a.shape[:2]
    return np.tile(Ts, (H // s + 1, W // s + 1, 1))[:H, :W], (int(xs[i]), int(ys[i]))


def _alpha(m):
    return np.where(_co(m, 2), 1.0, cv2.GaussianBlur(m.astype(np.float32), (0, 0), 0.7))


def _hop(m, le=3):
    ys, xs = np.nonzero(m)
    return [max(0, int(xs.min()) - le), max(0, int(ys.min()) - le), min(m.shape[1], int(xs.max()) + 1 + le),
            min(m.shape[0], int(ys.max()) + 1 + le)]


def _luu(a, alpha, box, path):
    x0, y0, x1, y1 = box
    rgba = np.dstack([np.clip(a[y0:y1, x0:x1], 0, 255).astype(np.uint8), (np.clip(alpha[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8)])
    Image.fromarray(rgba, "RGBA").save(path)


def phan_mau(a, nguong_muc=118):
    """phân vùng màu của concept: nền, hình, mực, xanh, kem, đỏ, vàng. nguong_muc: tối hơn mức này là mực (dạng có đốm xanh sẫm thì hạ)."""
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    bg = _nen(a)
    n, lab, st, _ = cv2.connectedComponentsWithStats((~bg).astype(np.uint8), connectivity=8)
    fg = lab == 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))          # bỏ mẩu rời (vết xoá chân cũ)
    ink = fg & (a.max(2) < nguong_muc)
    green = fg & (G > R + 25) & (G > B + 40) & ~ink
    red = fg & (R > 120) & (G < 105) & (B < 105) & (R > G + 60) & ~ink
    yellow = fg & (R > 215) & (G > 180) & (B < 150) & ~green
    cream = fg & ~ink & ~green & ~red & ~yellow & (R > 200) & (G > 190) & (B > 140) & (R - B > 8)
    cream = (cv2.morphologyEx(cream.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) > 0) & fg & ~ink & ~green & ~red & ~yellow
    # bỏ sợi mảnh (mép khử răng cưa mực-trắng quanh hình cũng ngả kem): mở 7 px, giữ cụm lớn, rồi lấy lại mép 3 px
    core = cv2.morphologyEx(cream.astype(np.uint8), cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(core, connectivity=4)
    core = np.isin(lab, [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 1500])
    cream = cream & _gian(core, 3)
    return dict(bg=~fg, fg=fg, ink=ink, green=green, red=red, yellow=yellow, cream=cream)


def cat(k):
    global MUC, NET_DAY
    c = CAT[k]
    MUC, NET_DAY = c.get("muc", 15), c.get("net_day", 12.5)
    src = os.path.join(d_inbox(k), "tai_ve", c.get("src", "L1_duyet.png"))
    a = np.array(Image.open(src).convert("RGB")).astype(np.float32)
    H, W = a.shape[:2]
    pm = phan_mau(a, c.get("nguong_muc", 118))
    fg, ink, green, red, yellow, cream = pm["fg"], pm["ink"], pm["green"], pm["red"], pm["yellow"], pm["cream"]
    ra = os.path.join(d_inbox(k), "manh")
    os.makedirs(ra, exist_ok=True)

    than_lien = _tai(green, *c["seed_than"])
    chan = green & ~than_lien & _poly((H, W), c["hop_chan"])            # đùi + bàn chân + các ngón (cụm xanh rời thân trong hộp)
    tay_x = green & ~than_lien & _poly((H, W), c["hop_tay_x"])
    if not chan[c["seed_chan"][1], c["seed_chan"][0]] or not tay_x[c["seed_tay_x"][1], c["seed_tay_x"][0]]:
        raise SystemExit("đùi hoặc bàn tay xa liền vùng xanh với thân: nét mực hở, phải kẻ tay")
    P_tay = _poly((H, W), c["poly_tay"])
    tay = _tai(than_lien & P_tay, *c["seed_tay"]) | (green & ~than_lien & ~chan & ~tay_x & P_tay)
    xanh_than = green & ~chan & ~tay_x & ~tay
    fills = dict(chan=chan, tay=tay, tay_x=tay_x, bung=cream, luoi=red, than=xanh_than | yellow)

    def lay(ten):
        khac = np.zeros((H, W), bool)
        for t, f in fills.items():
            if t != ten:
                khac |= f
        return _gian(fills[ten], MUC) & fg & ~_gian(khac, 2)

    muc = np.median(a[fg & (a.max(2) < 70)], axis=0)                  # màu mực
    g_xanh = float(np.median(a[..., 1][xanh_than]))
    van_xanh, o1 = _van(a, _co(xanh_than, 6) & (a[..., 1] > g_xanh - 30))     # ô sạch: không dính đốm xanh đậm
    van_kem, o2 = _van(a, _co(cream, 6))
    info = {"concept": os.path.basename(src), "cỡ": [W, H], "manh": {}, "mực": [float(v) for v in muc]}
    out = {}

    def ke(img, m_net, vung):
        """kẻ nét mực m_net (0..1) lên img, chỉ trong `vung` (chỗ vẽ bù)."""
        m = (m_net * cv2.GaussianBlur(vung.astype(np.float32), (0, 0), 1.2))[..., None]
        return img * (1 - m) + muc * m

    # ---- thân xanh (đầu, lưng, dải hông, hai mắt): bỏ nét mực của đùi và của tay, mọc thêm dưới đùi, dưới tay
    M0 = _lap_lo(lay("than"))
    bo = (_gian(chan, MUC + 2) | (_gian(tay, MUC + 2) & _gian(P_tay, MUC))) & ~fills["than"]
    giu = M0 & ~_gian(bo, 3)
    an = _poly((H, W), c["an_chan"]) | _poly((H, W), c["an_tay"])
    giu &= ~an | (_co(xanh_than, 1) & ~_gian(bo, 9))                     # trong vùng khuất chỉ giữ điểm xanh chắc chắn (bỏ mép mực nhạt)
    nets = [_net((H, W), pts) for pts in c["net_than"]]
    M = giu | an
    for nm in nets:
        M |= nm > 0.5
    bu = M & ~giu
    mb = cv2.GaussianBlur(bu.astype(np.float32), (0, 0), 1.0)[..., None]
    X = a * (1 - mb) + van_xanh * mb
    for nm in nets:
        X = ke(X, nm, bu)
    n_, lab_, st_, _c = cv2.connectedComponentsWithStats(M.astype(np.uint8), connectivity=8)       # bỏ mẩu rời (sót nét mực của mảnh khác)
    M = np.isin(lab_, [i for i in range(1, n_) if st_[i, cv2.CC_STAT_AREA] > 3000])
    out["than"] = (X, _alpha(M), M)

    # ---- bụng kem (hàm dưới + bụng): bỏ nét mực của lưỡi, tay, đùi; lấp chỗ lưỡi, tay che; nét đáy nối qua chỗ bàn tay che
    M0 = lay("bung")
    rieng = M0 & ~cream
    bo = rieng & (_gian(tay, MUC + 2) | _gian(chan, MUC + 2) | (_gian(red, MUC + 2) & ~_gian(xanh_than, 12)))
    moi = fg & ~cream & ~red & ~green & _gian(red, MUC + 2) & _gian(xanh_than, 12)     # đoạn nét môi nằm trên gốc lưỡi
    giu = ((cream | (rieng & ~bo)) & ~_gian(bo, 3)) | moi
    AB = _poly((H, W), c["an_bung"])
    giu &= ~AB | cream                                                    # trong vùng khuất của bụng không giữ nét mực nào (nét vai, nét tay)
    nets = [_net((H, W), pts) for pts in c["net_bung"]]
    M = (M0 & ~bo) | moi | AB
    for nm in nets:
        M |= nm > 0.5
    M = _lap_lo(M)
    bu = M & ~giu
    mb = cv2.GaussianBlur(bu.astype(np.float32), (0, 0), 1.0)[..., None]
    X = a * (1 - mb) + van_kem * mb
    for nm in nets:
        X = ke(X, nm, bu)
    out["bung"] = (X, _alpha(M), M)

    # ---- lưỡi: cắt khỏi nét môi, gốc mọc thêm lên trên bằng cách chép dải ngay dưới môi
    M = _lap_lo(lay("luoi")) & ~_gian(xanh_than, 11)
    X = a.copy()
    ys = np.nonzero(M.any(1))[0]
    y0, g = int(ys.min()) + 8, c["goc_luoi"]
    M2 = M.copy()
    M2[:y0] = False
    tx = lambda y: float(np.nonzero(M[y])[0].mean())
    dx = int(round(0.5 * (tx(y0) - tx(y0 + g))))                       # lưỡi hơi xiên: dải chép lên dịch ngang theo độ xiên
    for i in range(g):
        M2[y0 - g + i] = np.roll(M[y0 + i], dx)
        X[y0 - g + i] = np.roll(a[y0 + i], dx, axis=0)
    out["luoi"] = (X, _alpha(M2), M2)

    # ---- đùi + bàn chân gần; tay gần (đầu vai mờ dần vào thân: vai không có nét mực)
    Mc = _lap_lo(lay("chan"))
    out["chan"] = (a, _alpha(Mc), Mc)
    Mt = _lap_lo(lay("tay"))
    p0, p1 = np.array(c["vai"][0], float), np.array(c["vai"][1], float)
    d = (p1 - p0) / np.hypot(*(p1 - p0))
    nrm = np.array([d[1], -d[0]]) if d[0] > 0 else np.array([-d[1], d[0]])     # pháp tuyến chĩa lên (về phía thân)
    yy, xx = np.mgrid[0:H, 0:W]
    s = (xx - p0[0]) * d[0] + (yy - p0[1]) * d[1]
    h = (xx - p0[0]) * nrm[0] + (yy - p0[1]) * nrm[1]
    mo = np.clip(1 - h / 30.0, 0, 1) * (h > -2) * (s > -4) * (s < np.hypot(*(p1 - p0)) + 4) * xanh_than
    al = np.maximum(_alpha(Mt), cv2.GaussianBlur(mo.astype(np.float32), (0, 0), 1.0))
    out["tay"] = (a, al, al > 0.02)

    # ---- bàn tay xa: bỏ nét đáy bụng nằm trên nó, cổ tay mọc thêm lên trên (khuất dưới bụng)
    Mh = _lap_lo(lay("tay_x"))
    bo_h = ~tay_x & _gian(cream, MUC + 4)
    Mh &= ~bo_h
    X = a.copy()
    sua = Mh & _gian(bo_h, 4) & ~ink
    X[sua] = van_xanh[sua]
    cot = (~tay_x & _gian(cream, MUC + 4) & _gian(tay_x, MUC)).any(0)    # các cột bàn tay chui dưới bụng: chỉ kéo dài các cột này
    cot = cv2.erode(cot.astype(np.uint8)[None], np.ones((1, 9), np.uint8))[0] > 0
    quet = Mh.copy()
    goc_cot = Mh & cot[None, :]
    for dy in range(2, c["co_tay_x"] + 1, 2):
        quet[:-dy] |= goc_cot[dy:]
    quet = _lap_lo(quet)
    moi = quet & ~Mh
    X[moi] = van_xanh[moi]
    vien = moi & ~_co(quet, 12)
    mv = cv2.GaussianBlur(vien.astype(np.float32), (0, 0), 1.0)[..., None]
    X = X * (1 - mv) + muc * mv
    out["tay_x"] = (X, _alpha(quet), quet)

    for ten, (X, al, M) in out.items():
        box = _hop(al > 0.02)
        _luu(X, al, box, os.path.join(ra, ten + ".png"))
        info["manh"][ten] = box
    phu(k, a, pm, xanh_than, van_xanh, muc, info, ra)
    json.dump(info, open(os.path.join(ra, "manh.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # ---- tờ soi: ghép lại so với concept; từng lớp có vẽ bù đặt riêng trên nền xám
    def nen():
        return Image.new("RGBA", (W, H), GRAY + (255,))

    def dan(im, ten, dx=0, dy=0):
        p = Image.open(os.path.join(ra, ten + ".png"))
        im.alpha_composite(p, (info["manh"][ten][0] + dx, info["manh"][ten][1] + dy))

    ghep = nen()
    for ten in THU_TU:
        if ten in info["manh"]:
            dan(ghep, ten)
    goc = nen()
    goc.alpha_composite(Image.fromarray(np.dstack([a.astype(np.uint8), np.where(fg, 255, 0).astype(np.uint8)]), "RGBA"))
    dff = np.abs(np.array(ghep.convert("RGB")).astype(int) - np.array(goc.convert("RGB")).astype(int)).max(2)
    khac = Image.fromarray(np.dstack([np.clip(dff * 4, 0, 255)] * 3).astype(np.uint8)).convert("RGBA")
    t_than, t_bung, t_roi = nen(), nen(), nen()
    dan(t_than, "than")
    dan(t_bung, "bung")
    dan(t_roi, "tay_x", 60, -40)
    dan(t_roi, "luoi", -40, -60)
    dan(t_roi, "chan", -60, 20)
    dan(t_roi, "tay", -330, 30)
    o = [(ghep, "1. ghép lại"), (goc, "2. concept"), (khac, "3. khác nhau (x4)"), (t_than, "4. lớp thân xanh (đã vẽ bù dưới đùi, dưới tay)"),
         (t_bung, "5. lớp bụng (đã vẽ bù dưới lưỡi, tay)"), (t_roi, "6. lưỡi, đùi, tay, bàn tay xa (đặt lệch)")]
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
    x0, y0, x1, y1 = _hop(fg, 40)
    cw, ch = (x1 - x0) * 3 // 4, (y1 - y0) * 3 // 4
    to = Image.new("RGBA", (cw * 3, ch * 2), (60, 60, 60, 255))
    for i, (im, chu) in enumerate(o):
        q = im.crop((x0, y0, x1, y1)).resize((cw, ch), Image.LANCZOS)
        ImageDraw.Draw(q).text((10, 6), chu, fill=(255, 255, 255, 255), font=f)
        to.alpha_composite(q, ((i % 3) * cw, (i // 3) * ch))
    to.convert("RGB").save(os.path.join(ra, "_soi.png"))
    print(f"dạng {k}: {info['manh']}; ô vân xanh {o1}, kem {o2}; khác concept tối đa {int(dff.max())}, {int((dff > 24).sum())} px lệch > 24"
          f" -> {os.path.join(ra, '_soi.png')}")
    return info


# ---------------------------------------------------------------- mảnh dựng bằng mã từ concept: lưỡi dài, lòng miệng, mí nhắm
DAI_LUOI = 1010                 # dài lưỡi dài (px concept); clip còn kéo giãn thêm lúc bắn
LUOI_HEP = 0.40                # lưỡi bắn nhìn ngang: phần thịt hẹp còn chừng này so với lưỡi buông (nhìn chính diện)
HONG = (560, 260)              # cỡ ảnh vòm họng (px concept)
MAU_VOM = (138, 26, 24)        # vòm họng (đậm hơn lưỡi). Không vẽ sàn miệng: nhìn ngang thì không thấy mặt trên hàm dưới


def phu(k, a, pm, xanh_than, van_xanh, muc, info, ra):
    H, W = a.shape[:2]
    red, cream, ink, yellow = pm["red"], pm["cream"], pm["ink"], pm["yellow"]
    # ---- tâm nét môi (ranh thân xanh / bụng, lưỡi): điểm đo trên concept, từ khoé tới chóp
    net = ~xanh_than & ~cream & ~red & pm["fg"] & _gian(xanh_than, 13) & _gian(cream | red, 13)
    moi = []
    xs = np.nonzero(net.any(0))[0]
    for x in range(int(xs.min()) + 14, int(xs.max()) - 6, 26):
        ys = np.nonzero(net[:, x])[0]
        if len(ys) and ys.max() - ys.min() < 40:
            moi.append([float(x), float(ys.mean())])
    info["moi"] = moi

    # ---- lưỡi dài: duỗi thẳng lưỡi ngắn (mỗi hàng co về bề rộng chuẩn, vạch giữa về đúng giữa), lát đoạn giữa cho đủ dài, giữ đầu lưỡi
    T = np.array(Image.open(os.path.join(ra, "luoi.png")).convert("RGBA")).astype(np.float32)
    al = T[..., 3] > 128
    h, w = al.shape
    rows = np.nonzero(al.any(1))[0]
    xl = np.array([np.nonzero(al[y])[0].min() for y in rows], float)
    xr = np.array([np.nonzero(al[y])[0].max() + 1 for y in rows], float)
    v0, v1 = CAT[k].get("vach", (150, 210))
    vach = al & (T[..., 0] > v0) & (T[..., 0] < v1) & (T[..., 1] < 46)
    xc = np.array([np.nonzero(vach[y])[0].mean() if vach[y].sum() >= 4 else np.nan for y in rows])
    co_v = ~np.isnan(xc)
    y_v = rows[co_v]

    def muot(v, r=9):                                                  # làm mượt dọc lưỡi (mép và vạch giữa đo từng hàng bị rung)
        q = np.pad(v, r, mode="edge")
        return np.convolve(q, np.ones(2 * r + 1) / (2 * r + 1), mode="valid")

    xc = np.interp(rows, y_v, xc[co_v])
    xc[rows > y_v.max()] = np.nan
    xl, xr = muot(xl), muot(xr)
    xc = np.where(np.isnan(xc), np.nan, muot(np.where(np.isnan(xc), xc[co_v][-1], xc)))
    yv0, yv1 = int(y_v.min()), int(y_v.max())                          # đoạn có vạch giữa
    frac = float(np.median((xc[co_v] - xl[co_v]) / (xr[co_v] - xl[co_v])))
    Wd = int(round(np.median((xr - xl)[(rows > yv0) & (rows < yv1)])))
    y_dau = yv1 - 30                                                   # từ đây trở xuống là đầu lưỡi: giữ nguyên dáng

    def hang(y):
        """hàng y của lưỡi co về bề rộng Wd, vạch giữa về frac·Wd."""
        i = int(np.searchsorted(rows, y))
        c = xc[i] if not np.isnan(xc[i]) else xl[i] + frac * (xr[i] - xl[i])
        u = np.arange(Wd) + 0.5
        sx = np.where(u < frac * Wd, xl[i] + (c - xl[i]) * u / (frac * Wd), c + (xr[i] - c) * (u - frac * Wd) / ((1 - frac) * Wd))
        mp = np.clip(sx, 0, w - 1.001).astype(np.float32)[None]
        return cv2.remap(T, mp, np.full_like(mp, float(y)), cv2.INTER_LINEAR)[0]

    than_l = np.stack([hang(y) for y in range(int(rows.min()), y_dau)])          # gốc + thân lưỡi
    giua = np.stack([hang(y) for y in range(yv0 + 30, y_dau)])                   # đoạn lát (có vạch giữa suốt)
    i0 = int(np.searchsorted(rows, y_dau))
    sc = Wd / (xr[i0] - xl[i0])
    dau = T[y_dau:int(rows.max()) + 1]
    x0d = int(np.floor(xl[i0])) - 6
    dau = dau[:, max(0, x0d):]
    dau = cv2.resize(dau, (int(round(dau.shape[1] * sc)), dau.shape[0]), interpolation=cv2.INTER_LINEAR)
    le = int(round((xl[i0] - max(0, x0d)) * sc))                                  # lề trái của đầu lưỡi trong ảnh cắt
    rong = max(Wd + 24, dau.shape[1] - le + 24)
    cot = [np.pad(than_l, ((0, 0), (12, rong - Wd - 12), (0, 0)))]
    dai = than_l.shape[0]
    ov = 22
    g2 = np.pad(giua, ((0, 0), (12, rong - Wd - 12), (0, 0)))
    while dai + dau.shape[0] < DAI_LUOI:
        cot.append(g2)
        dai += g2.shape[0] - ov
    d2 = np.zeros((dau.shape[0], rong, 4), np.float32)
    x_off = 12 - le
    src = dau[:, max(0, -x_off):max(0, -x_off) + rong - max(0, x_off)]
    d2[:, max(0, x_off):max(0, x_off) + src.shape[1]] = src
    cot.append(d2)
    out = cot[0]
    for seg in cot[1:]:                                                 # nối chồng ov hàng, hoà dần
        wv = np.linspace(0, 1, ov)[:, None, None]
        mix = out[-ov:] * (1 - wv) + seg[:ov] * wv
        out = np.concatenate([out[:-ov], mix, seg[ov:]])
    # lưỡi bắn nhìn NGANG (người dùng dặn 2026-11-11: bản rộng như lưỡi buông là góc nhìn từ trên xuống): bóp bề ngang của phần
    # thịt còn LUOI_HEP lần, giữ nguyên bề dày nét mực hai mép
    mv = MUC - 2
    Wf = out.shape[1]
    Wn = int(2 * mv + (Wf - 2 * mv) * LUOI_HEP) + 8
    co_h = np.array([(out[y, :, 3] > 40).any() for y in range(out.shape[0])])
    Lm = np.array([np.nonzero(out[y, :, 3] > 40)[0].min() if co_h[y] else np.nan for y in range(out.shape[0])], float)
    Rm = np.array([np.nonzero(out[y, :, 3] > 40)[0].max() + 1 if co_h[y] else np.nan for y in range(out.shape[0])], float)
    yy_ = np.nonzero(co_h)[0]
    Lm, Rm = np.interp(np.arange(len(Lm)), yy_, Lm[co_h]), np.interp(np.arange(len(Rm)), yy_, Rm[co_h])
    y_tron = int(yy_.max()) - 60                                         # thân lưỡi: làm mượt mép (đo từng hàng bị rung); đầu lưỡi giữ nguyên
    Lm[:y_tron], Rm[:y_tron] = muot(Lm, 7)[:y_tron], muot(Rm, 7)[:y_tron]
    jj = np.arange(Wn, dtype=np.float32) + 0.5
    hep = np.zeros((out.shape[0], Wn, 4), np.float32)
    for y in yy_:
        l_, r_ = Lm[y], Rm[y]
        rong = r_ - l_
        if rong <= 2 * mv + 2:
            wn = rong
            x0h = Wn / 2 + ((l_ + r_) / 2 - Wf / 2) * LUOI_HEP - wn / 2
            sx = l_ + (jj - x0h)
        else:
            wi = (rong - 2 * mv) * LUOI_HEP
            wn = 2 * mv + wi
            x0h = Wn / 2 + ((l_ + r_) / 2 - Wf / 2) * LUOI_HEP - wn / 2
            u_ = jj - x0h                                                # vị trí trong lát cắt đã bóp: mép mực - thịt (bóp) - mép mực
            sx = np.where(u_ < mv, l_ + u_, np.where(u_ < mv + wi, l_ + mv + (u_ - mv) / LUOI_HEP, r_ - (wn - u_)))
        trong_ = (jj - x0h >= 0) & (jj - x0h <= wn)
        row = cv2.remap(np.ascontiguousarray(out[y:y + 1]), np.clip(sx, 0, Wf - 1.001).astype(np.float32)[None],
                        np.zeros((1, Wn), np.float32), cv2.INTER_LINEAR)[0]
        hep[y] = row * trong_[:, None]
    out = hep
    im = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA").rotate(90, expand=True)      # gốc bên trái, đầu lưỡi bên phải
    im.save(os.path.join(ra, "luoi_dai.png"))
    info["luoi_dai"] = [im.width, im.height]

    # ---- lòng miệng: nửa trên vòm họng đậm, nửa dưới sàn miệng, nét mực ngăn + nét mực mép trước; vân sáp lấy từ lưỡi
    do_kin = cv2.morphologyEx(red.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8)) > 0
    van_do, _ = _van(a, _co(do_kin, 6) & ~_gian(red & (a[..., 0] < CAT[k].get("do_nhat", 212)), 4), s=48)
    wh, hh = HONG
    v = van_do[:hh, :wh] / np.median(van_do[:hh, :wh].reshape(-1, 3), axis=0)
    yy, xx = np.mgrid[0:hh, 0:wh]
    X = v * np.array(MAU_VOM, np.float32)                                # vòm họng: một màu đậm, nét mực ở mép trước (má bên kia)
    nm = _net((hh, wh), [(wh - 7, -5), (wh - 7, hh + 5)], day=12)
    X = X * (1 - nm[..., None]) + muc * nm[..., None]
    Image.fromarray(np.dstack([np.clip(X, 0, 255), np.full((hh, wh), 255.0)]).astype(np.uint8), "RGBA").save(os.path.join(ra, "hong.png"))

    # ---- mí nhắm: phủ xanh lên tròng mắt (bao lồi vùng vàng), thêm một nét khép cong
    # vùng vàng của một mắt có thể bị con ngươi chia thành vài mảnh: gom các mảnh gần nhau (nới 22 px) thành từng mắt
    n, lab, st, _ = cv2.connectedComponentsWithStats(_gian(yellow, 22).astype(np.uint8), connectivity=8)
    cs = sorted(range(1, n), key=lambda i: -int((yellow & (lab == i)).sum()))[:2]
    cs.sort(key=lambda i: st[i, cv2.CC_STAT_LEFT])                      # trái = mắt gần
    for ten, i in zip(("mi_g", "mi_x"), cs):
        vang_mat = yellow & (lab == i)
        ys, xs = np.nonzero(vang_mat)
        hull = cv2.convexHull(np.stack([xs, ys], 1).astype(np.int32))
        Hm = np.zeros((H, W), np.uint8)
        cv2.fillConvexPoly(Hm, hull, 1)
        # lòng mắt = mọi thứ không phải da xanh (tròng vàng, con ngươi, chấm sáng) nằm cách da xanh hơn một bề dày nét mực (nét mực
        # quanh mắt và gờ mày đều sát da xanh nên bị loại), liền với vùng vàng của mắt này. Con ngươi to lệch khỏi vùng vàng vẫn dính.
        net_w = int(round(NET_DAY))
        ngoai = _gian(~pm["fg"], net_w + 1)                               # nét viền ngoài cùng của con (sát nền giấy): không phủ
        Z = pm["fg"] & ~xanh_than & ~cream & ~red & ~_gian(xanh_than, net_w - 1) & ~ngoai
        nz, labz = cv2.connectedComponents(Z.astype(np.uint8), connectivity=8)
        ids = np.unique(labz[vang_mat & Z])
        E = np.isin(labz, ids[ids != 0]) & _gian(Hm > 0, 80)
        E = _lap_lo(E | vang_mat)
        E = _lap_lo(cv2.morphologyEx(E.astype(np.uint8), cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))) > 0)
        E |= (a.min(2) > 200) & _gian(E, 6) & pm["fg"]                    # chấm sáng trong con ngươi
        E = (E & ~_gian(xanh_than, net_w - 2) & ~ngoai) | (vang_mat & ~_gian(~pm["fg"], 2))
        E |= (a.min(2) > 185) & _gian(E, 9) & pm["fg"] & ~ngoai            # phần chấm sáng nằm sát gờ mày (sáng thì không thể là nét mực)
        Xm = van_xanh.copy()
        ey, ex = np.nonzero(E)
        x0, x1 = int(ex.min()), int(ex.max())
        cols = np.arange(x0 + (x1 - x0) // 5, x1 - (x1 - x0) // 5)
        doc = float(np.polyfit(cols, [np.nonzero(E[:, x])[0].min() for x in cols], 1)[0])          # độ dốc mép trên (gờ mày)
        xm, ym, hm = float(ex.mean()), float(ey.mean()), float(ey.max() - ey.min())
        pts = []
        for fx, vong in ((0.13, 0.0), (0.5, -0.05), (0.9, 0.0)):                                   # nét khép: thẳng, song song gờ mày, hơi vồng lên
            x = x0 + fx * (x1 - x0)
            pts.append((x, ym + 0.10 * hm + 0.75 * doc * (x - xm) + vong * hm))
        nmk = _net((H, W), pts, day=9) * E
        Xm = Xm * (1 - nmk[..., None]) + muc * nmk[..., None]
        al_m = cv2.GaussianBlur(E.astype(np.float32), (0, 0), 0.8)
        box = _hop(al_m > 0.02)
        _luu(Xm, al_m, box, os.path.join(ra, ten + ".png"))
        info["manh"][ten] = box


# ================================================================ RIG (thư viện quai) ================================================================
# Cấu trúc học từ con gốc monster_3230 (ghi chú inbox/ech_xanh_ghichu.md mục 2), đổi cho hợp cách cắt của mình:
#   root -> move (game dời: cú lao) -> lat (lật ngửa lúc chết, rơi lúc xuất hiện) -> than (tâm thân: nhún, dời, nén giãn)
#        -> day (đáy thân phía sau: nghiêng cả khối) -> dau (NẮP ĐẦU: cả phần xanh phía trên xoay quanh bản lề phía sau = há miệng)
#                                                          -> ham (môi dưới, con của dau: đầu gật thì miệng vẫn khép; há = xoay ngược)
#                                                          -> moi (môi trên phía trước) -> l0..l4 (lưỡi ngắn)
#                                                    -> bung (bụng: phình) -> u1..u3 (cục phồng chạy dọc mặt trước bụng)
#                                                    -> d0..d7 (lưỡi dài, gốc trong miệng), mieng_goc -> mieng (chỗ và hướng nhả cho VFX)
#                                                    -> dui (đùi gần), vai (vai gần), chan_x (chân sau bên kia, ẩn lúc nghỉ)
#        move -> ban (bàn chân gần), ban_tay (bàn tay gần), tay_x (bàn tay xa): bám đất; chân, tay là lưới giãn giữa thân và đất
# Lớp (sau -> trước): chan_x, tay_x, hong (lòng miệng: mép trên theo dau, mép dưới theo ham, giãn ra khi há), bung, luoi_dai,
# luoi, than (xanh: đầu + lưng + hai mắt), mi_x, mi_g, chan, tay.
SC = 0.5                      # pixel concept -> pixel rig
CAO_HIEU = {1: 1.25, 2: 1.0}  # game co tướng theo game.height: dạng 1 khai cao hơn thật để vẽ nhỏ hơn dạng 2
CHAM = {1: 1.0, 2: 1.12}      # dạng 2 nặng hơn: mọi clip chậm lại chừng này
NL, ND = 5, 8                 # số đốt lưỡi ngắn, lưỡi dài
NHE = (0.6, 1.8)              # bản nhẹ của dạng sau gộp vào rig dạng trước (clip evolve): ảnh nhỏ còn 0,6, lưới thưa 1,8 lần

RIG = {
    1: dict(
        tam_x=730, dat=906,
        lat=(400, 900), than=(720, 650), day=(440, 830), ban_le=(470, 660), moi=(955, 458), bung=(880, 700),
        # ba vùng phồng theo ba chỗ người dùng khoanh (2026-11-11): đáy bụng sau bàn tay gần -> giữa bụng -> góc trên phải dưới miệng
        u=[(735, 825), (915, 735), (1077, 605)], u_r=[150, 190, 125], u_goc=[-90, -20, 20],
        mieng=(1060, 480), goc_luoi_dai=(445, 532), huong=8,
        dui=(450, 715), ban=(420, 885), y_chan=(770, 850),
        vai=(585, 630), ban_tay=(672, 878), y_tay=(650, 835),
        tay_x=(1045, 880), chan_x=(215, -10),
        vung_day=[(280, 655), (500, 655), (545, 560), (640, 560), (640, 890), (280, 890)], hoa=26,
        moi_loc=(570, 600),   # điểm nét môi: lấy x lớn hơn, y nhỏ hơn mức này (bỏ điểm đo nhầm ở dải hông)
    ),
    2: dict(
        ti=1.45,              # con to hơn dạng 1 chừng này trên concept: các khoảng hoà (px concept) nhân theo
        tam_x=700, dat=972,
        lat=(250, 965), than=(700, 560), day=(290, 890), ban_le=(270, 575), moi=(1000, 345), bung=(900, 650),
        u=[(640, 895), (900, 720), (1165, 525)], u_r=[215, 270, 180], u_goc=[-90, -20, 20],
        mieng=(1190, 360), goc_luoi_dai=(230, 400), huong=8,
        dui=(290, 690), ban=(280, 945), y_chan=(830, 925),
        vai=(550, 640), ban_tay=(650, 945), y_tay=(650, 890),
        tay_x=(1185, 935), chan_x=(310, -12),
        vung_day=[(60, 580), (340, 580), (390, 425), (560, 395), (770, 620), (770, 990), (60, 990)], hoa=30,
        moi_loc=(420, 480),
    ),
}


def _quai():
    sys.path.insert(0, HERE)
    from quai import anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat
    return anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat


def ln(f, keys):
    """nội suy thẳng theo khung (như phần lớn khoá của con gốc)."""
    return float(np.interp(f, [q[0] for q in keys], [q[1] for q in keys]))


def spl(f, keys, chu_ky=None):
    """đường cong trơn qua các khoá (Hermite, tiếp tuyến trung bình hai bên); chu_ky: khép vòng."""
    xs, vs = [float(q[0]) for q in keys], [float(q[1]) for q in keys]
    if chu_ky:
        f = f % chu_ky
        xs = [xs[-1] - chu_ky] + xs + [xs[0] + chu_ky, xs[1] + chu_ky]
        vs = [vs[-1]] + vs + [vs[0], vs[1]]
    else:
        f = min(max(f, xs[0]), xs[-1])
        xs = [xs[0] - 1] + xs + [xs[-1] + 1]
        vs = [vs[0]] + vs + [vs[-1]]
    i = 1
    while i < len(xs) - 3 and f > xs[i + 1]:
        i += 1

    def m(j):
        return 0.5 * ((vs[j + 1] - vs[j]) / (xs[j + 1] - xs[j]) + (vs[j] - vs[j - 1]) / (xs[j] - xs[j - 1]))

    h = xs[i + 1] - xs[i]
    u = (f - xs[i]) / h
    return ((2 * u ** 3 - 3 * u ** 2 + 1) * vs[i] + (u ** 3 - 2 * u ** 2 + u) * h * m(i) + (-2 * u ** 3 + 3 * u ** 2) * vs[i + 1]
            + (u ** 3 - u ** 2) * h * m(i + 1))


def _ss(u):
    u = min(1.0, max(0.0, u))
    return u * u * (3 - 2 * u)


def dung(k, sc=SC, tho=1.0):
    """dựng rig dạng k: trả (sk, info). sc: pixel concept -> pixel rig; tho: lưới thưa đi chừng này lần (bản nhẹ của dạng sau
    để gộp vào rig dạng trước cho clip tiến hóa)."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    Dat = khung.Dat
    g = RIG[k]
    dm = os.path.join(d_inbox(k), "manh")
    mj = json.load(open(os.path.join(dm, "manh.json"), encoding="utf-8"))
    ox, oy = g["tam_x"], g["dat"]
    B = mj["manh"]

    def R(p):
        return ((p[0] - ox) * sc, (oy - p[1]) * sc)

    def tam(ten, dx=0, dy=0):
        b = B[ten]
        return R(((b[0] + b[2]) / 2 + dx, (b[1] + b[3]) / 2 + dy))

    def nap(ten, ti=None):
        ti = sc if ti is None else ti
        im = Image.open(os.path.join(dm, ten + ".png")).convert("RGBA")
        im = im.resize((max(2, round(im.width * ti)), max(2, round(im.height * ti))), Image.LANCZOS)
        return anh.loang_mau(im)

    def cc(ten, L):
        """toạ độ concept của các đỉnh lưới mảnh `ten`."""
        im = sk.images[ten]
        b = B[ten]
        return np.stack([b[0] + L.pts[:, 0] * (b[2] - b[0]) / im.width, b[1] + L.pts[:, 1] * (b[3] - b[1]) / im.height], 1)

    def ic(ten, pts):
        """toạ độ concept -> pixel ảnh mảnh."""
        im = sk.images[ten]
        b = B[ten]
        return [((x - b[0]) * im.width / (b[2] - b[0]), (y - b[1]) * im.height / (b[3] - b[1])) for x, y in pts]

    sk = khung.Sk(f"{CODE}_{k}")
    for ten in ("than", "bung", "luoi", "chan", "tay", "tay_x", "mi_g", "mi_x", "luoi_dai"):
        sk.anh(ten, nap(ten))
    sk.anh("hong", nap("hong", sc * 0.5))

    H = (oy - B["than"][1]) * sc                                         # chiều cao con (px rig)
    Wb = (B["bung"][2] - B["chan"][0]) * sc

    sk.xuong("root")
    sk.xuong("move", "root")
    sk.xuong("lat", "move", *R(g["lat"]), the_gioi=True)
    sk.xuong("than", "lat", *R(g["than"]), the_gioi=True)
    sk.xuong("day", "than", *R(g["day"]), the_gioi=True)
    sk.xuong("dau", "day", *R(g["ban_le"]), the_gioi=True)
    sk.xuong("ham", "dau", *R(g["ban_le"]), the_gioi=True)
    sk.xuong("moi", "dau", *R(g["moi"]), the_gioi=True)
    sk.xuong("bung", "day", *R(g["bung"]), the_gioi=True)
    for i, pu in enumerate(g["u"]):
        sk.xuong(f"u{i + 1}", "bung", *R(pu), the_gioi=True)
    sk.xuong("mieng_goc", "day", *R(g["ban_le"]), the_gioi=True)
    sk.xuong("mieng", "mieng_goc", *R(g["mieng"]), goc=g["huong"], dai=40, the_gioi=True)
    sk.xuong("dui", "day", *R(g["dui"]), the_gioi=True)
    sk.xuong("vai", "day", *R(g["vai"]), the_gioi=True)
    sk.xuong("chan_x", "day", *tam("chan", *g["chan_x"]), the_gioi=True)
    sk.xuong("ban", "move", *R(g["ban"]), the_gioi=True)
    sk.xuong("ban_tay", "move", *R(g["ban_tay"]), the_gioi=True)
    sk.xuong("tay_x", "move", *R(g["tay_x"]), the_gioi=True)

    # lưỡi ngắn: dải dọc, gốc ở trên (khuất dưới môi trên)
    im = sk.images["luoi"]
    Ll = luoi.luoi_dai(im, NL, truc=[(im.width / 2, 0), (im.width / 2, im.height)], mu="ngon", buoc_theo_cao=H * tho, ten=f"luoi {k}")
    dat_l = Dat(*tam("luoi"))
    l = sk.chuoi("l", "moi", dat_l.ra(Ll.khop(NL), im.width, im.height))
    # lưỡi dài: ảnh nằm ngang, gốc bên trái (trong miệng), chĩa về phía đối thủ
    imd = sk.images["luoi_dai"]
    Ld = luoi.luoi_dai(imd, ND, mu="ngon", buoc_theo_cao=H * tho, ten=f"luoi_dai {k}")
    dat_d = Dat(*R(g["goc_luoi_dai"]), goc=g["huong"], neo=(0.0, 0.5))
    d = sk.chuoi("d", "day", dat_d.ra(Ld.khop(ND), imd.width, imd.height))

    sk.slot("chan_x", "chan_x", "chan_x", an=True)
    sk.slot("tay_x", "tay_x", "tay_x")
    sk.slot("hong", "dau", "hong")
    sk.slot("luoi_dai", d[0], "luoi_dai", an=True)                       # lưỡi bắn: trước vòm họng, SAU hàm dưới (ló ra từ sau môi dưới)
    sk.slot("bung", "day", "bung")
    sk.slot("luoi_ru", d[0], "luoi_dai", an=True)                        # cùng ảnh, cùng xương, nhưng TRƯỚC bụng: lưỡi thè rũ lúc chết
    sk.slot("luoi", l[0], "luoi")
    sk.slot("than", "dau", "than")
    sk.slot("mi_x", "dau", "mi_x", an=True)
    sk.slot("mi_g", "dau", "mi_g", an=True)
    sk.slot("chan", "dui", "chan")
    sk.slot("tay", "vai", "tay")

    sk.luoi_gan("luoi", "luoi", Ll, trongso.chuoi(Ll.s, Ll.truc[1][-1] / NL, l), dat=dat_l)
    Wld = trongso.chuoi(Ld.s, Ld.truc[1][-1] / ND, d)
    sk.luoi_gan("luoi_dai", "luoi_dai", Ld, Wld, dat=dat_d)
    sk.luoi_gan("luoi_ru", "luoi_dai", Ld, Wld, dat=dat_d)

    # thân xanh: nắp đầu (dau) + dải hông, đáy lưng (day); ranh hoà rộng quanh bản lề
    im = sk.images["than"]
    Lt = luoi.luoi_vung(im, buoc_theo_cao=H * tho, ten=f"than {k}")
    Wt = trongso.vung(Lt, [("day", ic("than", g["vung_day"])), ("dau", [(0, 0), (im.width, 0), (im.width, im.height), (0, im.height)])],
                      dai_hoa=g["hoa"])
    sk.luoi_gan("than", "than", Lt, trongso.lam_tron(Lt, Wt), dat=Dat(*tam("than")))

    # bụng kem: dải sát môi theo ham; mép sau theo day; còn lại theo bung, pha các cục phồng u1..u3 ở mặt trước
    TI = g.get("ti", 1.0)
    moi = np.array([q for q in mj["moi"] if q[1] < g["moi_loc"][1] and q[0] > g["moi_loc"][0]], float)
    im = sk.images["bung"]
    Lb = luoi.luoi_vung(im, buoc_theo_cao=H * tho, ten=f"bung {k}")
    Cb = cc("bung", Lb)
    x_sau = g["ban_le"][0] + 60 * TI
    Wg = []
    for x, y in Cb:
        dl = float(np.min(np.hypot(moi[:, 0] - x, moi[:, 1] - y)))
        wh = _ss(1 - (dl - 10 * TI) / (230.0 * TI))
        wd = _ss((x_sau + 110 * TI - x) / (110.0 * TI)) * (1 - wh)
        con = max(0.0, 1 - wh - wd)
        giu_moi = _ss((dl - 6 * TI) / (48.0 * TI))                                    # sát môi không theo cục phồng (kẻo hở nét môi với nắp đầu)
        wu = [0.88 * giu_moi * math.exp(-((x - px) ** 2 + (y - py) ** 2) / ur ** 2) for (px, py), ur in zip(g["u"], g["u_r"])]
        su = min(0.9, sum(wu))
        wu = [w * su / max(1e-9, sum(wu)) for w in wu]
        dct = {"ham": wh * (1 - su), "day": wd * (1 - su), "bung": con * (1 - su)}
        for i, w in enumerate(wu):
            dct[f"u{i + 1}"] = w
        Wg.append({q: w for q, w in dct.items() if w > 0.004})
    sk.luoi_gan("bung", "bung", Lb, trongso.chuan(Wg, toi_da=4), dat=Dat(*tam("bung")))

    # lòng miệng: lưới ô, hàng trên bám dau (nằm trong mép môi trên), hàng dưới bám ham (trong mép môi dưới): lúc khép dẹt lại, khuất
    imh = sk.images["hong"]
    cot, hang = 10, 5
    Lh = luoi.luoi_o(imh.width, imh.height, cot, hang, ten=f"hong {k}")
    ss = np.concatenate([[0], np.cumsum(np.hypot(*np.diff(moi, axis=0).T))])
    V, Wh = [], []
    for r in range(hang):
        v = r / (hang - 1)
        for c_ in range(cot):
            u = c_ / (cot - 1) * 0.985
            px, py = np.interp(u * ss[-1], ss, moi[:, 0]), np.interp(u * ss[-1], ss, moi[:, 1])
            V.append(R((px, py - 9 * TI + 18 * TI * v)))
            Wh.append({"dau": 1 - v, "ham": v} if 0 < v < 1 else ({"ham": 1.0} if v >= 1 else {"dau": 1.0}))
    sk.luoi_gan("hong", "hong", Lh, Wh, the_gioi=np.array(V))

    # đùi + bàn chân gần: trên theo dui, bàn chân theo ban (bám đất), giãn ở giữa
    im = sk.images["chan"]
    Lc = luoi.luoi_vung(im, buoc_theo_cao=H * tho, ten=f"chan {k}")
    y0, y1 = g["y_chan"]
    Wc = []
    for x, y in cc("chan", Lc):
        t = _ss((y - y0) / (y1 - y0))
        Wc.append({q: w for q, w in (("dui", 1 - t), ("ban", t)) if w > 0.004})
    sk.luoi_gan("chan", "chan", Lc, Wc, dat=Dat(*tam("chan")))
    sk.manh("chan_x", "chan", Dat(*tam("chan", *g["chan_x"])), ten="chan_x")

    # tay gần: vai theo vai, bàn tay theo ban_tay (bám đất)
    im = sk.images["tay"]
    La = luoi.luoi_vung(im, buoc_theo_cao=H * tho, ten=f"tay {k}")
    y0, y1 = g["y_tay"]
    Wa = []
    for x, y in cc("tay", La):
        t = _ss((y - y0) / (y1 - y0))
        Wa.append({q: w for q, w in (("vai", 1 - t), ("ban_tay", t)) if w > 0.004})
    sk.luoi_gan("tay", "tay", La, Wa, dat=Dat(*tam("tay")))
    im = sk.images["tay_x"]
    Lx = luoi.luoi_vung(im, buoc_theo_cao=H * tho, ten=f"tay_x {k}")
    y0 = B["tay_x"][1] + 20
    y1 = y0 + CAT[k]["co_tay_x"]
    Wx = []
    for x, y in cc("tay_x", Lx):
        t = _ss((y - y0) / (y1 - y0))
        Wx.append({q: w for q, w in (("day", 1 - t), ("tay_x", t)) if w > 0.004})
    sk.luoi_gan("tay_x", "tay_x", Lx, Wx, dat=Dat(*tam("tay_x")))
    sk.manh("mi_g", "mi_g", Dat(*tam("mi_g")))
    sk.manh("mi_x", "mi_x", Dat(*tam("mi_x")))

    for ev, mo in (("trung", "đầu lưỡi chạm đối thủ"), ("phun", "bắt đầu nhả nước (VFX bám xương mieng)"), ("het_phun", "hết nhả"),
                   ("nha", "chiêu cuối: ợ quả cầu nước ra khỏi miệng (VFX bám xương mieng)")):
        sk.su_kien(ev, mo)
    rb = (B["bung"][2] - g["bung"][0]) * sc
    db = (B["bung"][3] - g["bung"][1]) * sc
    info = {"k": k, "H": H, "Wb": Wb, "l": l, "d": d, "rb": rb, "db": db, "u_goc": list(g["u_goc"]), "du": [0.0, 0.4 * (B["bung"][3] - g["u"][1][1]) * sc, 0.0], "dai_d": float(Ld.truc[1][-1]), "cao_than": R(g["than"])[1],
            "dinh": {"than": Lt.n, "bung": Lb.n, "chan": Lc.n, "tay": La.n, "luoi": Ll.n, "luoi_dai": Ld.n}}
    return sk, info


def clips(sk, info, k):
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    Clip, LoXo, rung = hoat.Clip, hoat.LoXo, hoat.rung
    H, Wb, l, d = info["H"], info["Wb"], info["l"], info["d"]
    KX, KY = Wb / 240.0, H / 215.0                                           # đổi độ dời của khoá con gốc sang cỡ thân mình
    PX = H / 376.5                                                            # các độ dời ghi bằng px rig của dạng 1: nhân theo cỡ con
    ch = CHAM[k]
    F = 30.0 / ch                                                             # khung (của bản thiết kế) mỗi giây
    slots = [s_["name"] for s_ in sk.slots]
    BAM = ("ban", "ban_tay", "tay_x")                                         # xương bám đất (con của move)
    inv0 = np.linalg.inv(sk.W0["day"])
    g_d0 = sk.goc_tg(d[0])[2]

    def ha(P, gat, a=0.0, b=0.0):
        """đầu gật `gat` độ (âm = cúi; miệng vẫn khép vì ham là con của dau), há miệng: nắp đầu ngửa thêm a độ, môi dưới trễ b độ."""
        P.rot("dau", gat + a)
        P.rot("ham", -(a + b))
        P.rot("mieng_goc", gat + (a - b) / 2)

    def no(P, v):
        """cả người nở theo bụng (v = 0..1): thân to ra chút, đáy không lún xuống đất."""
        P.scale("than", 1 + 0.07 * v, 1 + 0.09 * v)
        P.move("than", 0, 0.09 * v * info["cao_than"])

    UG = info["u_goc"]
    LUC = ((0.62, 0.055), (0.42, 0.060), (0.52, 0.140))                       # mỗi vùng phồng: nở thêm bao nhiêu, lồi ra bao nhiêu (theo H) khi a = 1

    def phong(P, i, a):
        """vùng phồng i (0 bụng dưới, 1 giữa, 2 túi họng ngay dưới môi) nở a (1 = hết cỡ, âm = hóp): vừa to ra vừa lồi theo hướng của
        nó; đáy không lún xuống đất. Dải sát môi không thuộc vùng nào nên nét môi không lệch khỏi nắp đầu."""
        if abs(a) < 0.002:
            return
        rg = math.radians(UG[i])
        P.scale(f"u{i + 1}", 1 + LUC[i][0] * a, 1 + LUC[i][0] * a)
        P.move(f"u{i + 1}", LUC[i][1] * H * a * math.cos(rg), LUC[i][1] * H * a * math.sin(rg) + 0.85 * LUC[i][0] * a * info["du"][i])

    def phinh(P, sx, sy=None):
        """bụng phình kiểu thở / nảy (sx quanh 1): nở ở bụng dưới và giữa. KHÔNG co giãn xương bung: nó kéo cả góc trên bụng lòi ra
        khỏi chóp môi (lỗi người dùng thấy ở idle)."""
        a = (sx - 1) / 0.42
        phong(P, 1, 0.9 * a)

    def luoi_ngan(P, dai=1.0, truot=0.0, hien=1.0):
        """lưỡi ngắn: dài theo tỉ lệ (rụt vào miệng), trượt lên / xuống dọc lưỡi (dương = thò ra), độ đậm."""
        if dai != 1.0:
            P.scale(l[0], dai, 1.0)
        if truot:
            P.move(l[0], 0, -truot * PX)
        if hien < 1:
            P.alpha["luoi"] = hien

    def nuot(P, f, f0):
        """rụt lưỡi ngắn vào miệng bắt đầu ở khung f0 (6 khung), rồi ẩn."""
        luoi_ngan(P, dai=ln(f, [(f0, 1), (f0 + 1, 1.04), (f0 + 2, 0.8), (f0 + 4, 0.36), (f0 + 5, 0.2)]),
                  truot=-ln(f, [(f0, 0), (f0 + 1, -1.5), (f0 + 5, 9)]), hien=1.0 if f < f0 + 5 else 0.0)
        if f0 + 1 <= f < f0 + 5:
            for i, b_ in enumerate(l[1:]):
                P.rot(b_, (-7 if i % 2 else 9) * ln(f, [(f0 + 1, 0), (f0 + 3, 1), (f0 + 5, 0.4)]))

    def tha(P, f, f0):
        """thả lưỡi ngắn ra lại bắt đầu ở khung f0: bung ra quá đà rồi về (8 khung)."""
        if f < f0:
            P.alpha["luoi"] = 0.0
            return
        luoi_ngan(P, dai=ln(f, [(f0, 0.25), (f0 + 3, 1.13), (f0 + 5, 0.95), (f0 + 8, 1)]), truot=ln(f, [(f0, -8), (f0 + 3, 3), (f0 + 8, 0)]))
        for i, b_ in enumerate(l[1:]):
            P.rot(b_, (8 if i % 2 else -6) * ln(f, [(f0, 1), (f0 + 3, -0.6), (f0 + 6, 0.25), (f0 + 9, 0)]))

    def nham(P):
        P.alpha["mi_g"] = 1.0
        P.alpha["mi_x"] = 1.0

    def an_het(P, a):
        for s_ in slots:
            if s_ not in ("chan_x", "luoi_dai", "luoi_ru", "mi_g", "mi_x") or P.alpha.get(s_, 0) > 0:
                P.alpha[s_] = a * P.alpha.get(s_, 1.0)

    def theo(P, he=1.0):
        """chân, tay bám đất đi theo thân `he` phần (0 = đứng nguyên dưới đất, 1 = dính theo thân): lúc rơi, lúc lật ngửa."""
        if he <= 0:
            return
        W = sk.the_gioi(P)
        M = W["day"] @ inv0
        ang = math.degrees(math.atan2(M[1, 0], M[0, 0]))
        Wm = np.linalg.inv(W["move"])
        for b_ in BAM:
            p0 = sk.W0[b_][:, 2]
            lt = Wm @ (M @ p0)
            bb = sk.bones[sk.bi[b_]]
            P.move(b_, he * (lt[0] - bb["x"]), he * (lt[1] - bb["y"]))
            P.rot(b_, he * ang)

    def vung(P, xuong, tam, goc):
        """vung xương bám đất `xuong` quanh khớp `tam` (hông, vai) `goc` độ: chân, tay giơ lên chứ không chỉ xoay tại chỗ."""
        W = sk.the_gioi(P)
        pv_, q = W[tam][:2, 2], W[xuong][:2, 2]
        r = math.radians(goc)
        v = q - pv_
        dw = np.array([math.cos(r) * v[0] - math.sin(r) * v[1], math.sin(r) * v[0] + math.cos(r) * v[1]]) - v
        dl = np.linalg.solve(W["move"][:2, :2], dw)
        P.move(xuong, float(dl[0]), float(dl[1]))
        P.rot(xuong, goc)

    S_L = {  # dáng lưỡi dài (góc từng đốt sau đốt gốc), theo khung của đòn đánh
        "cuon": [-6, -14, -22, -28, -28, -24, -18], "quat": [3, 8, 9, -4, -14, -18, -12], "thang": [0, -1, 0, 1, 1, 2, 2],
        "nang": [0, -1, -3, -5, -8, -10, -11], "nay": [0, 1, 2, 3, 5, 6, 6], "rut": [4, 10, 14, 10, -8, -18, -22]}

    def luoi_dai(P, dai, goc=0.0, dang=None, hien=1.0):
        P.alpha["luoi_dai"] = hien
        P.scale(d[0], dai, 1.0)
        P.rot(d[0], goc)
        for b_, a in zip(d[1:], dang or []):
            P.rot(b_, a)

    def tron_dang(f, keys):
        """trộn các dáng lưỡi theo khung: keys = [(khung, tên dáng)...]."""
        fs = [q[0] for q in keys]
        return [float(np.interp(f, fs, [S_L[q[1]][i] for q in keys])) for i in range(ND - 1)]

    def mem(cung=1.0):
        return [LoXo(l, k=[300 * cung, 230 * cung, 180 * cung, 150 * cung, 125 * cung], damp=0.42, maxang=16)]

    # ---------------- idle: 2 vòng idle_01 của con gốc (40 khung mỗi vòng): nhún 2 lần, bụng hít một hơi - giữ - xả - nghỉ;
    # lưỡi đung đưa chậm trễ pha từ gốc ra ngọn, thò ra thụt vào nhẹ; vòng hai chớp mắt
    def idle_fn(t, P):
        fa = t * F
        f = fa % 40
        s20 = math.sin(2 * math.pi * f / 20.0)
        P.move("than", 0, 0.62 * KY * 9.68 * (0.5 - 0.5 * math.cos(2 * math.pi * f / 20.0)))
        P.rot("day", 1.6 * s20)
        P.rot("dau", -2.0 * s20)
        P.rot("dui", -1.6 * s20 * 0.5)
        b = spl(f, [(0, 1), (6, 1.13), (10, 1.15), (15, 1.14), (21, 1.0), (30, 1.0)], 40)
        phinh(P, b, 1 + (b - 1) * 0.8)
        P.move("moi", 0.9 * PX * (b - 1) / 0.15, 0.6 * PX * (b - 1) / 0.15)
        # lưỡi: con lắc nặng, chu kỳ 40 khung, gốc dẫn ngọn theo, biên độ lớn dần ra ngọn; thò thụt chu kỳ 80 khung
        for i, b_ in enumerate(l):
            P.rot(b_, (1.2 + 0.9 * i) * (math.sin(2 * math.pi * (fa - 3.2 * i) / 40.0) - math.sin(2 * math.pi * (-3.2 * i) / 40.0)))
        luoi_ngan(P, truot=3.2 * (1 - math.cos(2 * math.pi * fa / 80.0)) - 1.6 * (1 - math.cos(2 * math.pi * fa / 40.0)))
        if 52 <= fa < 55.5:
            nham(P)

    # ---------------- appear: rơi từ trên xuống, bẹp, nảy; chạm đất xong lưỡi bung ra
    def appear_fn(t, P):
        f = t * F
        roi = 2.6 * H * (1 - min(1.0, f / 7.0) ** 2)
        P.move("lat", 0, roi)
        P.scale("than", ln(f, [(0, .88), (7, .86), (8.5, 1.2), (10, 1.16), (12.5, .94), (15, 1.04), (18, .98), (21, 1)]),
                ln(f, [(0, 1.14), (7, 1.17), (8.5, .76), (10, .8), (12.5, 1.08), (15, .96), (18, 1.02), (21, 1)]))
        P.move("than", 0, KY * ln(f, [(0, 0), (8.5, -24), (10, -20), (12.5, 16), (15, -5), (18, 2), (21, 0)]))
        P.rot("dau", ln(f, [(0, 5), (7, 7), (8.5, -9), (11, 3), (14, -2), (18, 0)]))
        theo(P, ln(f, [(0, 1), (6.5, 1), (7.5, 0)]))
        for b_ in ("dui", "vai"):
            P.rot(b_, ln(f, [(0, -14), (7, -18), (8.5, 6), (12, 0)]))
        b = ln(f, [(0, 1), (8.5, 1), (10, 1.14), (13, .96), (16, 1.03), (20, 1)])
        phinh(P, b)
        tha(P, f, 11)
        if f < 12.5:
            nham(P)
        if f < 2:
            an_het(P, ln(f, [(0, 0), (2, 1)]))

    # ---------------- attack: há miệng bắn lưỡi dài (skill_01 của con gốc): ngồi thụt, nuốt lưỡi, phình bụng; bung trong 1 khung;
    # lưỡi tới hết tầm ở khung 14 (trúng), đầu lưỡi nặng chúi xuống rồi nảy; rút trong 2 khung; nuốt, thả lưỡi ra lại
    def attack_fn(t, P):
        f = t * F
        P.rot("day", ln(f, [(0, 0), (4, 2.2), (9, 0), (11, 13), (12, 6), (14, 5.4), (19, 4.5), (25, -1.2), (27, 0), (31, -1), (35, 0)]))
        P.move("than", 0.5 * KX * ln(f, [(0, 0), (4, -26.9), (9, -26.9), (11, -12.4), (12, 40.7), (14, 34), (19, 25), (25, 20.6), (26, -12.5), (27, -12.4),
                                         (31, -1.4), (35, 0)]),
               0.5 * KY * ln(f, [(0, 0), (4, 1.9), (9, 1.9), (11, -9), (12, 36.1), (14, 22.5), (19, 22.5), (25, 17.4), (26, 7.3), (27, 5), (31, 14), (35, 0)]))
        P.scale("than", ln(f, [(0, 1), (4, 1.05), (9, 1.06), (11, 1.1), (12, .93), (14, .97), (25, 1), (27, 1.07), (31, .98), (35, 1)]),
                ln(f, [(0, 1), (4, .95), (9, .94), (11, .88), (12, 1.09), (14, 1.03), (25, 1), (27, .93), (31, 1.02), (35, 1)]))
        P.move("move", 0.36 * H * ln(f, [(0, 0), (11, 0), (12, .82), (14, 1), (25, 1), (27, .1), (30, 0)]), 0)
        gat = ln(f, [(0, 0), (2, -1), (5, -9), (9, -12), (11, -6), (12, 0), (25, 0), (27, -8), (31, -4), (35, 0)])
        a = ln(f, [(0, 0), (11, 0), (12, 25), (14, 31), (19, 27), (25, 28), (27, 0)])
        mo = ln(f, [(0, 0), (11, 0), (12, 1), (25, 1), (27, 0)])
        ha(P, gat, a, 10 * mo)
        b = ln(f, [(0, 1), (4, 1.02), (9, 1.14), (12, .97), (25, 1), (27, 1.15), (31, .99), (35, 1)])
        phinh(P, b)
        if f < 11:
            nuot(P, f, 0)
        elif f < 27.5:
            P.alpha["luoi"] = 0.0
            dai = ln(f, [(11, .3), (12, .84), (13, 1.24), (14, 1.42), (16, 1.33), (19, 1.3), (25, 1.2), (26, .66), (27.5, .28)])
            goc = ln(f, [(11, -10), (12, 4), (14, -2), (16, 1.5), (19, 0), (25, 0), (26, 5), (27.5, -6)])
            dang = tron_dang(f, [(11, "cuon"), (12, "quat"), (13.5, "thang"), (15.5, "nang"), (17.5, "nay"), (20, "nang"), (22.5, "thang"), (25, "thang"),
                                 (26, "rut"), (27.5, "cuon")])
            luoi_dai(P, dai, goc, dang)
        tha(P, f, 28) if f >= 11 else None
        if 11.5 <= f < 13.5 or 26 <= f < 29:
            nham(P)

    # ---------------- cast: chỉ há miệng cho nước bắn ra (skill_03 của con gốc): lấy đà, há và chồm tới, GIỮ HÁ có rung suốt lúc tia
    # nước chảy, ngậm, nảy về. Clip có sự kiện `het_phun` nên sân KHÔNG ghìm giờ clip ở khung nhả (AolaActor.SelfHold): clip phải tự
    # giữ há đủ lâu. Tia nước n_tia của chiêu mana chảy 0,93 s (HatNuoc.HoldNuoc) -> giữ há từ khung 9,5 tới 37,5 (0,93 s ở dạng 1).
    def cast_fn(t, P):
        f = t * F
        r = rung(t, 9.5 / F, 37 / F)
        P.rot("day", ln(f, [(0, 0), (2, 2.4), (6, 0), (8, 12), (9, 5), (14, 4), (22, 3), (30, 3.6), (37, 3.5), (41, -3.5), (49, -0.8), (53, 0)]))
        P.move("than", 0.42 * KX * ln(f, [(0, 0), (2, -45.3), (6, -38.7), (8, -12.4), (9, 72.7), (14, 52.4), (24, 44), (37, 38), (41, -20), (49, -1), (53, 0)]),
               0.42 * KY * ln(f, [(0, 0), (2, 1.9), (6, 1.9), (8, -9), (9, 31.7), (14, 35.7), (24, 38), (37, 30), (41, 12), (49, 8), (53, 0)]))
        P.scale("than", ln(f, [(0, 1), (2, 1.05), (6, 1.06), (8, 1.1), (9, .94), (14, .97), (37, .98), (41, 1.07), (45, .98), (49, 1.01), (53, 1)]),
                ln(f, [(0, 1), (2, .95), (6, .94), (8, .88), (9, 1.08), (14, 1.03), (37, 1.02), (41, .93), (45, 1.02), (49, .99), (53, 1)]))
        gat = ln(f, [(0, 0), (2, -2), (5, -11), (6, -13), (8, -4), (9, 0), (37, 0), (41, -7), (44, 1.5), (49, 0), (53, 0)])
        a = ln(f, [(0, 0), (8, 0), (9, 27), (14, 31), (24, 29), (37, 28), (41, 0)]) + 0.9 * r
        mo = ln(f, [(0, 0), (8, 0), (9, 1), (37, 1), (41, 0)])
        ha(P, gat, a, 10 * mo)
        b = ln(f, [(0, 1), (2, 1.02), (6, 1.16), (9, .98), (37, .9), (41, 1.13), (45, .98), (49, 1.02), (53, 1)]) * (1 + 0.012 * r)   # bụng xẹp dần lúc phun
        phinh(P, b)
        if f < 8:
            nuot(P, f, 0)
        tha(P, f, 43) if f >= 8 else None
        if 41 <= f < 44:
            nham(P)

    # ---------------- skill: phình bụng rồi ợ ra quả cầu nước (ý người dùng 2026-11-11: bụng phình, rồi chuyển phần phình đấy TỪ TỪ
    # lên phần miệng, rồi mở mồm; không vẽ nét hằn). Ba vùng phồng: u1 bụng dưới, u2 giữa, u3 túi họng ngay dưới môi.
    # Ba vùng theo chỗ người dùng khoanh: u1 đáy bụng sau bàn tay gần (tay không phình), u2 giữa bụng, u3 góc trên phải ngay dưới miệng.
    # 0-4 nuốt lưỡi, nhún; 4-20 hít ba hơi, ĐÁY BỤNG phình; 20-26 nín, rung; 26-47 khối phình đi dần lên: đáy xẹp, giữa bụng lồi rồi
    # xẹp, chỗ dưới miệng phồng lên (ba vùng gối nhau nên trông như một khối trôi lên); 47-48 nín; 48 bật miệng ợ ra (`nha`): chỗ
    # dưới miệng xẹp tức thì, đầu hất ngửa; giữ há, ngậm, nảy về
    def skill_fn(t, P):
        f = t * F
        r1 = rung(t, 16 / F, 26 / F)
        r2 = rung(t, 44 / F, 57 / F)
        aL = spl(f, [(0, 0), (4, 0), (8, .42), (10, .3), (14, .74), (16, .62), (20, 1), (26, 1.03), (30, .82), (34, .45), (38, .12), (42, -.06), (48, -.08),
                     (52, .06), (56, 0), (70, 0)]) * (1 + 0.03 * r1)
        aM = spl(f, [(0, 0), (20, .1), (26, .14), (30, .5), (34, .88), (38, .7), (42, .34), (46, .1), (50, 0), (70, 0)])
        aT = spl(f, [(0, 0), (30, 0), (34, .16), (38, .52), (42, .9), (45, 1.06), (48, 1.04)]) * (1 + 0.03 * r2) if f < 48 else \
            ln(f, [(48, 1.04), (48.7, .1), (50.5, 0), (53, .06), (56, 0), (70, 0)])
        phong(P, 0, aL)                                                       # đáy bụng lồi XUỐNG dưới (sau bàn tay gần): cả thân được đội lên
        P.move("than", 0, 0.085 * H * max(0.0, aL))
        phong(P, 1, aM)
        phong(P, 2, aT)
        no(P, 0.6 * max(0.0, 0.3 * aL + 0.45 * aM + 0.35 * aT))                # cả người nở nhẹ theo khối phình
        P.rot("day", spl(f, [(0, 0), (4, -2), (8, 2.5), (14, 5), (20, 7.5), (26, 8), (34, 6.5), (42, 4), (47, 2), (48.7, 11), (51, 8), (57, 6), (61, -2.5),
                             (65, .8), (70, 0)]))
        P.move("than", KX * spl(f, [(0, 0), (4, 0), (20, -9), (26, -10), (40, -5), (47, -2), (48.7, -15), (57, -10), (61, 3), (70, 0)]) + 0.9 * r1,
               KY * spl(f, [(0, 0), (4, -6), (8, 2), (20, 4), (26, 4), (36, 8), (44, 13), (47.5, 14), (48.7, 5), (57, 3), (61, -4), (65, 1.5), (70, 0)]))
        P.scale("than", spl(f, [(0, 1), (4, 1.04), (8, .99), (26, 1), (36, .98), (44, .95), (47.5, .95), (48.7, 1.07), (53, 1.01), (61, 1.04), (65, .99), (70, 1)]),
                spl(f, [(0, 1), (4, .96), (8, 1.01), (26, 1), (36, 1.03), (44, 1.07), (47.5, 1.07), (48.7, .92), (53, .99), (61, .96), (65, 1.01), (70, 1)]))
        gat = spl(f, [(0, 0), (4, -5), (8, 1.5), (14, 3), (20, 5), (26, 6), (36, 3), (43, 5), (47.5, 7), (48.7, 3), (57, 2), (61, -6), (64, 2), (70, 0)])
        a = ln(f, [(0, 0), (48, 0), (48.7, 34), (50.5, 30), (57, 28), (60.5, 0)]) + 1.3 * r2 * (1 if 48.7 <= f < 57 else 0)
        mo = ln(f, [(0, 0), (48, 0), (48.7, 1), (57, 1), (60.5, 0)])
        ha(P, gat, a, 11 * mo)
        if f < 12:
            nuot(P, f, 0)
        tha(P, f, 62) if f >= 12 else None
        if 22 <= f < 48.4 or 60 <= f < 63:
            nham(P)

    # ---------------- hit: bị đẩy ngả ra sau, nhắm mắt, miệng bật hé, lưỡi văng; nảy về
    def hit_fn(t, P):
        f = t * F
        P.rot("day", ln(f, [(0, 0), (1, 8), (3, 10.5), (6, 6), (9, -2.5), (12, 1), (16, 0)]))
        P.move("than", KX * ln(f, [(0, 0), (1, -16), (3, -26), (6, -15), (9, 3), (12, -1), (16, 0)]),
               KY * ln(f, [(0, 0), (1, 5), (3, 13), (6, 8), (9, -3), (12, 1), (16, 0)]))
        P.scale("than", ln(f, [(0, 1), (1, .88), (3, .93), (6, 1.05), (9, 1.03), (12, .99), (16, 1)]),
                ln(f, [(0, 1), (1, 1.12), (3, 1.07), (6, .95), (9, .97), (12, 1.01), (16, 1)]))
        gat = ln(f, [(0, 0), (1, 6), (3, 9), (6, 3), (9, -4), (12, 1), (16, 0)])
        ha(P, gat, ln(f, [(0, 0), (1, 5), (4, 6), (8, 0)]), ln(f, [(0, 0), (1, 4), (4, 4), (8, 0)]))
        phinh(P, ln(f, [(0, 1), (1, .9), (4, 1.08), (8, .97), (12, 1.02), (16, 1)]))
        for i, b_ in enumerate(l):
            P.rot(b_, (8 + 3 * i) * ln(f, [(0, 0), (1.5, 1), (5, -.45), (9, .2), (13, 0)]))
        if 0.5 <= f < 9.5:
            nham(P)

    # ---------------- die: trúng đòn giật, ngã ngửa ra sau (lăn trên lưng tròn), chân tay chổng lên, miệng há, lưỡi dài thè ra khỏi miệng
    # rồi rũ xuống phía trước; nảy tắt dần, chân giật hai cái, rồi mờ đi
    LAT = 72.0
    Vd = np.vstack([sk.atts["than"]["than"]["V"], sk.atts["bung"]["bung"]["V"]])
    pv = sk.W0["lat"][:2, 2]

    def cham_dat(goc):
        """thân xoay `goc` độ quanh xương lat thì phải nhấc lên bao nhiêu để điểm thấp nhất vừa chạm đất."""
        r = math.radians(goc)
        y = pv[1] + math.sin(r) * (Vd[:, 0] - pv[0]) + math.cos(r) * (Vd[:, 1] - pv[1])
        return -float(y.min())

    def die_fn(t, P):
        f = t * F
        lat = ln(f, [(0, 0), (2, -5), (5, 16), (9, 54), (12, 81), (15, 66), (18, 76), (21, 70), (24, LAT), (60, LAT)])
        P.rot("lat", lat)
        P.move("lat", -0.2 * H * ln(f, [(0, 0), (3, .08), (12, 1), (60, 1)]),
               cham_dat(lat) + H * ln(f, [(0, 0), (5, .03), (9, .09), (12, 0), (15, .07), (18, 0), (21, .025), (24, 0), (60, 0)]))
        P.scale("than", ln(f, [(0, 1), (1, .9), (4, 1.06), (9, 1), (12, 1.1), (15, .96), (18, 1.04), (21, .99), (24, 1)]),
                ln(f, [(0, 1), (1, 1.1), (4, .95), (9, 1), (12, .9), (15, 1.04), (18, .97), (21, 1.01), (24, 1)]))
        a = ln(f, [(0, 0), (1, 8), (5, 10), (12, 15), (15, 8), (18, 12), (24, 10), (60, 10)])
        ha(P, 0, a, ln(f, [(0, 0), (1, 3), (12, 3), (60, 3)]))
        phinh(P, ln(f, [(0, 1), (1, .9), (5, 1.05), (12, 1.14), (15, .95), (18, 1.07), (21, .98), (24, 1.02), (28, 1), (60, 1)]))
        theo(P, ln(f, [(0, 0), (2, 0), (5, 1), (60, 1)]))
        P.alpha["chan_x"] = ln(f, [(0, 0), (5, 0), (6, 1), (60, 1)])
        kick = ln(f, [(0, 0), (5, 0), (9, 1), (12, -.5), (15, .7), (18, -.3), (22, .2), (26, 0), (33, 0), (35, .5), (37, -.2), (39, 0), (60, 0)])
        gio = ln(f, [(0, 0), (5, 0), (12, 1.2), (15, .85), (18, 1.05), (24, 1), (60, 1)])        # chân tay chổng lên trời
        P.rot("dui", 34 * gio + 14 * kick)
        vung(P, "ban", "dui", 40 * gio + 18 * kick)
        P.rot("chan_x", 46 * gio - 13 * kick)
        P.rot("vai", 20 * gio - 10 * kick)
        vung(P, "ban_tay", "vai", 30 * gio - 14 * kick)
        P.rot("tay_x", 24 * gio + 10 * kick)
        if f < 5:
            luoi_ngan(P, dai=ln(f, [(0, 1), (2, 1.05), (5, .3)]), truot=-ln(f, [(0, 0), (5, 8)]))
        else:
            # lưỡi dài thè ra khỏi miệng rồi rũ xuống phía trước: mỗi đốt gập thêm một ít, càng ra ngọn càng rũ; nảy tắt dần
            P.alpha["luoi"] = 0.0
            dai = ln(f, [(5, .3), (9, .62), (12, .92), (15, .82), (60, .85)])
            do = ln(f, [(5, -.3), (9, .1), (12, 1.25), (15, .8), (18, 1.1), (21, .95), (24, 1), (60, 1)])
            do += 0.10 * math.exp(-max(0.0, f - 24) / 10.0) * math.sin(2 * math.pi * (f - 24) / 12.0) if f > 24 else 0.0
            P.alpha["luoi_ru"] = 1.0
            P.scale(d[0], dai, 1.0)
            for b_, g_ in zip(d[1:], (0, 0, 0, -6, -16, -24, -26)):          # phần trong miệng nằm thẳng dọc khe miệng, phần ló ra mới rũ
                P.rot(b_, g_ * do)
        nham(P)
        if f > 46:
            an_het(P, ln(f, [(46, 1), (56, 0), (60, 0)]))

    return [Clip("appear", 24 / F, appear_fn, mem=mem()),
            Clip("idle", 80 / F, idle_fn, loop=True),
            Clip("attack", 38 / F, attack_fn, ev=[(14 / F, "trung", "")], mem=mem()),
            Clip("cast", 54 / F, cast_fn, ev=[(9.5 / F, "phun", ""), (37.5 / F, "het_phun", "")], mem=mem()),
            Clip("skill", 70 / F, skill_fn, ev=[(48.7 / F, "nha", "")], mem=mem()),
            Clip("hit", 16 / F, hit_fn, mem=mem()),
            Clip("die", 58 / F, die_fn, mem=mem(1.3))]


def nuong_het(sk, cl):
    """nướng mọi clip; clip kết thúc ở dáng nghỉ thì hoà phần lò xo còn dư về khung 0 idle."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    fr = {c.ten: hoat.nuong(sk, c) for c in cl}
    for c in cl:
        if not c.loop and c.ten not in ("die", "evolve"):
            hoat.khop_cuoi(fr[c.ten], fr["idle"][0], 0.2)
    return fr


def noi_clip(sk, fr):
    """lệch lớn nhất (px rig) giữa khung 0 và khung cuối của từng clip với khung 0 idle, đo trên đỉnh lưới đã da hoá của mọi slot hiện."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    ve = soi.Ve(sk)

    def dinh(P):
        items, _ = ve.skin(P)
        return {(it[0], it[1]): it[2] for it in items if it[5] > 0.02}

    goc = dinh(fr["idle"][0])
    out = {}
    for ten, fs in fr.items():
        r = []
        for P in (fs[0], fs[-1]):
            q = dinh(P)
            if set(q) != set(goc):
                r.append(None)
            else:
                r.append(round(max(float(np.abs(q[s_] - goc[s_]).max()) for s_ in goc), 2))
        out[ten] = r
    return out


def rig(k, tien_hoa=None):
    """dựng, nướng, xuất dạng k vào inbox/ech_xanh_<k>/rig/. tien_hoa = (sk2, info2, fr2, cl2): gộp dạng sau cho clip evolve."""
    anh, hoat, khung, luoi, soi, tienhoa, trongso, xuat = _quai()
    sk, info = dung(k)
    cl = clips(sk, info, k)
    fr = nuong_het(sk, cl)
    ra = os.path.join(d_inbox(k), "rig")
    os.makedirs(ra, exist_ok=True)
    ve = soi.Ve(sk)
    h_that = soi.chieu_cao(ve, fr["idle"][0])
    cao = h_that * CAO_HIEU[k]
    ten = f"{CODE}_{k}"
    noi = {"nối clip (khung 0, khung cuối so với khung 0 idle; None = bộ slot hiện khác)": str(noi_clip(sk, fr))}
    M, clM, frM = sk, cl, fr
    if tien_hoa:
        sk2, info2, fr2, cl2 = tien_hoa
        h2 = soi.chieu_cao(soi.Ve(sk2), fr2["idle"][0]) * CAO_HIEU[2]
        ti = cao / h2
        M = tienhoa.gop(sk, sk2)

        def gong(t, P):                                                       # dạng cũ: nuốt lưỡi, bụng phình dần, rung, nhắm mắt
            b = hoat.cv(t, [(0, 1), (0.3, 0.94), (0.6, 1.16, "out"), (1.0, 1.36), (1.3, 1.5)])
            r = hoat.rung(t, 0.45, 1.3)
            for ten_u, he in (("u2", 0.9), ("u1", 0.5)):
                P.scale(ten_u, 1 + (b - 1) * he * (1 + 0.04 * r), 1 + (b - 1) * he * (1 - 0.04 * r))
            P.rot("day", hoat.cv(t, [(0, 0), (0.6, 4), (1.3, 8)]))
            mi = hoat.cv(t, [(0, 0), (0.24, 0), (0.25, 1), (1.05, 1), (1.3, 0), (2.8, 0)])       # nhắm mắt lúc gồng; tan cùng dạng cũ
            if mi > 0:
                P.alpha["mi_g"] = mi
                P.alpha["mi_x"] = mi

        def bung_ra(t, P, fl):                                                # dạng sau hiện ra: bụng nảy một nhịp, há miệng gầm
            sq = hoat.cv(t, [(0, 0), (1.5, 0), (1.75, 1, "out"), (2.0, -0.45, "io"), (2.25, 0.2, "io"), (2.45, 0, "io"), (2.8, 0)])
            P.scale("n_than", 1 + 0.12 * sq, 1 - 0.11 * sq)
            a = 16 * fl
            P.rot("n_dau", a)
            P.rot("n_ham", -(a + 7 * fl))

        memM = cl[0].mem + tienhoa.doi_ten_mem(cl2[0].mem)
        ev = tienhoa.clip_tien_hoa(M, sk, sk2, fr2["idle"][0], tiB=ti, fnA=gong, fnB=bung_ra, mem=memM)
        clM = cl + [ev]
        frM = dict(fr)
        frM["evolve"] = hoat.nuong(M, ev)
        _, _, s_ev = tienhoa.lech_cuoi(M, frM["evolve"], sk2, fr2["idle"][0], ti)
        noi["evolve"] = s_ev + f" (dạng sau co {ti:.3f} trong rig gộp)"
    Hh = info["H"]
    tk = xuat.xuat_het(M, clM, ra, ten, f"Ếch xanh dạng {k}", frames=frM, dang=k, so_dang=2, dung_yen=("cast", "skill"),
                       cao=cao, khop_idle=0, noi_them=noi, ma_goc=3230,
                       can=[("can_ha_cast", "cast", 14 / 30.0 * CHAM[k], "mieng", 0.55 * Hh),
                            ("can_luoi_attack", "attack", 14 / 30.0 * CHAM[k], "mieng", 0.75 * Hh),
                            ("can_o_skill", "skill", 45 / 30.0 * CHAM[k], "bung", 0.7 * Hh),
                            ("can_die", "die", 30 / 30.0 * CHAM[k], "than", 1.0 * Hh)])
    print(f"dạng {k}: đỉnh {info['dinh']}, cao thật {h_that:.0f} px rig, game.height {cao:.0f}; .atomik {tk['atomik_kb']:.0f} KB -> {ra}")
    print("  nối clip:", noi_clip(sk, fr))
    return sk, info, fr, cl


THU_TU = ["tay_x", "bung", "luoi", "than", "chan", "tay"]      # thứ tự vẽ sau -> trước của các mảnh cắt từ concept


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "bo_chan_xa":
        bo_chan_xa()
    elif cmd == "cat":
        cat(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    elif cmd == "rig":
        rig(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    elif cmd == "all":
        rig(2)
        sk2, info2 = dung(2, sc=SC * NHE[0], tho=NHE[1])                 # bản nhẹ của dạng 2: chỉ để gộp vào dạng 1 cho clip evolve
        cl2 = clips(sk2, info2, 2)
        rig(1, tien_hoa=(sk2, info2, nuong_het(sk2, cl2), cl2))
    else:
        print(__doc__)
