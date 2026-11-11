# -*- coding: utf-8 -*-
"""Cắt mảnh THẲNG TỪ CONCEPT (cách lai, Claude điều phối 2026-11-11): thân chính (thân + đầu + cuống + vây đuôi + vây lưng + ngà)
là một mảnh liền; ngà, vây chèo, hàm dưới, các lớp sen (nụ) cũng cắt từ concept vì concept vẽ đủ; GPT chỉ cho lòng miệng, mí,
cánh rời, tia lỗ thở. Vùng = lớp màu + đa giác đọc trên concept kẻ lưới; nét mực lấy nhãn vùng gần nhất; chỗ thân bị sen / vây /
hàm / nước che được vá bằng ô vân lát từ chính concept (không loang màu) theo bên lưng / bụng, và kẻ lại nét viền ở mép vá.
Thuần numpy + Pillow.

    py -3 -I ArtGen/Spine/tm07_lien.py 2      -> inbox/tm07_2/lien/<tên>.png + lien.json (khung bao concept px) + _soi.png
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from quai import anh  # noqa: E402
import tm07_khop as K  # noqa: E402

INBOX = os.path.join(HERE, "inbox")
INK = (43, 33, 24)


def poly(shape, pts):
    return anh.to_da_giac(shape, pts)


def lop_ten(L):
    return {m[0]: i for i, m in enumerate(K.MAU)}


def nhan_gan_nhat(lab, need, lan=12):
    """pixel need lấy nhãn gần nhất (giãn lặp 8 hướng, đủ cho nét mực 6 px)."""
    lab = lab.copy()
    for _ in range(lan):
        miss = need & (lab < 0)
        if not miss.any():
            break
        g = lab.copy()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                sh = np.roll(np.roll(lab, dy, 0), dx, 1)
                g = np.where((g < 0) & (sh >= 0), sh, g)
        lab[miss] = g[miss]
    return lab


def o_van(rgb, box):
    """ô vân lát (phản chiếu 4 phía cho liền mép) lấy từ box (x0, y0, x1, y1) của concept."""
    t = rgb[box[1]:box[3], box[0]:box[2]]
    t = np.concatenate([t, t[:, ::-1]], 1)
    return np.concatenate([t, t[::-1]], 0)


def lat(rgb_out, mask, tile):
    H, W = mask.shape
    th, tw = tile.shape[:2]
    ys, xs = np.nonzero(mask)
    rgb_out[ys, xs] = tile[ys % th, xs % tw]


def duong_duoi(pts, x):
    """y của đường gấp khúc pts tại x (kéo dài hai đầu)."""
    P = np.asarray(pts, float)
    return np.interp(x, P[:, 0], P[:, 1])


def cat(k, cfg):
    base = os.path.join(INBOX, f"tm07_{k}")
    con = Image.open(os.path.join(base, "tai_ve", "L1_duyet.png")).convert("RGB")
    rgb = np.asarray(con).astype(np.uint8)
    H, W = rgb.shape[:2]
    L = K.lop(rgb, mo=1)
    T = lop_ten(L)
    bg = anh.nen_tu_mep(rgb.min(axis=2) > 236)
    fg = ~bg
    ink = (rgb.astype(int).sum(2) < 230) & fg
    shape = (H, W)
    cls = lambda *names: np.isin(L, [T[n] for n in names])  # noqa: E731
    yy0 = np.arange(H)[:, None]
    water = (cls("lam_dam", "lam", "lam_nhat") | (fg & (L == T["trang"]))) & (yy0 > cfg["nuoc_y"])   # chỉ dưới mặt nước
    for pg in cfg.get("giot", []):                                                                 # giọt bay riêng (chỉ màu lam)
        water |= poly(shape, pg) & cls("lam_dam", "lam", "lam_nhat")
    water = anh.gian(water, 5) & fg      # nới 5 px: mép sóng khử răng cưa lẫn màu khác lớp, không để thành hạt thân
    if cfg.get("nuoc_them"):
        water |= poly(shape, cfg["nuoc_them"]) & fg
    pieces = {}   # tên -> mặt nạ
    for nm, (pg, names) in cfg["manh"].items():
        m = poly(shape, pg) & fg
        if names:
            m &= cls(*names) | ink
        pieces[nm] = m
    # thân chính = hình − nước − các mảnh rời − nét mực (nét lấy nhãn gần nhất sau)
    lab = np.full(shape, -1, np.int32)
    order = ["than"] + list(cfg["manh"])
    body = fg & ~water
    for nm in cfg["manh"]:
        body &= ~pieces[nm]
    lab[body & ~ink] = 0
    for i, nm in enumerate(cfg["manh"], 1):
        lab[pieces[nm] & ~ink] = i
    # dọn: thân chỉ giữ cụm ≥ 3000 px, mảnh rời chỉ giữ cụm lớn nhất (vụn do khử răng cưa, vân chì lẫn màu)
    for i in range(len(cfg["manh"]) + 1):
        m = lab == i
        lb, cs = anh.thanh_phan(m)
        if not cs:
            continue
        if i == 0:
            keep = [c["i"] for c in cs if c["dt"] >= 3000]
        else:
            keep = [c["i"] for c in cs if c["dt"] >= 300]
        lab[m & ~np.isin(lb, keep)] = -1
    any_pg = np.zeros(shape, bool)
    for nm in cfg["manh"]:
        any_pg |= poly(shape, cfg["manh"][nm][0])
    lab = nhan_gan_nhat(lab, fg & (lab < 0) & (~water | any_pg))   # mảnh rời (vây chèo) được lấy cả nét trong vùng nước
    lab[water & (lab == 0)] = -1
    # mảnh "lớp màu" bị nét mực của mảnh khác lấn: giữ trong đa giác của nó
    for i, nm in enumerate(cfg["manh"], 1):
        pg, _ = cfg["manh"][nm]
        out = (lab == i) & ~poly(shape, pg)
        lab[out] = 0
    # vá thân: vùng khuất (đa giác) ∪ chỗ các mảnh rời che thân (trong đa giác che) lát ô vân theo bên lưng / bụng
    rgb2 = rgb.copy()
    than = lab == 0
    hid = np.zeros(shape, bool)
    for pg in cfg["khuat"]:
        hid |= poly(shape, pg)
    for nm, noi in cfg.get("khuat_manh", {}).items():   # vá cả dưới mảnh rời (nới vài px: viền mực mảnh nằm ngoài đa giác)
        hid |= anh.gian(pieces[nm], noi)
    hid &= ~than
    hid &= ~np.isin(lab, [i for i, nm in enumerate(cfg["manh"], 1) if nm in cfg.get("giu_tren", ())])   # không vá dưới mảnh thuộc đầu
    yy, xx = np.mgrid[0:H, 0:W]
    bien = duong_duoi(cfg["ranh"], xx)
    tren = yy < bien
    tiles = {nm: o_van(rgb, bx) for nm, bx in cfg["o_van"].items()}
    lat(rgb2, hid & tren, tiles["lung"])
    lat(rgb2, hid & ~tren, tiles["bung"])
    for nm, bx in cfg.get("o_van_rieng", {}).items():   # vùng vá riêng (vd. lưng sau sen)
        pg, ten_tile = bx
        m = hid & poly(shape, pg)
        lat(rgb2, m, tiles[ten_tile])
    # lỗ hàm dưới + lỗ miệng trong mảnh thân: tô đỏ rượu (lòng miệng) ngay trong mảnh thân, hàm rời vẽ đè lên; há hàm là lộ lòng
    # miệng đúng hình lỗ, không tràn ra ngoài bóng dáng (lỗi đã gặp: mảng GPT sau thân thò ra ngoài mõm)
    rk = np.zeros(shape, bool)
    for i, nm in enumerate(cfg["manh"], 1):
        if nm in cfg.get("long_mieng", ()):
            rk |= anh.gian(lab == i, 2)
    rk &= ~than
    rk &= fg                                   # chỉ trong bóng dáng concept (không thò ra ngoài mõm)
    if rk.any():
        rgb2[rk] = (139, 47, 69)
        ys_, xs_ = np.nonzero(rk)
        cx_, cy_ = xs_.mean(), ys_.mean()
        rr = anh.to_da_giac(shape, [(cx_ + 0.45 * (xs_.max() - xs_.min()) * np.cos(t), cy_ + 0.3 * (ys_.max() - ys_.min()) * np.sin(t)) for t in np.linspace(0, 6.283, 40)]) & rk
        rgb2[rr] = (106, 31, 51)
    than_full = than | hid | rk
    # lỗ kín còn sót trong thân (vụn nhãn, mép khử răng cưa): lát ô vân theo bên lưng / bụng
    lo = ~than_full & ~anh.nen_tu_mep(~than_full)
    lo &= ~np.isin(lab, [i for i, nm in enumerate(cfg["manh"], 1)])   # không lấp chỗ của mảnh rời
    if lo.any():
        lat(rgb2, lo & tren, tiles["lung"])
        lat(rgb2, lo & ~tren, tiles["bung"])
        than_full |= lo
        print(f"  lấp {int(lo.sum())} px lỗ kín trong thân")
    # kẻ nét viền ở mép vá (mép mặt nạ thân mà pixel là chỗ vá)
    er = anh.co(than_full, 3)
    mep = than_full & ~er & hid
    mep = anh.gian(mep, 2) & than_full
    rgb2[mep] = INK
    out = {}
    lien = {}

    def luu(nm, m, src):
        ys, xs = np.nonzero(m)
        if not len(ys):
            print("  (trống)", nm)
            return
        x0, y0, x1, y1 = int(xs.min()) - 2, int(ys.min()) - 2, int(xs.max()) + 3, int(ys.max()) + 3
        x0, y0 = max(0, x0), max(0, y0)
        a = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
        a[..., :3] = src[y0:y1, x0:x1]
        al = anh.lam_mo(m[y0:y1, x0:x1].astype(np.float32), 0.8)
        a[..., 3] = (np.clip(al * 1.3, 0, 1) * 255).astype(np.uint8)
        a[..., :3][a[..., 3] == 0] = 0
        im = Image.fromarray(a, "RGBA")
        im = Image.fromarray(np.asarray(anh.loang_mau(im)))
        out[nm] = im
        lien[nm] = [x0, y0, x1, y1]
        print(f"  {nm}: {x1 - x0}x{y1 - y0} tại ({x0}, {y0})")
    luu("than", than_full, rgb2)
    for i, nm in enumerate(cfg["manh"], 1):
        luu(nm, lab == i, rgb)
    ra = os.path.join(base, "lien")
    os.makedirs(ra, exist_ok=True)
    for nm, im in out.items():
        im.save(os.path.join(ra, nm + ".png"))
    json.dump(lien, open(os.path.join(ra, "lien.json"), "w"), indent=1)
    anh.to_soi(ra, list(out), rong=1800)
    # ảnh nhãn để soi
    pal = np.array([(90, 90, 90)] + [(60, 60, 200), (200, 60, 60), (60, 180, 60), (220, 180, 40), (180, 60, 200), (40, 190, 200),
                                     (230, 120, 60), (120, 230, 120), (200, 200, 60), (60, 120, 230), (230, 60, 160), (130, 90, 40)], np.uint8)
    vis = pal[np.clip(lab + 1, 0, len(pal) - 1)]
    vis[hid] = (255, 255, 255)
    Image.fromarray(vis).resize((W // 2, H // 2)).save(os.path.join(ra, "_nhan.png"))
    print("  ->", ra, "|", os.path.join(ra, "_soi.png"), os.path.join(ra, "_nhan.png"))
    return out, lien


# ---------------------------------------------------------------- cấu hình (toạ độ concept 1536x1024 đọc trên ảnh kẻ lưới)
CFG = {
    2: {
        "nuoc_y": 690,
        "nuoc_them": None,
        "giot": [[(120, 640), (215, 640), (215, 730), (120, 730)], [(1235, 640), (1360, 640), (1360, 740), (1235, 740)]],
        # mảnh rời: (đa giác, lớp màu hoặc None = mọi màu trong đa giác)
        "manh": {
            "nga": ([(1243, 348), (1262, 300), (1300, 262), (1500, 142), (1532, 180), (1335, 352)], ("vang", "vang_nhat", "muc")),
            "ham": ([(1176, 440), (1230, 433), (1300, 418), (1350, 405), (1356, 445), (1332, 486), (1292, 520), (1232, 528), (1184, 504)], None),
            "mieng": ([(1222, 392), (1338, 388), (1344, 440), (1232, 450)], ("ruou", "muc")),
            "vay_cheo": ([(896, 580), (952, 598), (988, 640), (978, 705), (932, 795), (852, 872), (700, 888), (666, 850), (720, 760), (798, 660)], None),
            "vx": ([(972, 328), (984, 250), (1040, 220), (1122, 234), (1138, 298), (1100, 324)], None),
            "sen_sau": ([(606, 470), (612, 330), (640, 262), (680, 222), (960, 220), (966, 470), (800, 522), (700, 522)], ("do", "hong", "hong_nhat", "muc")),
            "sen_truoc": ([(688, 335), (728, 288), (792, 278), (852, 330), (852, 425), (772, 475), (700, 445)], ("hong", "do", "hong_nhat", "muc")),
            "dai": ([(700, 290), (830, 290), (830, 360), (700, 360)], ("vang", "vang_nhat", "muc")),
        },
        "giu_tren": ("nga", "mieng", "ham"),
        "long_mieng": ("mieng", "ham"),
        "khuat_manh": {"vay_cheo": 6},   # vây xa vẽ SAU thân: không vá dưới nó (vá sẽ che mất)
        # vùng khuất phải vá (bụng dưới nước, bụng sau vây chèo, lưng sau sen)
        "khuat": [[(290, 556), (370, 660), (460, 760), (600, 830), (780, 850), (940, 840), (1060, 800), (1150, 720), (1190, 630), (1100, 600), (900, 590), (700, 640), (500, 620), (380, 580)],
                  [(896, 580), (952, 598), (988, 640), (978, 705), (932, 795), (852, 872), (700, 888), (666, 850), (720, 760), (798, 660)],
                  [(585, 478), (700, 500), (850, 472), (962, 420), (966, 530), (585, 530)]],
        "ranh": [(300, 640), (450, 682), (600, 700), (750, 670), (900, 622), (1050, 562), (1200, 500)],
        "o_van": {"lung": (880, 500, 944, 564), "bung": (1000, 620, 1064, 684)},
    },
    1: {
        "nuoc_y": 745,
        "nuoc_them": None,
        "giot": [[(60, 570), (150, 570), (150, 650), (60, 650)], [(700, 580), (770, 580), (770, 650), (700, 650)]],
        "manh": {
            "nga": ([(988, 292), (1030, 272), (1082, 282), (1092, 362), (1000, 372)], ("vang", "vang_nhat", "muc")),
            "ham": ([(1046, 570), (1116, 572), (1120, 612), (1060, 618)], None),
            "mieng": ([(1052, 556), (1104, 556), (1104, 600), (1052, 600)], ("ruou", "muc")),
            "vay_cheo": ([(698, 598), (762, 618), (794, 660), (764, 762), (690, 744), (672, 660)], None),
            "de_nu": ([(646, 336), (806, 336), (806, 380), (646, 380)], ("cham", "peri", "muc")),
            "nu_sau": ([(638, 345), (640, 240), (700, 150), (760, 148), (812, 245), (808, 345)], ("do", "hong", "hong_nhat", "muc")),
        },
        "giu_tren": ("nga", "mieng", "ham"),
        "long_mieng": ("mieng", "ham"),
        "khuat_manh": {"vay_cheo": 6, "de_nu": 6},
        "khuat": [[(440, 640), (470, 720), (600, 792), (800, 804), (1000, 784), (1100, 724), (1110, 660), (440, 650)],
                  [(688, 568), (772, 568), (772, 652), (688, 652)],   # giọt nước phải vẽ đè lên thân
                  [(698, 598), (762, 618), (794, 660), (764, 762), (690, 744), (672, 660)],
                  [(640, 332), (812, 330), (812, 390), (640, 390)]],
        "ranh": [(430, 590), (600, 640), (800, 662), (1000, 640), (1120, 600)],
        "o_van": {"lung": (560, 440, 624, 504), "bung": (820, 690, 884, 754)},
    },
}

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    k = int(sys.argv[1])
    cat(k, CFG[k])
