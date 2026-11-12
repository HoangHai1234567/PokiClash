# -*- coding: utf-8 -*-
"""Tượng đá giữ rừng (tuong_da): cắt MẢNH CỨNG từ năm tờ "đúng chỗ, đúng cỡ" (M_A..M_E, Codex vẽ lại concept đã duyệt, mỗi tờ giữ vài
mảnh không chồng nhau, vẽ đủ phần khuất) và từ chính concept (mười viên đá ngón tay: tròn, dựng lại bằng bao lồi).

    tuong_da_manh.py lam      → inbox/tuong_da_1/manh/<tên>.png (RGBA, cắt sát) + dat.json (chỗ đặt trên khung concept, xương bám, thứ
                                tự vẽ) + _so_ghep.png (ghép lại cạnh concept) + _to.png (từng mảnh trên nền xám)

Mảnh → xương của rig gốc monster_3423 (mọi mảnh cứng một xương): xem BANG. Con nhìn sang phải; "g" = gần (bên trái người xem, vẽ trước
thân), "x" = xa."""
import json
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tuong_da as TD  # noqa: E402

MANH = os.path.join(TD.BASE, "manh")
DUYET = os.path.join(TD.TAI, "L1_duyet.png")
INK = (43, 33, 24)
PAD = 4
# tờ → {mảnh: tâm ước chừng trên khung concept}
TO = {"A": {"dau": (800, 200), "vai_x": (1040, 420), "chop1": (750, 770)},
      "B": {"nguc_tren": (760, 420), "ban_g": (510, 890), "ban_x": (1045, 878)},
      "C": {"dai": (640, 610)},
      "D": {"loi": (822, 590)},
      "E": {"cau": (820, 412), "vai_g": (493, 410), "khoa": (845, 692), "cang_g": (450, 760), "cang_x": (1085, 750), "chop2": (679, 828),
            "chop3": (852, 785), "da_g1": (453, 552), "da_g2": (383, 609), "da_g3": (485, 629), "da_x1": (1063, 570), "da_x2": (1161, 597),
            "da_x3": (1047, 641), "da_x4": (1108, 632)}}
# mảnh → xương bộ chính của rig gốc
XUONG = {"dau": "bone6", "cau": "bone5", "nguc_tren": "bone30", "dai_sau": "bone2", "dai_truoc": "bone2", "loi": "bone27", "loi_tat": "bone27",
         "khoa": "bone43", "chop1": "bone24", "chop2": "bone25", "chop3": "bone26", "vai_g": "bone28", "vai_x": "bone29",
         "cang_g": "bone18", "ban_g": "bone19", "cang_x": "bone11", "ban_x": "bone12",
         "da_g1": "bone36", "da_g2": "bone37", "da_g3": "bone38", "da_x1": "bone39", "da_x2": "bone40", "da_x3": "bone41", "da_x4": "bone42"}
NGON = {"g": ["bone20", "bone21", "bone22", "bone23"], "x": ["bone13", "bone14", "bone15", "bone16"]}
# thứ tự vẽ sau → trước: lòng bàn tay nấp sau đầu cụt của tảng cẳng tay (chỉ lộ khi nắm tay bay đi), các viên đá ngón vẽ trước cả hai
THU_TU = ["ban_x", "cang_x", "NGON_x", "da_x1", "da_x2", "da_x3", "da_x4", "vai_x", "chop1", "dai_sau", "loi_tat", "loi", "nguc_tren",
          "dai_truoc", "chop2", "chop3", "khoa", "da_g1", "da_g2", "da_g3", "vai_g", "ban_g", "cang_g", "NGON_g", "dau", "cau"]
DAI_CAT = 628           # đai dưới: phần dưới y này (và hai rễ) là phần vắt ra TRƯỚC vòng ngực đứng
BO_NGON = [(981, 867)]  # vùng đá khép kín KHÔNG phải ngón (phần lộ của lòng bàn tay xa)
DAU_NGON = "da_g2"      # viên đá tròn trơn của tờ E dùng làm CON DẤU cho tám viên đá ngón tay (nét mực thật, hình kín)
DK_NGON = {"g": 72.0, "x": 68.0}                                     # đường kính viên đá ngón (kể cả nét mực), đo trên concept
GOC_NGON = {"g": [20, 115, 200, 300], "x": [250, 160, 60, 330]}      # mỗi ngón xoay con dấu một góc khác
# lòng bàn tay Codex vẽ to và thấp hơn chỗ nó nấp trong concept: co cả mảnh về khung này (x0, y0, bề rộng)
BAN_KHUNG = {"ban_g": (430, 832, 182), "ban_x": (950, 835, 155)}
NGUC_DAY = 712          # vòng ngực đứng: Codex vẽ tròn đều nên đáy thò dưới đai; ép dọc cả mảnh cho đáy về y này (nấp sau đai)
if TD.K == 1:           # DẠNG 1 "Mầm Đá": số đo trên concept dạng 1 (bốn viên đá nhỏ, mảnh nhỏ hơn)
    TO = {"A": {"dau": (790, 280), "vai_x": (1010, 450), "chop1": (750, 800)},
          "B": {"nguc_tren": (800, 470), "ban_g": (500, 905), "ban_x": (1017, 895)},
          "C": {"dai": (620, 650)},
          "D": {"loi": (805, 605)},
          "E": {"cau": (795, 415), "vai_g": (525, 435), "khoa": (825, 720), "cang_g": (465, 780), "cang_x": (1055, 780), "chop2": (674, 830),
                "chop3": (836, 813), "da_g1": (472, 581), "da_g2": (400, 637), "da_x1": (1050, 601), "da_x2": (1130, 645)}}
    THU_TU = [t for t in THU_TU if t not in ("da_g3", "da_x3", "da_x4")]
    DAI_CAT = 655
    BO_NGON = []
    DK_NGON = {"g": 54.0, "x": 51.0}
    BAN_KHUNG = {"ban_g": (445, 866, 118), "ban_x": (958, 858, 108)}
    NGUC_DAY = 722


def el(r):
    r = max(1, int(round(r)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def doc(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(np.int32)


def nen(A, lo_min=1500):
    """mặt nạ NỀN: trắng thông ra mép ảnh + lỗ trắng kín lớn (lòng vòng ngực, lòng đai). Trắng kín nhỏ là của mảnh."""
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


def cat_to(ma, ep=False):
    p = os.path.join(TD.TAI, f"M_{ma}.png")
    A = doc(p)
    fg = ~nen(A)
    fg = cv2.morphologyEx(fg.astype(np.uint8), cv2.MORPH_OPEN, el(1)).astype(bool)
    n, lab, st, cen = cv2.connectedComponentsWithStats(fg.astype(np.uint8), 8)
    ra = {}
    da_dung = set()
    for ten, (cx, cy) in sorted(TO[ma].items(), key=lambda kv: -1):
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
    thua = [tuple(st[i, :5]) for i in range(1, n) if i not in da_dung and st[i, 4] >= 400]
    print(f"  tờ {ma}: {len(ra)} mảnh" + (f"; cụm THỪA không dùng: {thua}" if thua else ""))
    return ra


def loi_tat(im):
    """lõi TẮT: hạt mầm mất màu (xám đá ngả lục), mầm héo ngả nâu; nét mực giữ nguyên."""
    a = np.asarray(im).astype(np.float32)
    rgb, al = a[..., :3], a[..., 3:]
    sang = rgb.mean(2, keepdims=True)
    luc = (rgb[..., 1:2] - np.maximum(rgb[..., 0:1], rgb[..., 2:3])) > 18            # vùng lục (hạt, lá)
    xam = np.concatenate([sang * 0.62 + 34, sang * 0.64 + 36, sang * 0.58 + 30], 2)
    out = np.where(luc, xam, rgb)
    return Image.fromarray(np.dstack([np.clip(out, 0, 255), al]).astype(np.uint8), "RGBA")


def ngon_tay(C, ben, cang_m, ban_m):
    """các viên đá ngón tay của một bàn tay, lấy từ concept: mỗi vùng màu đá khép kín bởi nét mực (không phải tảng cẳng tay, không
    phải lòng bàn tay) là một viên; dựng đủ bằng BAO LỒI (viên tròn bị viên bên cạnh che một miếng), tô chỗ khuất, kẻ lại viền."""
    fgC = ~nen(C)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fgC.astype(np.uint8), 8)
    ys, xs = np.nonzero(ban_m)
    i_tay = np.bincount(lab[ys, xs]).argmax()
    tay = lab == i_tay
    muc = (C.max(2) < 110) & (C.sum(2) < 250)                                         # nét mực
    cang_to = cv2.dilate(cang_m.astype(np.uint8), el(3)).astype(bool)
    trong = tay & ~muc & ~cang_to
    trong = cv2.erode(trong.astype(np.uint8), el(1))
    n2, lab2, st2, cen2 = cv2.connectedComponentsWithStats(trong, 4)
    ban_loi = cv2.erode(ban_m.astype(np.uint8), el(10)).astype(bool)
    out = []
    da = np.median(C[trong.astype(bool)], axis=0)
    for i in range(1, n2):
        if st2[i, 4] < 500:
            continue
        r = lab2 == i
        nau = C[r].mean(0)
        if nau[0] - nau[2] > 55 or nau[1] - nau[0] > 25:                               # rễ nâu / rêu lục: không phải đá
            continue
        cx, cy = cen2[i]
        if st2[i, 4] > 9000:                                                          # mảng to: phần lộ của lòng bàn tay / tảng cẳng tay
            continue
        if cy < ys.min() - 40:
            continue
        if any(np.hypot(cx - bx, cy - by) < 28 for bx, by in BO_NGON):                 # phần lộ của lòng bàn tay, không phải ngón
            continue
        x_, y_, w_, h_ = st2[i, :4]                                                   # tâm khung bao (trọng tâm lệch về phía không bị che)
        out.append(dict(tam=(float(x_ + w_ / 2), float(y_ + h_ / 2)), dk=DK_NGON[ben]))
    out.sort(key=lambda d: d["tam"][0])
    print(f"  ngón {ben}: {len(out)} viên")
    return out


def con_dau(im):
    """con dấu viên đá ngón: viên đá tròn của tờ E, xoá nét mặt cắt bên trong (ngón trong concept là đá tròn trơn)."""
    a = np.asarray(im).copy()
    trong = cv2.erode((a[..., 3] > 200).astype(np.uint8), el(8)).astype(bool)
    sang = a[..., :3].astype(int).sum(2) / 3
    net = trong & (sang < np.median(sang[trong]) - 14)
    net = cv2.dilate(net.astype(np.uint8), el(1))
    rgb = cv2.inpaint(np.ascontiguousarray(a[..., :3]), net, 4, cv2.INPAINT_TELEA)
    return Image.fromarray(np.dstack([rgb, a[..., 3]]), "RGBA")


def lam():
    os.makedirs(MANH, exist_ok=True)
    C = doc(DUYET)
    P = {}
    for ma in TO:
        P.update(cat_to(ma))
    dat, anh_ = {}, {}

    def luu(ten, im, goc, xuong):
        im.save(os.path.join(MANH, ten + ".png"))
        anh_[ten] = im
        dat[ten] = dict(goc=[int(goc[0]), int(goc[1])], co=[im.width, im.height], xuong=xuong)

    for ten, (A, m) in P.items():
        if ten == "dai":
            im, goc = manh_rgba(A, m)
            luu("dai_sau", im, goc, XUONG["dai_sau"])
            # phần vắt ra trước: dải dưới y = DAI_CAT + hai rễ nâu (cụm nâu nối lên trên)
            nau = (A[..., 0] - A[..., 1] > 35) & (A[..., 0] - A[..., 2] > 60) & (A[..., 0] > 110) & m      # rễ nâu (đá kem có R − G nhỏ)
            nau = cv2.dilate(nau.astype(np.uint8), el(7)).astype(bool) & m
            Y = np.arange(m.shape[0])[:, None]
            tr = m & ((Y >= DAI_CAT) | nau)
            tr = cv2.morphologyEx(tr.astype(np.uint8), cv2.MORPH_OPEN, el(2)).astype(bool)
            im, goc = manh_rgba(A, tr)
            luu("dai_truoc", im, goc, XUONG["dai_truoc"])
            continue
        im, goc = manh_rgba(A, m)
        if ten in BAN_KHUNG:
            x0, y0, w = BAN_KHUNG[ten]
            k = w / im.width
            im = im.convert("RGBa").resize((w, max(2, round(im.height * k))), Image.LANCZOS).convert("RGBA")
            goc = (x0, y0)
        if ten == "nguc_tren":
            h2 = NGUC_DAY + PAD - goc[1]
            im = im.convert("RGBa").resize((im.width, h2), Image.LANCZOS).convert("RGBA")
        luu(ten, im, goc, XUONG[ten])
        if ten == "loi":
            luu("loi_tat", loi_tat(im), goc, XUONG["loi_tat"])
    # ngón tay từ concept
    ngon = {}
    for ben in "gx":
        ds = ngon_tay(C, ben, P["cang_" + ben][1], P["ban_" + ben][1])
        ngon[ben] = []
        dau = con_dau(anh_[DAU_NGON])
        for k, d in enumerate(ds, 1):
            ten = f"ng_{ben}{k}"
            ti = d["dk"] / ((dau.width + dau.height) / 2 - 2 * PAD)
            im = dau.convert("RGBa").resize((max(2, round(dau.width * ti)), max(2, round(dau.height * ti))), Image.LANCZOS)
            im = im.rotate(GOC_NGON[ben][(k - 1) % 4], resample=Image.BICUBIC, expand=True).convert("RGBA")
            luu(ten, im, (round(d["tam"][0] - im.width / 2), round(d["tam"][1] - im.height / 2)), None)      # xương ngón gán ở rig
            dat[ten]["tam"] = list(d["tam"])
            ngon[ben].append(ten)
    thu_tu = []
    for t in THU_TU:
        thu_tu += ngon[t[-1]] if t.startswith("NGON_") else [t]
    dat["_thu_tu"] = thu_tu
    json.dump(dat, open(os.path.join(MANH, "dat.json"), "w", encoding="utf-8"), indent=1)
    # ghép lại cạnh concept
    Wc, Hc = C.shape[1], C.shape[0]
    ghep = Image.new("RGBA", (Wc, Hc), (255, 255, 255, 255))
    for t in thu_tu:
        if t == "loi_tat":
            continue
        ghep.alpha_composite(anh_[t], tuple(dat[t]["goc"]))
    so = Image.new("RGB", (Wc * 2 + 10, Hc), (255, 255, 255))
    so.paste(Image.fromarray(C.astype(np.uint8)), (0, 0))
    so.paste(ghep.convert("RGB"), (Wc + 10, 0))
    so.save(os.path.join(MANH, "_so_ghep.png"))
    d = np.abs(np.asarray(ghep.convert("RGB")).astype(int) - C).max(2)
    print(f"  ghép so concept: {100.0 * (d > 60).mean():.2f}% điểm lệch màu rõ")
    # tờ từng mảnh trên nền xám
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
        dr.text((x, y), f"{t} {dat[t]['xuong'] or ''}", fill=(255, 255, 255), font=f)
    to.save(os.path.join(MANH, "_to.png"))
    print(os.path.join(MANH, "_so_ghep.png"))
    print(os.path.join(MANH, "_to.png"), len(thu_tu), "mảnh")


if __name__ == "__main__":
    if sys.argv[1:2] == ["lam"]:
        lam()
    else:
        print(__doc__)
