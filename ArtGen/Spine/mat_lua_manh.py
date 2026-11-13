# -*- coding: utf-8 -*-
"""Mắt lửa bọc giáp (mat_lua): cắt MẢNH CỨNG từ năm tờ "đúng chỗ, đúng cỡ" (M_A..M_E: Codex vẽ lại concept đã duyệt, mỗi tờ giữ vài
mảnh không chồng nhau, vẽ đủ phần khuất).

    mat_lua_manh.py lam      → inbox/mat_lua_1/manh/<tên>.png (RGBA, cắt sát) + dat.json (chỗ đặt trên khung concept, xương bám, thứ tự
                               vẽ) + _so_ghep.png (ghép lại cạnh concept) + _to.png (từng mảnh trên nền xám)

Mảnh → slot / xương của rig gốc monster_3342 (con nhìn sang phải; "gan" = bên trái người xem, "xa" = bên phải). Hai hình đổi màu bằng
mã: `mat_tat` (mắt tắt: tròng xám tro, con ngươi than) và `cau_tat` (cầu lửa nguội: than tím sẫm, vân hồng than) cho appear / die."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mat_lua as G  # noqa: E402

MANH = os.path.join(G.BASE, "manh")
DUYET = os.path.join(G.TAI, "L1_duyet.png")
PAD = 4
# tờ → {mảnh: tâm ước chừng trên khung concept}
TO = {"A": {"cau": (805, 560), "nam_gan": (380, 800)},
      "B": {"mu": (800, 400), "duoi_trai": (620, 665), "nam_xa": (1180, 780)},
      "C": {"vai_gan": (480, 490), "vai_xa": (1050, 400), "duoi_phai": (990, 800), "nho_mat": (755, 550)},
      "D": {"mat": (932, 652), "tay_gan": (425, 628), "tay_xa": (1138, 618)},
      "E": {"lua": (600, 330), "giot1": (452, 50), "giot2": (320, 250), "duoi_giua": (700, 810), "nho_phai": (1100, 532)}}
# mảnh → slot của rig gốc (None = mảnh thêm của mình)
SLOT = {"cau": "shenti_01", "cau_tat": "shenti_01", "mat": "yanjing_01", "mat_tat": "yanjing_01", "mu": "tou_01", "nho_mat": "tou_02",
        "nho_phai": "tou_03", "vai_gan": "jian_03", "vai_xa": "jian_02", "duoi_trai": "shitou_01", "duoi_giua": "shitou_04",
        "duoi_phai": "shitou_03", "tay_gan": "shoubi_01", "tay_xa": "shoubi_02", "nam_gan": "shou_01", "nam_xa": "shou_02",
        "lua": None, "giot1": None, "giot2": None}
# thứ tự vẽ sau → trước. Theo con gốc, trừ một chỗ theo concept đã duyệt: tấm dưới giữa đè lên tấm dưới trái. Cả bên XA (khúc
# tay, nắm tay, tấm vai) nằm SAU quả cầu và tấm đầu như con gốc (người dùng 2026-11-13: "giáp vai tay phải layer phải nằm dưới giáp
# đầu và thân", "khi walk tay bên kia phải nằm dưới thân chứ"); concept vẽ tấm vai xa đè mép tấm đầu, nắm tay xa đè tấm dưới phải.
THU_TU = ["giot2", "giot1", "lua", "tay_xa", "nam_xa", "vai_xa", "cau_tat", "cau", "mat_tat", "mat", "nho_phai", "mu", "nho_mat",
          "duoi_phai", "duoi_trai", "duoi_giua", "tay_gan", "vai_gan", "nam_gan"]
if G.K == 2:            # DẠNG 2 (hàm nanh, nắm tay trơn): số đo trên concept dạng 2; ba tấm dưới thành hàm, tấm giữa đè hai tấm bên
    TO = {"A": {"cau": (815, 625)},
          "B": {"mu": (830, 390), "nam_gan": (340, 780), "nam_xa": (1220, 770)},
          "C": {"vai_gan": (480, 490), "vai_xa": (1120, 420), "duoi_phai": (1010, 810)},
          "D": {"mat": (925, 668), "tay_gan": (520, 605), "tay_xa": (1115, 590)},
          "E": {"lua": (600, 330), "giot1": (445, 65), "giot2": (258, 275), "duoi_giua": (780, 820), "nho_phai": (1110, 535)},
          "F": {"nho_mat": (760, 570), "duoi_trai": (575, 810)}}
    # khúc tay GẦN cũng nằm sau quả cầu (lúc quay chong chóng không vắt ngang trước mắt và hàm; chỉ lộ ở mép cầu)
    THU_TU = ["giot2", "giot1", "lua", "tay_xa", "tay_gan", "nam_xa", "vai_xa", "cau_tat", "cau", "mat_tat", "mat", "nho_phai", "mu",
              "nho_mat", "duoi_trai", "duoi_phai", "duoi_giua", "vai_gan", "nam_gan"]


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def doc(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.int32)


def nen(A, lo_min=4000):
    """mặt nạ NỀN: trắng thông ra mép ảnh + lỗ trắng kín lớn. Trắng kín nhỏ (chấm sáng trong mắt) là của mảnh."""
    trang = (A.min(2) > 236).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(trang, 4)
    bg = np.zeros(trang.shape, bool)
    H, W = trang.shape
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if x == 0 or y == 0 or x + w == W or y + h == H or a >= lo_min:
            bg |= lab == i
    return bg


def manh_rgba(A, m):
    """ảnh RGBA cắt sát của mặt nạ m (mép mềm 1 px theo độ sáng: điểm mép ngả trắng thì trong dần)."""
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, el(2)).astype(bool)
    n, lab = cv2.connectedComponents((~m).astype(np.uint8), connectivity=4)
    for i in range(1, n):                                    # lấp lỗ nhỏ kín trong mảnh (điểm trắng lọt giữa vân sáp)
        r = lab == i
        ys, xs = np.nonzero(r)
        if xs.min() > 0 and ys.min() > 0 and xs.max() < m.shape[1] - 1 and ys.max() < m.shape[0] - 1 and r.sum() < 4000:
            m |= r
    ys, xs = np.nonzero(m)
    x0, y0, x1, y1 = max(0, xs.min() - PAD), max(0, ys.min() - PAD), min(m.shape[1], xs.max() + PAD + 1), min(m.shape[0], ys.max() + PAD + 1)
    sub = A[y0:y1, x0:x1].astype(np.uint8)
    mm = m[y0:y1, x0:x1]
    a = cv2.GaussianBlur(mm.astype(np.float32), (0, 0), 0.8)
    vien = mm & ~cv2.erode(mm.astype(np.uint8), el(2)).astype(bool)
    sang = sub.min(2).astype(np.float32)
    a = np.where(vien, np.minimum(a, np.clip((250.0 - sang) / 70.0, 0, 1)), a)
    out = np.dstack([sub, (np.clip(a, 0, 1) * 255).astype(np.uint8)])
    out[..., :3][out[..., 3] == 0] = 0
    return Image.fromarray(out, "RGBA"), (int(x0), int(y0))


def cat_to(ma):
    p = os.path.join(G.TAI, f"M_{ma}.png")
    A = doc(p)
    if A.shape[:2] != (1024, 1536):
        raise SystemExit(f"tờ {ma}: cỡ {A.shape[1]}x{A.shape[0]}, phải 1536x1024")
    fg = ~nen(A)
    fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, el(1)).astype(bool)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    ra = {}
    da_dung = set()
    for ten, (cx, cy) in TO[ma].items():
        best, bi = 1e18, -1
        for i in range(1, n):
            if st[i, 4] < 250 or i in da_dung:
                continue
            x, y, w, h, _ = st[i]
            dx = max(x - cx, 0, cx - (x + w))
            dy = max(y - cy, 0, cy - (y + h))
            d = dx * dx + dy * dy + 0.02 * ((cen[i][0] - cx) ** 2 + (cen[i][1] - cy) ** 2)
            if d < best:
                best, bi = d, i
        if bi < 0:
            raise SystemExit(f"tờ {ma}: không thấy mảnh {ten}")
        da_dung.add(bi)
        ra[ten] = (A, lab == bi)
    thua = [tuple(int(v) for v in st[i, :5]) for i in range(1, n) if i not in da_dung and st[i, 4] >= 300]
    print(f"  tờ {ma}: {len(ra)} mảnh" + (f"; cụm THỪA không dùng: {thua}" if thua else ""))
    return ra


def doi_mau(im, bang, giu_muc=True):
    """đổi màu theo bảng [(màu cũ, màu mới)]: mỗi điểm (không phải mực) lấy độ lệch so với màu cũ gần nhất cộng vào màu mới (giữ vân
    sáp); nét mực giữ nguyên."""
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3:]
    cu = np.array([c for c, _ in bang], np.float32)
    moi = np.array([m for _, m in bang], np.float32)
    d = ((rgb[..., None, :] - cu[None, None]) ** 2).sum(-1)
    k = d.argmin(-1)
    lech = (rgb - cu[k]) * 0.55
    out = moi[k] + lech
    muc = rgb.max(2) < 95
    if giu_muc:
        out[muc] = rgb[muc]
    return Image.fromarray(np.dstack([np.clip(out, 0, 255), al]).astype(np.uint8), "RGBA")


MAT_TAT = [((255, 236, 160), (128, 118, 112)), ((150, 24, 30), (64, 54, 58)), ((255, 255, 240), (128, 118, 112))]
CAU_TAT = [((220, 58, 34), (70, 54, 66)), ((244, 128, 34), (88, 62, 70)), ((255, 206, 80), (110, 72, 72))]


def lam():
    os.makedirs(MANH, exist_ok=True)
    C = doc(DUYET)
    P = {}
    for ma in TO:
        if not os.path.exists(os.path.join(G.TAI, f"M_{ma}.png")):
            print(f"  chưa có tờ {ma}")
            continue
        P.update(cat_to(ma))
    dat, anh_ = {}, {}

    def luu(ten, im, goc):
        im.save(os.path.join(MANH, ten + ".png"))
        anh_[ten] = im
        dat[ten] = dict(goc=[int(goc[0]), int(goc[1])], co=[im.width, im.height], slot=SLOT[ten])

    for ten, (A, m) in P.items():
        im, goc = manh_rgba(A, m)
        luu(ten, im, goc)
        if ten == "mat":
            luu("mat_tat", doi_mau(im, MAT_TAT), goc)
        if ten == "cau":
            luu("cau_tat", doi_mau(im, CAU_TAT), goc)
    thu_tu = [t for t in THU_TU if t in anh_]
    dat["_thu_tu"] = thu_tu
    json.dump(dat, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1)
    # ghép lại cạnh concept
    Wc, Hc = C.shape[1], C.shape[0]
    ghep = Image.new("RGBA", (Wc, Hc), (255, 255, 255, 255))
    for t in thu_tu:
        if t.endswith("_tat"):
            continue
        ghep.alpha_composite(anh_[t], tuple(dat[t]["goc"]))
    so = Image.new("RGB", (Wc * 2 + 10, Hc), (255, 255, 255))
    so.paste(Image.fromarray(C.astype(np.uint8)), (0, 0))
    so.paste(ghep.convert("RGB"), (Wc + 10, 0))
    so.save(os.path.join(MANH, "_so_ghep.png"))
    d = np.abs(np.asarray(ghep.convert("RGB")).astype(int) - C).max(2)
    print(f"  ghép so concept: {100.0 * (d > 60).mean():.2f}% điểm lệch màu rõ")
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
    x = y = 12
    hh = 0
    cho = []
    for t in thu_tu:
        im = anh_[t]
        if x + im.width + 12 > 2200:
            x, y, hh = 12, y + hh + 34, 0
        cho.append((t, x, y))
        x += max(im.width, 90) + 16
        hh = max(hh, im.height)
    to = Image.new("RGB", (2200, y + hh + 40), (150, 150, 150))
    dr = ImageDraw.Draw(to)
    for t, x, y in cho:
        to.paste(anh_[t], (x, y + 20), anh_[t])
        dr.text((x, y), f"{t} {dat[t]['slot'] or ''}", fill=(255, 255, 255), font=f)
    to.save(os.path.join(MANH, "_to.png"))
    print(os.path.join(MANH, "_so_ghep.png"))
    print(os.path.join(MANH, "_to.png"), len(thu_tu), "mảnh")


if __name__ == "__main__":
    if sys.argv[1:2] == ["lam"]:
        lam()
    else:
        print(__doc__)
